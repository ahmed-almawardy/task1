from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase

from core.models import WorkShift, Days


class ShiftTest(TestCase):
    def test_create_shift_closes_next_day(self):
        data = {
            'day': Days.FRIDAY.value,
            'opening_time': 64800,
            'closing_time': 3600,
        }
        shift = WorkShift.objects.create(**data)
        self.assertEqual(data['day'], shift.day)
        self.assertEqual(data['opening_time'], shift.opening_time)
        self.assertEqual(data['closing_time'], shift.closing_time)

    def test_create_shift_closes_same_day(self):
        data = {
            'day': Days.FRIDAY.value,
            'opening_time': 32400,
            'closing_time': 39600,
        }
        shift = WorkShift.objects.create(**data)
        self.assertEqual(data['day'], shift.day)
        self.assertEqual(data['opening_time'], shift.opening_time)
        self.assertEqual(data['closing_time'], shift.closing_time)



class WorkShiftAPITest(APITestCase):
    def test_create_shift_with_same_day(self):
        data = {
        "friday" : [
            {
            "type" : "open",
            "value" : 32400
            },
            {
            "type": "close",
            "value": 64800
            }
        ],
        "saturday": [
            {
            "type" : "open",
            "value" : 32400
            },
            {
            "type" : "close",
            "value" : 39600
            },
            {
            "type" : "open",
            "value" : 57600
            },
            {
            "type" : "close",
            "value" : 82800
            }
        ]
        }
        url = reverse('core:shift-create')
        response = self.client.post(data=data, path=url, format='json')
        expected = 'Friday: 09:00:00 AM - 06:00:00 PM\nSaturday: 09:00:00 AM - 11:00:00 AM, 04:00:00 PM - 11:00:00 PM'
        self.assertContains(response, expected)

    def test_create_shift_with_dayoff(self):
        data = {
        "friday" : [],
        "saturday": [
            {
            "type" : "open",
            "value" : 32400
            },
            {
            "type" : "close",
            "value" : 39600
            },
            {
            "type" : "open",
            "value" : 57600
            },
            {
            "type" : "close",
            "value" : 82800
            }
        ]
        }
        url = reverse('core:shift-create')
        response = self.client.post(data=data, path=url, format='json')
        expected = 'Friday: Closed\nSaturday: 09:00:00 AM - 11:00:00 AM, 04:00:00 PM - 11:00:00 PM'
        self.assertContains(response, expected)


    def test_create_shift_notsame_day(self):
        data = {
        "friday" : [
            {
            "type" : "open",
            "value" : 64800
            }
        ],
        "saturday": [
            {
            "type" : "close",
            "value" : 3600
            },
            {
            "type" : "open",
            "value" : 54800
            },
        ],
        "sunday": [
            {
            "type" : "close",
            "value" : 2800
            },
            {
            "type" : "open",
            "value" : 57600
            },
            {
            "type" : "close",
            "value" : 82800
            }
        ]
        }
        url = reverse('core:shift-create')
        response = self.client.post(data=data, path=url, format='json')
        expected = 'Friday: 06:00:00 PM - 01:00:00 AM\nSaturday: 03:13:20 PM - 12:46:40 AM\nSunday: 04:00:00 PM - 11:00:00 PM'
        self.assertContains(response, expected)