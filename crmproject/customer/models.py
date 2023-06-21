from django.db import models
from django.contrib.auth.models import AbstractUser
from customer.manager import CustomManager

class UserTable(AbstractUser):
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    mob = models.IntegerField(default=0)    
    password = models.CharField(max_length=15)
    object_manager = CustomManager()

    def __str__(self):
        return str(self.email)

class Customer(models.Model):
    company_name = models.CharField(max_length=200, blank = True,null = True)
    address = models.CharField(max_length=300,blank = True, null = True)

    def __str__(self):
        return str(self.company_name)

class Representatives(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)

    def __str__(self):
        return str(self.name)

class VendorsInsights(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    prev_date = models.DateField(widget=forms.DateInput(format='%d-%m-%Y'),blank = True,null= True)
    current_date = models.DateField(blank = True, null = True)
    next_date = models.DateField(blank = True, null = True)

    def __str__(self):
        return str(self.current_date)

class VendorsMailSent(models.Model):
    represent = models.ForeignKey(Representatives, on_delete=models.CASCADE)
    subject = models.CharField(max_length=300, blank = True, null = True)
    body = models.CharField(max_length=1000, blank = True, null = True) 

    def __str__(self):
        return str(self.represent)