"""
Serializers for the vesting app.
"""
from rest_framework import serializers


class CompanyValuationSerializer(serializers.Serializer):
    """A valuation of the company."""
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    valuation_date = serializers.DateField(
        input_formats=['%d-%m-%Y'], format='%d-%m-%Y')


class VestSerializer(serializers.Serializer):
    """A vesting event."""
    vested_quantity = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField(
        input_formats=['%d-%m-%Y'], format='%d-%m-%Y')


class OptionGrantSerializer(serializers.Serializer):
    """A grant of options to an employee."""
    quantity = serializers.IntegerField()
    start_date = serializers.DateField(
        input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
    cliff_months = serializers.IntegerField()
    duration_months = serializers.IntegerField()


class ScheduleSerializer(serializers.Serializer):
    """A schedule of vesting events."""
    option_grants = OptionGrantSerializer(many=True, required=True)
    company_valuations = CompanyValuationSerializer(many=True, required=True)
    vests = VestSerializer(many=True, required=False)
