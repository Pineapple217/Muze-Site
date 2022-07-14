from distutils.command.upload import upload
from  PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import gettext as _

class Lid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, upload_to = 'images/profile/')

    date_of_birth = models.DateField()
    tel = models.CharField(max_length=50)

    GENDERS = [
        ('M', _('Male')),
        ('F', _('Female')),
        ('X', _('Other')),
    ]
    gender = models.CharField(max_length=1, choices=GENDERS)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10)
    zipcode = models.CharField(max_length=4)
    residence = models.CharField(max_length=200)

    discord_id = models.PositiveBigIntegerField()
    media = models.BooleanField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        if self.profile_picture:
            max_size = 500
            img = Image.open(self.profile_picture.path)
            img_width, img_height = img.size
            size = img_height if img_height < img_width else img_width
            new_img = img.crop(((img_width - size) // 2,
                         (img_height - size) // 2,
                         (img_width + size) // 2,
                         (img_height + size) // 2))
            if size > max_size:
                new_img = new_img.resize((max_size, max_size))
            new_img.save(self.profile_picture.path)


    class Meta:
        verbose_name_plural = "Leden"


