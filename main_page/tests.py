from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Producers
from .serializers import ProducersSerializer


class TestViews(TestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('On this page you can explore our rich collection of wall materials',
                      response.content.decode())

    def test_materials(self):
        response = self.client.get('/api/wall/materials/')
        self.assertEqual(response.status_code, 200)


class TestProducersUpdate(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.producer = Producers.objects.create(name='Test Producer',
                                                 country='Test Country',
                                                 address='Test Address',
                                                 phone='+123456789123',
                                                 foundation_year='2000')

    def test_update_producer(self):
        url = reverse('producer-update', args=[self.producer.pk])
        data = {
            'name': 'Updated Producer',
            'country': 'Updated Country',
            'address': 'Updated Address',
            'phone': '+963258741258',
            'foundation_year': '2010'

        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.producer.refresh_from_db()
        self.assertEqual(self.producer.name, 'Updated Producer')
        self.assertEqual(self.producer.country, 'Updated Country')
        self.assertEqual(self.producer.address, 'Updated Address')
        self.assertEqual(self.producer.phone, '+963258741258')
        self.assertEqual(self.producer.foundation_year, '2010')
        self.assertEqual(response.data, ProducersSerializer(self.producer).data)
