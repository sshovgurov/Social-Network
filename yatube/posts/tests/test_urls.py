from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Group, User


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Stas')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Название',
            slug='slug',
            description='Описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=PostsURLTests.user,
        )

    def test_url_to_authorized_client(self):
        """Страница доступна авторизованному пользователю."""
        urls = (
            ('new.html', reverse('new_post')),
            ('group.html', (
                reverse('group_posts', kwargs={'slug': self.group.slug})
            )),
        )
        for template, reverse_name in urls:
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_new_url_redirect_anonymous(self):
        """Страница /new/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_new_url_redirect_anonymous_on_admin_login(self):
        """Страница по адресу /new/ перенаправит анонимного
        пользователя на страницу логина"""
        response = PostsURLTests.guest_client.get('/new/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')

    def test_urls_uses_correct_templates(self):
        templates_url_names = {
            'index.html': '/',
            'group.html': reverse(
                'group_posts',
                kwargs={'slug': self.group.slug}
            ),
            'new.html': reverse('new_post'),
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_url_exists_at_desired_location(self):
        templates_url_names = [
            reverse('index'),
            reverse('profile', kwargs={'username': self.user}),
            reverse(
                'post', kwargs={
                    'username': self.user,
                    'post_id': self.post.id
                })
        ]
        for url in templates_url_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)
