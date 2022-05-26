from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group


User = get_user_model()
'''при выводе поста с картинкой изображение передаётся в словаре context
на главную страницу,
на страницу профайла,
на страницу группы,
на отдельную страницу поста;
при отправке поста с картинкой через форму PostForm создаётся запись в базе данных;'''
class PostImageTests(TestCase):    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
            group=cls.group,
        )
    
    def setUp(self):
        self.user = User.objects.create_user(username='Staps')
        self.authorized_client = Client() # второй клиент, авторизуем его
        self.authorized_client.force_login(self.user)