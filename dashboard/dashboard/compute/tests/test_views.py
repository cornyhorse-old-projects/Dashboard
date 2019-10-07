import pytest
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

pytestmark = pytest.mark.django_db


class TestNetwork(TestCase):
    url = reverse('add_network')
    post_data_network1 = {
        'network_name': 'Network010',
        'network_description': 'Description of Network1',
        'located_in_cloud': True
    }
    post_data_network2 = {
        'network_name': 'Network020',
        'network_description': 'Description of Network2',
        'located_in_cloud': True
    }

    def test_create_two_network_per_user(self):
        self.client.force_login(User.objects.create_user(username='foobar', password='password'))
        response_for_network1 = self.client.post(self.url, self.post_data_network1)
        response_for_network2 = self.client.post(self.url, self.post_data_network2)

        home_page = self.client.get(reverse('networkResources'))

        self.assertEqual(response_for_network1.status_code, 302)
        self.assertEqual(response_for_network2.status_code, 302)
        self.assertRedirects(response_for_network1, reverse('networkResources'))
        self.assertRedirects(response_for_network2, reverse('networkResources'))
        self.assertContains(home_page, 'Network010')
        self.assertContains(home_page, 'Network020')

