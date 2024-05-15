from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact'

# class Cases(models.Model):
#     name = models.CharField(max_length=100)
#     message = models.TextField()
#     court = models.TextField()
#     judge = models.TextField()
   
#     class Meta:
#         db_table = 'cases'