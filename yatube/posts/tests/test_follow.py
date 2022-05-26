from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group, Follow


User = get_user_model()
'''Авторизованный пользователь может подписываться на других пользователей и удалять их из подписок.
Новая запись пользователя появляется в ленте тех,
кто на него подписан и не появляется в ленте тех, кто не подписан'''
class PostViewTests(TestCase):    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='stanislav')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.author = User.objects.create_user(username='staps')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Тестовая пост',
            group=cls.group,
        )
        
        cls.user2 = User.objects.create_user(username='stanislav2')
        cls.not_follow_client = Client()
        cls.not_follow_client.force_login(cls.user2)

    
    def test_new_post_appear_at_desire_follow(self):
        '''Новая запись пользователя появляется в ленте тех,
           кто на него подписан и не появляется в ленте тех, кто не подписан'''
        Follow.objects.create(user=self.user, author=self.author)

        reverse_name = reverse('posts:follow_index')
        response = self.authorized_client.get(reverse_name)
        first_object = response.context.get('page_obj')
        self.assertIsNone(first_object)

        reverse_name2 = reverse('posts:follow_index')
        response2 = self.not_follow_client.get(reverse_name2)
        second_object = response2.context.get('page_obj')[0]
        self.assertNotEqual(second_object, self.post)