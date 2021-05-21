from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='sts')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Название',
            slug='test_slug',
            description='Описание',
        )

        cls.post = Post.objects.create(
            text="Тестовый текст",
            group=cls.group,
            author=cls.user,
        )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_pages_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': self.group.slug})
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_post_uses_correct_context(self):
        """Шаблон страницы создания поста сформирован с
        правильным контекстом"""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_index_uses_correct_context(self):
        """Шаблон главной страницы сформирован с правильным контекстом.
        Все созданные посты отображаются на главной странице."""
        response = self.authorized_client.get(reverse('index'))
        first_object = response.context['page'][0]
        post_group_0 = first_object.group
        post_text_0 = first_object.text
        post_author_0 = first_object.author
        self.assertEqual(post_group_0, PostViewTests.group)
        self.assertEqual(post_text_0, PostViewTests.post.text)
        self.assertEqual(post_author_0, PostViewTests.user)

    def test_group_uses_correct_context(self):
        """Шаблон group сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': self.group.slug}),
        )
        self.assertEqual(response.context['group'].title, self.group.title)
        self.assertEqual(response.context['group'].description,
                         self.group.description)
        self.assertEqual(response.context['group'].slug, self.group.slug)

    def test_post_edit_form(self):
        """Тест редактирования поста через форму"""
        editor_data = {'username': PostViewTests.post.author,
                       'post_id': PostViewTests.post.id,
                       }
        form_data = {'text': 'Обновленный тестовый текст поста',
                     'group': PostViewTests.group.id}
        self.authorized_client.post(
            reverse('post_edit', kwargs=editor_data),
            data=form_data,
            follow=False
        )
        self.assertEqual(Post.objects.get(id=PostViewTests.post.id).text,
                         form_data['text'])


class FollowUnfollowContextPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='SubZero')
        cls.sub = User.objects.create_user(username='Skorpion')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_follow_correct_context(self):
        self.authorized_client.get(
            reverse('profile_follow', kwargs={'username': self.sub.username}))
        response = self.authorized_client.get(reverse('follow_index'))
        self.assertEqual(len(response.context.get('page').object_list), 0)
        self.authorized_client.get(
            reverse('profile_unfollow',
                    kwargs={'username': self.sub.username}))
        response = self.authorized_client.get(reverse('follow_index'))
        self.assertEqual(len(response.context.get('page').object_list), 0)
