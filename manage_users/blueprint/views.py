from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsAdminOrReadOnly


def index(request):
    """Главная страница с информацией о проекте."""
    return render(request, 'index.html')


@extend_schema_view(
    list=extend_schema(
        summary='Получить список пользователей',
        description='Возвращает пагинированный список пользователей с поддержкой фильтрации и поиска.',
        parameters=[
            OpenApiParameter('is_staff', bool, description='Фильтр: только администраторы'),
            OpenApiParameter('is_active', bool, description='Фильтр: только активные пользователи'),
            OpenApiParameter('search', str, description='Поиск по username, email, имени'),
            OpenApiParameter('ordering', str, description='Сортировка: -date_joined, username'),
        ],
    ),
    retrieve=extend_schema(
        summary='Получить пользователя по ID',
        description='Возвращает детальную информацию о пользователе.',
    ),
    create=extend_schema(
        summary='Создать нового пользователя',
        description='Создаёт пользователя с указанием обязательных полей. Пароль должен быть надёжным.',
        request=UserCreateSerializer,
        responses={201: UserSerializer},
    ),
    update=extend_schema(
        summary='Полностью обновить пользователя',
        description='Заменяет все поля пользователя. Требует указания всех обязательных полей.',
    ),
    partial_update=extend_schema(
        summary='Частично обновить пользователя',
        description='Обновляет только указанные поля пользователя.',
    ),
    destroy=extend_schema(
        summary='Удалить пользователя',
        description='Безвозвратно удаляет пользователя из системы.',
        responses={204: OpenApiResponse(description='Пользователь успешно удалён')},
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для управления пользователями.
    
    Доступные действия:
    - `list`: получить список пользователей
    - `retrieve`: получить пользователя по ID
    - `create`: создать нового пользователя
    - `update` / `partial_update`: обновить данные пользователя
    - `destroy`: удалить пользователя
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined', 'last_login']
    ordering = ['-date_joined']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @extend_schema(
        summary='Сменить пароль пользователя',
        description='Эндпоинт для изменения пароля. Доступен только для администраторов или для самого пользователя.',
        request={'application/json': {'type': 'object', 'properties': {'password': {'type': 'string'}}}},
        responses={
            200: OpenApiResponse(description='Пароль успешно изменён'),
            400: OpenApiResponse(description='Ошибка валидации пароля'),
            403: OpenApiResponse(description='Недостаточно прав'),
        },
    )
    @action(detail=True, methods=['post'], url_path='change-password')
    def change_password(self, request, pk=None):
        """Смена пароля пользователя."""
        user = self.get_object()
        
        # Проверка прав: админ или сам пользователь
        if not (request.user.is_staff or request.user == user):
            return Response({'detail': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
        
        password = request.data.get('password')
        if not password:
            return Response({'password': ['Поле обязательно']}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(password)
        user.save()
        
        return Response({'detail': 'Пароль успешно изменён'}, status=status.HTTP_200_OK)
