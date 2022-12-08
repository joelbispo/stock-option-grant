"""
Test the Vesting API.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

VESTING_SCHEDULE_URL = reverse("vesting:schedule")


class VestingAPITestCase(TestCase):
    """Test the Vesting API."""

    def setUp(self):
        """Set up the test case."""

        self.__client = APIClient()

    def test_given_valid_payload_when_generate_schedule_then_success(self):
        """Test the generate schedule success scenario."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "01-01-2018",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "09-12-2017"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 49)

    def test_given_no_payload_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when no payload."""
        # Act
        response = self.__client.post(VESTING_SCHEDULE_URL)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_get_method_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when GET request method."""
        # Act
        response = self.__client.get(VESTING_SCHEDULE_URL)

        # Assert
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_given_put_method_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when PUT request method."""
        # Act
        response = self.__client.put(VESTING_SCHEDULE_URL)

        # Assert
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_given_delete_method_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when DELETE request method."""
        # Act
        response = self.__client.delete(VESTING_SCHEDULE_URL)

        # Assert
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_given_patch_method_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when PATCH request method."""
        # Act
        response = self.__client.patch(VESTING_SCHEDULE_URL)

        # Assert
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_given_head_method_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when HEAD request method."""
        # Act
        response = self.__client.head(VESTING_SCHEDULE_URL)

        # Assert
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_given_invalid_payload_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when invalid payload."""
        # Act
        response = self.__client.post(VESTING_SCHEDULE_URL, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_invalid_option_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when invalid option grants."""
        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, {"option_grants": []}, format="json"
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_invalid_company_val_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when invalid company valuations."""
        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, {"company_valuations": []}, format="json"
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class VestingAPIValidationTestCase(TestCase):
    """Test the Vesting API data validation."""

    def setUp(self):
        """Set up the test case."""

        self.__client = APIClient()

    def test_given_invalid_date_format_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when invalid date format."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_no_option_grants_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when option grants is missing."""

        # Arrange
        payload = {
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ]
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_no_company_val_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when company is missing."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_price_zero_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when valuation price is zero."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": 0.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_price_negative_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when valuation price is negative."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": -1.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_quantity_is_zero_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when option quantity is zero."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 0,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_quantity_negative_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when option quantity is negative."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": -1,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_cliff_negative_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when cliff months is negative."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": -1,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_duration_negative_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when duration months is negative."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": -1,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_duration_zero_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when duration months is zero."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 0,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_cliff_bigger_duration_when_generate_then_fails(self):
        """Test generate fails when cliff is bigger than duration."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 48,
                    "duration_months": 12,
                }
            ],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_option_grants_empty_when_generate_schedule_then_fails(self):
        """Test the generate schedule fails when option grants is empty."""

        # Arrange
        payload = {
            "option_grants": [],
            "company_valuations": [
                {
                    "price": 10.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_company_empty_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when company empty."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_given_price_less_zero_when_generate_schedule_then_fails(self):
        """Test generate schedule fails when price is less than zero."""

        # Arrange
        payload = {
            "option_grants": [
                {
                    "quantity": 4800,
                    "start_date": "2018-01-01",
                    "cliff_months": 12,
                    "duration_months": 48,
                }
            ],
            "company_valuations": [
                {
                    "price": -1.0,
                    "valuation_date": "2017-01-01"
                }
            ],
        }

        # Act
        response = self.__client.post(
            VESTING_SCHEDULE_URL, payload, format="json")

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
