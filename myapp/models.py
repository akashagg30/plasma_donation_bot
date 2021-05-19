from django.core import validators
from django.db import models
from django.core.validators import RegexValidator

blood_group_list =  (
                        ("A", "A"),
                        ('B', 'B'),
                    )

class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    is_donner = models.BooleanField(default=False)
    is_benificiary = models.BooleanField(default=False)
    name = models.CharField(max_length=100, null=True)
    user_name = models.CharField(max_length=100, null=True)
    state = models.IntegerField(default=1)


class Donner(models.Model):
    users = models.OneToOneField(Users, on_delete= models.CASCADE, primary_key= True)
    corona_positive_since = models.DateTimeField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, choices=blood_group_list)
    last_plasma_donation = models.DateTimeField(null=True, blank=True)
    vaccination_date = models.DateTimeField(null=True, blank=True)

    phone_number =  models.CharField(max_length=10, blank=False, null=False, 
                        validators = [
                            RegexValidator( regex=r'^d{10}$', 
                                            message="Phone number must be entered in the format: '9999999999'. only 10 digits are allowed."
                                        )
                        ]
                    )
    action_time = models.DateTimeField(auto_now=True)
    # location = 


# class beneficiary(models.Model):
#     blood_group 
#     phone_number
#     loccation
#     Name
#     last_interation



