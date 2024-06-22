from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import check_password

class User(AbstractUser):
    # Common fields
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)  
    date_joined = models.DateTimeField(auto_now_add=True)
    school = models.CharField(max_length=50 , default= None)


    dept = models.CharField(max_length=50 , default= None)
    facility = models.CharField(max_length=50 , default= None)
    
    # Custom fields for different user types
    is_GMAadmin = models.BooleanField('Is GMAadmin', default=False)
    is_SYSadmin = models.BooleanField('Is SYSadmin', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    is_superadmin = models.BooleanField('Is superadmin' , default=False)
    hname = models.CharField(max_length=20, default= None )

    UID = models.CharField(max_length=10, default=None)
    HID = models.CharField(max_length=20, blank=True, null=True)  


    def __str__(self):
        return self.username

    @classmethod
    def authenticate(cls, request, email, password):
        try:
            user = cls.objects.get(email=email)

            # Check the user's password
            if check_password(password, user.password):
                return user
        except cls.DoesNotExist:
            pass
        return None



class Ticket(models.Model):
    TID = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    hname = models.CharField(max_length=20, default= None )
    uname = models.CharField(max_length=20, default= None )
    status = models.CharField(max_length=20, default= 'Sent' )
    hreason = models.CharField(max_length=20, default= None )
    time = models.CharField(max_length=20, default= '24' )
    dept = models.CharField(max_length=50 , default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    facilities = models.CharField(max_length= 10, default=None)
    UID = models.CharField(max_length=20, default=' ')
    HID = models.CharField(max_length=10 , default=' ')

    def __str__(self):
        return self.TID