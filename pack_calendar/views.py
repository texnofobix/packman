from django.utils import timezone
from django.views.generic import ListView, DetailView

from membership.mixins import ActiveMemberOrContributorTest

from .models import Event


class EventListView(ActiveMemberOrContributorTest, ListView):
    """
    Display a listing of all the events coming up
    """
    model = Event
    paginate_by = 10
    context_object_name = 'event_list'

    def get_queryset(self):
        """
        Return a queryset containing all events for the next 6 months
        """
        return Event.objects.filter(start__lte=timezone.now() + timezone.timedelta(weeks=26)).filter(
            start__gte=timezone.now()).order_by('start')


class EventDetailView(ActiveMemberOrContributorTest, DetailView):
    """
    Display the details of a specific event
    """
    model = Event
