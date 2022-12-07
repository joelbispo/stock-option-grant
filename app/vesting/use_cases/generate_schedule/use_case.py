from decimal import Decimal

from dateutil.relativedelta import relativedelta
from vesting.models import CompanyValuation, OptionGrant, Vest


class GenerateScheduleUseCase:

    def execute(self, option_grants: OptionGrant,
                company_valuations: CompanyValuation):
        """
        Generate a schedule of vesting events for a given grant of options.
        """

        return self._calculate_vests(option_grants, company_valuations)

    def _calculate_vests(self, option_grants: OptionGrant,
                         company_valuations: CompanyValuation):
        """
        Calculate the vesting schedule for a given grant of options.
        """

        cliff = option_grants.cliff_months
        duration = option_grants.duration_months
        cliff_percentage = cliff / duration

        start_date = option_grants.start_date

        vest_list = []

        for index in range(0, duration+1):

            current_date = start_date + \
                relativedelta(months=+(index))

            current_quantity = option_grants.quantity * ((
                cliff_percentage +
                ((index/duration) - cliff_percentage)
            ) * (((duration-cliff) + index) // duration))

            current_value = Decimal(current_quantity) * \
                Decimal(company_valuations.price)
            vest_list.append(Vest(vested_quantity=current_quantity,
                             total_value=current_value, date=current_date))
        return vest_list
