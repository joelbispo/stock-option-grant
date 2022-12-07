"""
Test the GenerateScheduleUseCase class.
"""
import datetime
from decimal import Decimal

from django.test import TestCase
from vesting.models import CompanyValuation, OptionGrant
from vesting.use_cases.generate_schedule.use_case import \
    GenerateScheduleUseCase


class GenerateScheduleUseCaseTest(TestCase):
    """Test the GenerateScheduleUseCase class."""

    def setUp(self):
        self.__generate_schedule_use_case = GenerateScheduleUseCase()

    def test_generate_schedule_use_case(self):
        """Test the generate schedule use case."""

        # Arrange

        option_grant = OptionGrant(quantity=4800, start_date=datetime.date(
            2018, 1, 1), cliff_months=12, duration_months=48)
        company_valuation = CompanyValuation(
            price=10.0, valuation_date=datetime.date(2017, 12, 9))

        # Act

        result = self.__generate_schedule_use_case.execute(
            option_grant, company_valuation)

        # Assert
        self.assertEqual(option_grant.duration_months + 1, len(result))

        # First month
        self.assertEqual(result[0].total_value, Decimal(0.00))
        self.assertEqual(result[0].date, datetime.date(2018, 1, 1))
        self.assertEqual(result[0].vested_quantity, 0)

        # Cliff month
        self.assertEqual(result[12].total_value, Decimal(12000.00))
        self.assertEqual(result[12].date, datetime.date(2019, 1, 1))
        self.assertEqual(result[12].vested_quantity, 1200)

        # Last month
        self.assertEqual(result[48].total_value, Decimal(48000.00))
        self.assertEqual(result[48].date, datetime.date(2022, 1, 1))
        self.assertEqual(result[48].vested_quantity, 4800)