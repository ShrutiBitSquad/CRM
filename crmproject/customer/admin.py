from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Representatives)
admin.site.register(Customer)
admin.site.register(VendorsInsights)
admin.site.register(VendorsMailSent)