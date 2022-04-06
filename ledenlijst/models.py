from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.
class Lid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # naam = models.CharField(max_length=100)
    # voornaam = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    tel = models.CharField(max_length=50)

    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Other'),
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

    class Meta:
        verbose_name_plural = "Leden"
    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Lid.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instace, **kwargs):
    #     instace.profile.save()
