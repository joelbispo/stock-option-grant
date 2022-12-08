"""
Generate a schedule of vesting events for a given grant of options.
"""
import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from vesting.models import CompanyValuation, OptionGrant, Vest

from app.shared.exceptions import BusinessValidationError


class GenerateScheduleUseCase:
    """ Generate a schedule of vesting events for a given grant of options."""

    def execute(self, option_grants: OptionGrant,
                company_valuations: CompanyValuation):
        """Execute the schedule generation."""

        return self._calculate_vests(option_grants, company_valuations)

    def _calculate_vests(self, option_grants: OptionGrant,
                         company_valuations: CompanyValuation) -> list[Vest]:
        """
        Calculate the vesting schedule for a given grant of options.
        """

        duration: int = option_grants.duration_months

        if option_grants.cliff_months > duration:
            raise BusinessValidationError(
                "Cliff must be less than or equal to duration.")

        if option_grants.start_date < company_valuations.valuation_date:
            raise BusinessValidationError(
                "Start date must be greater than or equal to valuation date."
            )

        vest_list: list[Vest] = []

        for index in range(0, duration + 1):

            calculated_vest: Vest = self.calculate_vest_of_a_month(
                option_grants.start_date,
                option_grants.cliff_months,
                duration,
                option_grants.quantity,
                company_valuations.price,
                index,
            )
            vest_list.append(calculated_vest)

        return vest_list

    @staticmethod
    def calculate_vest_of_a_month(
        start_date: datetime.date,
        cliff: int,
        duration: int,
        quantity: int,
        price: Decimal,
        month: int,
    ) -> Vest:
        """ Calculate the vesting of a month for a given grant of options."""
        current_date: datetime.date = start_date + \
            relativedelta(months=+(month))
        cliff_percentage: float = cliff / duration

        current_quantity: float = quantity * ((cliff_percentage + ((month / duration) - cliff_percentage)) * (((duration - cliff) + month) // duration))  # noqa
        current_value: Decimal = Decimal(current_quantity) * Decimal(price)

        return Vest(
            vested_quantity=current_quantity,
            total_value=current_value,
            date=current_date,
        )
