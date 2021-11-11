from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from skillprofile.models import Skill, SkillTag


class TestSkillprofile(TestCase):
    def setUp(self):
        print('setUp')

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_skill_list_basic(self):
        response = self.client.get('/skills/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn("List of all skills", content)
        self.assertIn('object_list', response.context)

    def test_skill_list(self):
        test_skill = Skill.objects.create(name='Test Skill', slug='test-slug')
        response = self.client.get('/skills/')
        self.assertEqual(len(response.context['object_list']), 1)
        self.assertIn(test_skill, response.context['object_list'])


class TestSkillprofileViewsPermissions(TestCase):

    user1_data = {'username': 'test_user1', 'password': 'test_pass'}
    user2_data = {'username': 'test_user2', 'password': 'test_pass'}
    super_user_data = {'username': 'test_super_user', 'password': 'test_pass'}
    user_w_perms_data = {'username': 'test_user_w_perms', 'password': 'test_pass'}

    @classmethod
    def setUpClass(cls):
        """Set up data for the whole TestCase"""
        super().setUpClass()

        cls.user1 = get_user_model().objects.create_user(**cls.user1_data)
        cls.user2 = get_user_model().objects.create_user(**cls.user2_data)
        cls.super_user = get_user_model().objects.create_superuser(**cls.super_user_data)
        cls.user_w_perms = get_user_model().objects.create_user(**cls.user_w_perms_data)

        cls.user1_skill = Skill.objects.create(name='user1_skill', slug='user1_slug', author_user=cls.user1)
        cls.user2_skill = Skill.objects.create(name='user2_skill', slug='user2_slug', author_user=cls.user2)

        cls.user1_tag = SkillTag.objects.create(name='user1_tag', slug='user1_slug', author_user=cls.user1)

    def test_user_skill_delete(self):
        """User can't delete somebody's skill"""
        self.client.login(**self.user1_data)
        response = self.client.get(reverse('user-skill-delete', kwargs={'username': self.user2.username,
                                                                        'slug': self.user2_skill.slug}))
        self.assertEqual(response.status_code, 403)

    def test_superuser_skill_delete(self):
        """Superuser can delete every skill"""
        self.client.login(**self.super_user_data)
        response = self.client.get(reverse('user-skill-delete', kwargs={'username': self.super_user.username,
                                                                        'slug': self.user2_skill.slug}))
        self.assertEqual(response.status_code, 200)

    def test_user_own_skill_delete(self):
        """User can delete his own skill"""
        self.client.login(**self.user1_data)
        response = self.client.get(reverse('user-skill-delete', kwargs={'username': self.user1.username,
                                                                        'slug': self.user1_skill.slug}))
        self.assertEqual(response.status_code, 200)

    def test_user_skill_update(self):
        """User can't update somebody's skill, only his own"""
        self.client.login(**self.user2_data)
        response = self.client.get(reverse('user-skill-update', kwargs={'username': self.user1.username,
                                                                        'slug': self.user1_skill.slug}))
        self.assertEqual(response.status_code, 403)

    def test_superuser_skill_update(self):
        """Superuser can update every skill"""
        self.client.login(**self.super_user_data)
        response = self.client.get(reverse('user-skill-update', kwargs={'username': self.super_user.username,
                                                                        'slug': self.user1_skill.slug}))
        self.assertEqual(response.status_code, 200)

    def test_user_own_skill_update(self):
        """User can update his own skill"""
        self.client.login(**self.user1_data)
        response = self.client.get(reverse('user-skill-update', kwargs={'username': self.user1.username,
                                                                        'slug': self.user1_skill.slug}))
        self.assertEqual(response.status_code, 200)

    def test_user_tag_update(self):
        """Ordinary user can't update skill tag"""
        self.client.login(**self.user1_data)
        response = self.client.get(reverse('skill-tag-update', kwargs={'slug': self.user1_tag.slug}))
        self.assertEqual(response.status_code, 403)

    def test_user_w_perm_tag_update(self):
        """User with permission can update skill tag"""
        self.client.login(**self.user_w_perms_data)
        self.user_w_perms.user_permissions.add(Permission.objects.filter(name='Can change skill tag').first())
        response = self.client.get(reverse('skill-tag-update', kwargs={'slug': self.user1_tag.slug}))
        self.assertEqual(response.status_code, 200)

    def test_superuser_tag_update(self):
        """Superuser can update skill tag"""
        self.client.login(**self.super_user_data)
        response = self.client.get(reverse('skill-tag-update', kwargs={'slug': self.user1_tag.slug}))
        self.assertEqual(response.status_code, 200)
