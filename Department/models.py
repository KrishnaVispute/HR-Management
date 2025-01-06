from django.db import models

# Create your models here.
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  
    role_name = models.CharField(max_length=100) 
    description = models.CharField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=True)

    def _str_(self):
        return self.role_name