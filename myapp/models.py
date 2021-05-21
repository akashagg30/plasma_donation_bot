from django.core import validators
from django.db import models
from django.core.validators import RegexValidator

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    user_name = models.CharField(max_length=100, null=True)
    phone_number =  models.CharField(max_length=10, null=True)
    is_donor = models.BooleanField(default=False)
    is_beneficiary = models.BooleanField(default=False)
    state = models.IntegerField(default=1)


class Donor(models.Model):
    users = models.OneToOneField(Users, on_delete= models.CASCADE, primary_key= True)
    corona_positive_since = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=3)
    last_plasma_donation = models.DateField(null=True, blank=True)
    vaccination_date = models.DateField(null=True, blank=True)
    shown_time = models.DateTimeField(null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


class Beneficiary(models.Model):
    users = models.OneToOneField(Users, on_delete= models.CASCADE, primary_key= True)
    blood_group = models.CharField(max_length=3)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_interation = models.DateTimeField(auto_now=True)



