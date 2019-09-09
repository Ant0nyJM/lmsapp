from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    def __str__(self):
        return self.book_name
    class Meta():
        permissions = [
            ('can_change','Can view, edit, delete or add books'),
        ]
        
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=50)
    book_edition = models.CharField(max_length=50)
    book_genre = models.CharField(max_length=50)
    book_issued = models.BooleanField(default=False)
    book_issuer = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)