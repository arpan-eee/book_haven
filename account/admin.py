from django.contrib import admin
from .models import Account,Borrow,Comment

# Register your models here.

admin.site.register(Account)
admin.site.register(Borrow)
admin.site.register(Comment)