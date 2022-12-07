"""
Generate Schedule Controller.
"""
from rest_framework import status
from rest_framework.response import Response
from vesting.models import CompanyValuation, OptionGrant
from vesting.serializers import ScheduleSerializer, VestSerializer
from vesting.use_cases.generate_schedule.use_case import \
    GenerateScheduleUseCase


class GenerateScheduleController:
    """Controller for the generate schedule use case."""

    def __init__(self):
        self.generate_schedule_use_case = GenerateScheduleUseCase()

    def handle(self, request):
        """Handle the request."""

        schedule_serializer = ScheduleSerializer(data=request.data)

        if schedule_serializer.is_valid():
            option_grant_data = schedule_serializer.validated_data.pop(
                'option_grants')
            company_valuation_data = schedule_serializer.validated_data.pop(
                'company_valuations')

            company_valuation = CompanyValuation(**company_valuation_data[0])
            option_grant = OptionGrant(**option_grant_data[0])

            schedule = self.generate_schedule_use_case.execute(
                option_grant, company_valuation)

            vest_serializer = VestSerializer(schedule, many=True)
            return Response(vest_serializer.data, status=status.HTTP_200_OK)

        return Response(schedule_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
