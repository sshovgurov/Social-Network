from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='Stas')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Заголовок тестовой задачи',
            description='Описание',
            slug='test-task'
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user
        )

    def test_new_post_created_form(self):
        """Тест для проверки формы создания нового поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': PostFormTests.group.id
        }
        response = PostFormTests.authorized_client.post(
            reverse('new_post'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse('index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertFalse(
            Post.objects.filter(
                text='Текст поста',
                group=PostFormTests.group.id
            ).exists()
        )

    def test_post_edit_form(self):
        """Тест редактирования поста через форму"""
        editor_data = {'username': PostFormTests.post.author,
                       'post_id': PostFormTests.post.id,
                       }
        form_data = {'text': 'Обновленный тестовый текст поста',
                     'group': PostFormTests.group.id}
        self.authorized_client.post(
            reverse('post_edit', kwargs=editor_data),
            data=form_data,
            follow=False
        )
        self.assertEqual(Post.objects.get(id=PostFormTests.post.id).text,
                         form_data['text'])
