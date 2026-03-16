from django.db import models

# Мы используем встроенную модель User из django.contrib.auth
# Поэтому этот файл может оставаться пустым или содержать заглушку.

# Пример для будущего расширения (если понадобится кастомная модель):
# class UserProfile(models.Model):
#     user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, blank=True)
#     bio = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     
#     def __str__(self):
#         return f"Profile for {self.user.username}"
