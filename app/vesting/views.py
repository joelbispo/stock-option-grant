
from rest_framework import viewsets
from vesting.serializers import OptionCompanyValuationSerializer
from vesting.use_cases.generate_schedule.generate_schedule_controller import \
    GenerateScheduleController


class ScheduleViewSet(viewsets.ViewSet):
    """
    API endpoint that allows schedules to be viewed or edited.
    """
    serializer_class = OptionCompanyValuationSerializer

    def create(self, request):
        """
        Retrieve a schedule.
        """
        return GenerateScheduleController().handle(request)
