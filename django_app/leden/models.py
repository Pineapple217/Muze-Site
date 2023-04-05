from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _l
from datetime import datetime, time, timedelta
from django.db.models import Q

from simple_history.models import HistoricalRecords
from simple_history import register

from constance import config


register(User)


def file_size(value):  # add this to some file where you can import it from
    max_pp_size_mb = config.PP_MAX_SIZE_MB
    limit = max_pp_size_mb * 1024 * 1024
    if value.size > limit:
        raise ValidationError(
            _("File too large. Size should not exceed %(max)s MB.")
            % {"max": max_pp_size_mb}
        )


class Lid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="images/profile/", validators=[file_size]
    )

    date_of_birth = models.DateField()
    tel = models.CharField(max_length=50)

    GENDERS = [
        ("M", _l("Male")),
        ("F", _l("Female")),
        ("X", _l("Other")),
    ]
    gender = models.CharField(max_length=1, choices=GENDERS)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=4)
    residence = models.CharField(max_length=200)

    discord_id = models.PositiveBigIntegerField(null=True, blank=True)
    media = models.BooleanField()

    is_accepted = models.BooleanField(default=False)

    history = HistoricalRecords()

    def is_available(self, shift) -> bool:
        def is_next_day(time_s) -> bool:
            return time(config.NEXT_DAY_BREAKPOINT, 0, 0) > time_s > time(0, 0, 0)

        start = shift.get_start_datetime()
        end = shift.get_end_datetime()
        shift_range = (start, end)
        avail = self.onbeschikbaar_set.filter(
            Q(start__lte=shift.date) & Q(end__gte=shift.date)
        )
        if avail:
            return False

        avail_rep = self.onbeschikbaarherhalend_set.filter(
            Q(start_period__lte=start) & Q(end_period__gte=end)
        )
        if avail_rep:
            for a in avail_rep:
                if shift.date.isoweekday() == a.weekday:
                    avail_start = datetime.combine(
                        shift.date + timedelta(days=1)
                        if is_next_day(a.start)
                        else shift.date,
                        a.start,
                    )
                    avail_end = datetime.combine(
                        shift.date + timedelta(days=1)
                        if is_next_day(a.end)
                        else shift.date,
                        a.end,
                    )
                    if not (
                        (avail_end <= shift_range[0]) or (avail_start >= shift_range[1])
                    ):
                        return False
        return True

    def save(self, *args, **kwargs):
        super().save()

        if self.profile_picture:
            max_size = 500
            img = Image.open(self.profile_picture.path)
            img_width, img_height = img.size
            size = img_height if img_height < img_width else img_width
            new_img = img.crop(
                (
                    (img_width - size) // 2,
                    (img_height - size) // 2,
                    (img_width + size) // 2,
                    (img_height + size) // 2,
                )
            )
            if size > max_size:
                new_img = new_img.resize((max_size, max_size))
            new_img.save(self.profile_picture.path)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        verbose_name_plural = "Leden"

        permissions = [
            ("accept_lid", _("Can add new members who applied for membership"))
        ]
