"""
Test the Vesting API.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

VESTING_SCHEDULE_URL = reverse('vesting:schedule')


class VestingAPITestCase(TestCase):
    """Test the Vesting API."""

    def setUp(self):
        """Set up the test case."""

        self.__client = APIClient()

    def test_given_valid_payload_when_generate_schedule_then_success(self):
        """Test the generate schedule success scenario."""

        # Arrange
        payload = {
            'option_grants': [{
                'quantity': 4800,
                'start_date': '01-01-2018',
                'cliff_months': 12,
                'duration_months': 48
            }],
            'company_valuations': [{
                'price': 10.0,
                'valuation_date': '09-12-2017'
            }]
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 49)

    def test_given_invalid_date_format_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when invalid date format."""

        # Arrange
        payload = {
            'option_grants': [{
                'quantity': 4800,
                'start_date': '2018-01-01',
                'cliff_months': 12,
                'duration_months': 48
            }],
            'company_valuations': [{
                'price': 10.0,
                'valuation_date': '2017-01-01'
            }]
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_no_option_grants_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when option grants is missing."""

        # Arrange
        payload = {
            'company_valuations': [{
                'price': 10.0,
                'valuation_date': '2017-01-01'
            }]
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_no_company_val_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when company is missing."""

        # Arrange
        payload = {
            'option_grants': [{
                'quantity': 4800,
                'start_date': '2018-01-01',
                'cliff_months': 12,
                'duration_months': 48
            }],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format='json')

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
