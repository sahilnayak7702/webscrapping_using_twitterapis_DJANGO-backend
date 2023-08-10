from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=450, null=True, blank=True)
    def __str__(self):
        return self.name

class Advocate(models.Model):
    # now we will create a relationship between companies and advocate
    # we will create one to many relationship
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=520, null=True, blank=True)
    profile_pic = models.CharField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=550, null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    # blank=True allows us to save the data without any data in it. means if the data is blank then it can be saved in Django

    def __str__(self):
        return self.username
