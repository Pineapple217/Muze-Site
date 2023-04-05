from django.shortcuts import get_object_or_404
from django_ical.views import ICalFeed

from leden.models import Lid

from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


class ShiftFeed(ICalFeed):
    """
    A simple event calender
    """

    product_id = "-//example.com//Example//EN"
    timezone = "UTC"
    file_name = "event.ics"

    def items(self):
        lid = get_object_or_404(Lid, ical_token=self.ical_token)
        return lid.shift_set.all()

    def item_guid(self, item):
        return "{}{}".format(item.id, get_current_site(self.request))

    def item_title(self, item):
        return "Shiften in De Muze"
        # return "{}".format(str(item))

    def item_description(self, item):
        desc = ""
        desc += f"{self.request.scheme}://{get_current_site(self.request)}{item.shift_list.get_absolute_url()}\n"
        desc += f"Shifters:\n"
        for l in item.shifters.all():
            desc += f"   {str(l)}\n"
        desc += f"({item.shifters.count()}/{item.max_shifters})"
        return desc

    def timezone(self, item):
        return settings.TIME_ZONE

    def item_attendee(self, item):
        return "Jules ;)"

    def item_start_datetime(self, item):
        return item.get_start_datetime()

    def item_end_datetime(self, item):
        return item.get_end_datetime()

    def item_link(self, item):
        return f"{self.request.scheme}://{get_current_site(self.request)}{item.shift_list.get_absolute_url()}"

    def __call__(self, request, ical_token, *args, **kwargs):
        self.ical_token = ical_token
        self.request = request
        return super(ShiftFeed, self).__call__(request, *args, **kwargs)
