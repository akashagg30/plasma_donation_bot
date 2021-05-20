from django.core import validators
from django.db import models
from django.core.validators import RegexValidator

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    is_donor = models.BooleanField(default=False)
    can_donate = models.BooleanField(default=False)
    is_benificiary = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    user_name = models.CharField(max_length=100, null=True)
    state = models.IntegerField(default=1)


class Donor(models.Model):
    users = models.OneToOneField(Users, on_delete= models.CASCADE, primary_key= True)
    corona_positive_since = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=3)
    last_plasma_donation = models.DateField(null=True, blank=True)
    vaccination_date = models.DateField(null=True, blank=True)

    phone_number =  models.CharField(max_length=10, blank=False, null=False)
    action_time = models.DateTimeField(auto_now=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


# class beneficiary(models.Model):
#     blood_group 
#     phone_number
#     loccation
#     Name
#     last_interation



