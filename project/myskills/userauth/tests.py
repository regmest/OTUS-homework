from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from selenium.webdriver import Firefox


class TestUserauth(TestCase):

    @classmethod
    def setUpClass(cls):
        """Setting user"""
        super().setUpClass()
        cls.user_data = {'username': 'testuser', 'password': 'testpass'}
        cls.user = get_user_model().objects.create_user(**cls.user_data)

    def test_user_force_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(**self.user_data)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertTrue(response.context['user'], self.user)

    def test_user_login_process(self):
        """Imitating real login process"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertIn('form', response.context)

        response = self.client.post('/accounts/login/', data=self.user_data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

    def test_user_skill_create_login_redirect(self):
        """Only logged users can create skills"""
        response = self.client.get(reverse('skill-create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(**self.user_data)

        response = self.client.get(reverse('skill-create'))
        self.assertEqual(response.status_code, 200)

    def test_user_tag_create_login_redirect(self):
        """Only logged users can create tags"""
        response = self.client.get(reverse('skill-tag-create'))
        self.assertEqual(response.status_code, 302)

        self.client.login(**self.user_data)

        response = self.client.get(reverse('skill-tag-create'))
        self.assertEqual(response.status_code, 200)


class TestUserauthWithWebdriver(TestCase):

    def setUp(self):
        self.driver = Firefox(executable_path='/Users/reginameshkova/Desktop/mine/geckodriver')

    def test_login_title(self):
        self.driver.get("http://localhost:8000/accounts/login/")
        self.assertEqual("Myskills" in self.driver.title, True)

    def tearDown(self):
        self.driver.quit()



