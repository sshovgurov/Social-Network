from django.test import TestCase

from posts.models import Post, Group, User


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Заголовок тестовой задачи',
            description='Описание',
            slug='test-task'
        )

        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=User.objects.create(username='Stas')
        )

    def group_check_str_output(self):
        """Метод __str__ в Group"""
        group = GroupModelTest.group
        group_title = group.title
        self.assertEqual(group_title, str(group.title))

    def post_check_str_output(self):
        """метод __str__ в Post"""
        post = GroupModelTest.post
        post_text = post.text[:15]
        self.assertEqual(post_text, str(post.text[:15]))

    def test_verbose_name_group(self):
        """verbose_name в поле group"""
        group = GroupModelTest.group
        verboses = {
            'title': 'Заголовок',
            'slug': 'Слаг',
            'description': 'Описание'
        }
        for value, expected in verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

    def test_help_text_group(self):
        """help_text в group"""
        group = GroupModelTest.group
        help_texts = {
            'title': 'Дайте название модели',
            'slug': 'Это слаг',
            'description': 'Опишите суть модели',
        }
        for value, expected in help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected)

    def test_verbose_name_post(self):
        """verbose_name в Post"""
        post = GroupModelTest.post
        verboses = {
            'text': 'текст',
            'pub_date': 'дата публикации',
            'author': 'автор',
            'group': 'сообщество'
        }
        for value, expected in verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

    def test_help_text_post(self):
        """help_text в POST"""
        post = GroupModelTest.post
        help_texts = {
            'text': 'введите текст',
            'pub_date': 'укажите дату публикации',
            'author': 'укажите автора',
            'group': 'укажите группу'
        }
        for value, expected in help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected)
