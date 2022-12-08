"""
Test the GenerateScheduleUseCase class.
"""
import datetime
from decimal import Decimal

from django.test import TestCase
from vesting.models import CompanyValuation, OptionGrant
from vesting.use_cases.generate_schedule.generate_schedule_use_case import \
    GenerateScheduleUseCase

from app.shared.exceptions import BusinessValidationError


class GenerateScheduleUseCaseTest(TestCase):
    """Test the GenerateScheduleUseCase class."""

    def setUp(self):
        self.__generate_schedule_use_case = GenerateScheduleUseCase()

    def test_generate_schedule_use_case(self):
        """Test the generate schedule use case."""

        # Arrange

        option_grant = OptionGrant(
            quantity=4800,
            start_date=datetime.date(2018, 1, 1),
            cliff_months=12,
            duration_months=48,
        )
        company_valuation = CompanyValuation(
            price=10.0, valuation_date=datetime.date(2017, 12, 9)
        )

        # Act

        result = self.__generate_schedule_use_case.execute(
            option_grant, company_valuation
        )

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

    def test_generate_schedule_use_case_with_invalid_start_date(self):
        """Test the generate schedule use case with invalid start date."""

        # Arrange
        option_grant = OptionGrant(
            quantity=4800,
            start_date=datetime.date(2017, 12, 9),
            cliff_months=12,
            duration_months=48,
        )
        company_valuation = CompanyValuation(
            price=10.0, valuation_date=datetime.date(2018, 12, 9)
        )

        # Act
        with self.assertRaises(BusinessValidationError):
            self.__generate_schedule_use_case.execute(
                option_grant, company_valuation)

    def test_generate_schedule_use_case_with_invalid_cliff(self):
        """Test the generate schedule use case with invalid cliff."""

        # Arrange
        option_grant = OptionGrant(
            quantity=4800,
            start_date=datetime.date(2018, 1, 1),
            cliff_months=49,
            duration_months=48,
        )
        company_valuation = CompanyValuation(
            price=10.0, valuation_date=datetime.date(2018, 12, 9)
        )

        # Act
        with self.assertRaises(BusinessValidationError):
            self.__generate_schedule_use_case.execute(
                option_grant, company_valuation)

    def test_generate_schedule_use_case_with_invalid_duration(self):
        """Test the generate schedule use case with invalid duration."""

        # Arrange
        option_grant = OptionGrant(
            quantity=4800,
            start_date=datetime.date(2018, 1, 1),
            cliff_months=12,
            duration_months=49,
        )
        company_valuation = CompanyValuation(
            price=10.0, valuation_date=datetime.date(2018, 12, 9)
        )

        # Act
        with self.assertRaises(BusinessValidationError):
            self.__generate_schedule_use_case.execute(
                option_grant, company_valuation)

    def test_given_cliff_equal_to_duration_when_execute_then_sucess(self):
        """Test the generate schedule use case with invalid duration."""

        # Arrange
        option_grant = OptionGrant(
            quantity=4800,
            start_date=datetime.date(2018, 1, 1),
            cliff_months=48,
            duration_months=48,
        )
        company_valuation = CompanyValuation(
            price=10.0, valuation_date=datetime.date(2017, 12, 9)
        )

        # Act
        result = self.__generate_schedule_use_case.execute(
            option_grant, company_valuation)

        # Assert

        # First month
        self.assertEqual(result[0].total_value, Decimal(0.00))
        self.assertEqual(result[0].date, datetime.date(2018, 1, 1))
        self.assertEqual(result[0].vested_quantity, 0)

        # Month 13
        self.assertEqual(result[12].total_value, Decimal(0.00))
        self.assertEqual(result[12].date, datetime.date(2019, 1, 1))
        self.assertEqual(result[12].vested_quantity, 0)

        # Month before last and cliff month
        self.assertEqual(result[47].total_value, Decimal(0.00))
        self.assertEqual(result[47].date, datetime.date(2021, 12, 1))
        self.assertEqual(result[47].vested_quantity, 0)

        # Last month and cliff month
        self.assertEqual(result[48].total_value, Decimal(48000.00))
        self.assertEqual(result[48].date, datetime.date(2022, 1, 1))
        self.assertEqual(result[48].vested_quantity, 4800)
