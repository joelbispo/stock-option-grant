
from rest_framework import viewsets
from vesting.serializers import OptionCompanyValuationSerializer
from vesting.use_cases.generate_schedule.controller import \
    GenerateScheduleController


class ScheduleViewSet(viewsets.ViewSet):
    """
    API endpoint that allows schedules to be viewed or edited.
    """
    serializer_class = OptionCompanyValuationSerializer

    def retrieve(self, request, pk=None):
        """
        Retrieve a schedule.
        """
        return GenerateScheduleController().handle(request)
