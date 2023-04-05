from django_ical.views import ICalFeed

from .models import Shift

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


class ShiftFeed(ICalFeed):
    """
    A simple event calender
    """

    product_id = "-//example.com//Example//EN"
    timezone = "UTC"
    file_name = "event.ics"

    def items(self):
        return self.request.user.lid.shift_set.all()

    def item_guid(self, item):
        return "{}{}".format(item.id, "global_name")

    def item_title(self, item):

        return "{}".format(str(item))

    def item_description(self, item):
        print(self.request.scheme)
        print(get_current_site(self.request))
        return f"{self.request.scheme}://{get_current_site(self.request)}{item.shift_list.get_absolute_url()}"

    def item_start_datetime(self, item):
        return item.get_start_datetime()

    def item_end_datetime(self, item):
        return item.get_end_datetime()

    def item_link(self, item):
        print(self.request.scheme)
        print(get_current_site(self.request))
        return f"{self.request.scheme}://{get_current_site(self.request)}{item.shift_list.get_absolute_url()}"

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super(ShiftFeed, self).__call__(request, *args, **kwargs)
