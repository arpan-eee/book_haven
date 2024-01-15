from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, related_name="account",on_delete=models.CASCADE)
    book = models.ManyToManyField(Book, related_name="accounts", blank=True)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    since = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
    
class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    borrowed_time = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return f'{self.book.title} - {self.user.user.username}'
    
class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.time}'
    
        
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)




