from ast import mod
import email
from os import name
from pyexpat import model
from re import A
from django.db import models
from django.contrib.auth.models import User

class user(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

class data1(models.Model):
    H_CDR1 = models.CharField(max_length=100)
    H_CDR2 = models.CharField(max_length=100)
    H_CDR3 = models.CharField(max_length=100)
    L_CDR1 = models.CharField(max_length=100)
    L_CDR2 = models.CharField(max_length=100)
    L_CDR3 = models.CharField(max_length=100)
    Epitope = models.CharField(max_length=515)
    Description = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"data1 object: {self.H_CDR1}, {self.H_CDR2}, {self.H_CDR3}, {self.L_CDR1}, {self.L_CDR2}, {self.L_CDR3}, {self.Epitope}"


class output(models.Model):
    result = models.BooleanField()

    def __str__(self):
        return self.name
    
class data2(models.Model):
    Type = models.CharField(max_length=1)
    CDR = models.CharField(max_length=1)
    BWindow = models.CharField(max_length=9)
    AWindow = models.CharField(max_length=9, null=True)
    BSol = models.CharField(max_length=100)
    ASol = models.CharField(max_length=100)
    BSec = models.CharField(max_length=100)
    ASec = models.CharField(max_length=100)
    Description = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return f"data2 object: {self.Type}, {self.CDR}, {self.BWindow}, {self.BSol}, {self.ASol}, {self.BSec}, {self.ASec}"
    
class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction_date = models.DateTimeField(auto_now_add=True)
    input_data = models.TextField()  # You can change this to store your specific input data structure
    prediction_result = models.CharField(max_length=10)  # Adjust the max_length as needed
    Description = models.TextField(null=True, blank=True)  # Add this line

    def __str__(self):
        return f"{self.user.username} - {self.prediction_result} on {self.prediction_date}"