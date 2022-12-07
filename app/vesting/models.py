"""
Models for the vesting app.
"""


class CompanyValuation(object):
    """A valuation of the company."""

    def __init__(self, price, valuation_date):
        self.price = price
        self.valuation_date = valuation_date


class Vest(object):
    """A vesting event."""

    def __init__(self, vested_quantity, total_value, date):
        self.vested_quantity = vested_quantity
        self.total_value = total_value
        self.date = date


class OptionGrant(object):
    """A grant of options to an employee."""

    def __init__(self, quantity, start_date, cliff_months, duration_months):
        self.quantity = quantity
        self.start_date = start_date
        self.cliff_months = cliff_months
        self.duration_months = duration_months


class Schedule(object):
    """A schedule of vesting events."""

    def __init__(self, option_grants, company_valuations, vests):
        self.option_grants = option_grants
        self.company_valuations = company_valuations
        self.vests = vests
