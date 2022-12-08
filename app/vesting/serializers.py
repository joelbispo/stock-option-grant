"""
Serializers for the vesting app.
"""
from rest_framework import serializers


class CompanyValuationSerializer(serializers.Serializer):
    """Company Valuation Serializer."""

    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    valuation_date = serializers.DateField(
        input_formats=['%d-%m-%Y'], format='%d-%m-%Y')

    def validate(self, data: dict) -> dict:
        """Validate the data."""
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return data


class VestSerializer(serializers.Serializer):
    """Vest Serializer."""

    vested_quantity = serializers.IntegerField()
    total_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField(input_formats=['%d-%m-%Y'],
                                 format='%d-%m-%Y')

    def validate(self, data: dict) -> dict:
        """Validate the data."""

        if data['vested_quantity'] < 0:
            raise serializers.ValidationError(
                "Vested quantity must be greater than or equal to 0.")

        if data['total_value'] < 0:
            raise serializers.ValidationError(
                "Total value must be greater than or equal to 0.")
        return data


class OptionGrantSerializer(serializers.Serializer):
    """Option Grant Serializer."""

    quantity = serializers.IntegerField()
    start_date = serializers.DateField(input_formats=['%d-%m-%Y'],
                                       format='%d-%m-%Y')
    cliff_months = serializers.IntegerField()
    duration_months = serializers.IntegerField()

    def validate(self, data: dict) -> dict:
        """Validate the data."""

        if data['quantity'] <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than 0.")

        if data['cliff_months'] < 0:
            raise serializers.ValidationError(
                "Cliff months must be greater than or equal to 0.")

        if data['cliff_months'] > data['duration_months']:
            raise serializers.ValidationError(
                "Cliff months must be less than or equal to duration months.")

        if data['duration_months'] <= 0:
            raise serializers.ValidationError(
                "Duration months must be greater than 0.")

        return data


class OptionCompanyValuationSerializer(serializers.Serializer):
    """ Option Grant and Company Valuation Serializer."""

    option_grants = OptionGrantSerializer(many=True, required=True)
    company_valuations = CompanyValuationSerializer(many=True, required=True)

    def validate(self, data: dict) -> dict:
        """Validate the data."""

        if len(data['option_grants']) != 1:
            raise serializers.ValidationError(
                "Only one option grant must be provided.")
        if len(data['company_valuations']) != 1:
            raise serializers.ValidationError(
                "Only one company valuation must be provided.")
        return data
