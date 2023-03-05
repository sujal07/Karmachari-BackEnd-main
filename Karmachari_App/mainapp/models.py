from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from django.utils.html import mark_safe

User=get_user_model()

# Create your models here.
# deparment= (
#         ('BCT','BCT'),
#         ('BCE', 'BCE'),
#         ('BEX','BEX')
#     )

class Department(models.Model):
    name = models.CharField(max_length=100, default="Everyone", null=True)
    # Post = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userID = uuid.uuid4()
    profileimg = models.ImageField(upload_to='profile_images',default='img.png')
    dob = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, default=0)
    def __str__(self):
        return self.user.username
    
    def img_preview(self): #new
        return mark_safe(f'<img src = "{self.profileimg.url}" width = "300"/>')
    
class Notice(models.Model):
    title = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    context = models.TextField(max_length=100000, null=True)        
    def __str__(self):
        return self.title

class Leaves(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    leave_condn = (
        ('Sick Leave','Sick Leave'),
        ('Vacation','Vacation'),
        ('Emergency','Emergency')
    )
    leave_permission = (
        ('Approved','Approved'),
        ('Pending','Pending'),
        ('Not Approved','Not Approved')
    )
    subject = models.CharField(max_length=100, null=True)
    date = models.DateField(default=timezone.now)
    duration = models.DateField(default=timezone.now)
    leave_type = models.CharField(max_length=100, null=True,choices= leave_condn)
    message = models.TextField(max_length=100000, null=True)
    status = models.CharField(max_length=100, choices= leave_permission, default='Pending')
    def __str__(self):
        return self.subject
    
# class Calendar(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     dateOfQuestion = models.DateField(null=True)
#     checkInTime = models.DateTimeField(auto_now_add=True)
#     checkOutTime = models.DateTimeField(auto_now_add=True)
#     overtime = models.DateTimeField(null=True)
#     def __str__(self):
#         return self.user.username
    # def calculate_duration(self):
    #     if self.checkOutTime:
    #         duration = self.checkOutTime - self.checkInTime
    #         return duration.total_seconds() / 3600.0  # Convert to hours
    #     else:
    #         return 0
    
class Salary(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.CharField(max_length=100, null=True)
    amount = models.FloatField(null=True)
    def __str__(self):
        return self.user.username
    
class Schedule(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    schedule_start = models.TimeField()
    schedule_end = models.TimeField()
    def __str__(self):
        return self.department.name
    
    
class Payroll(models.Model):
    status =(
        ('On Time','On Time'),
        ('Late','Late'),
        ('Absent','Absent'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    remarks = models.CharField(max_length=100, null=True, choices=status)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    deduction = models.FloatField(null=True)
    bonus = models.FloatField(null=True)
    overttimeBonus = models.FloatField(null=True)
    def __str__(self):
        return self.user.username
    
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Late', 'Late'),
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    dateOfQuestion = models.DateField(null=True)
    checkInTime = models.DateTimeField(null=True)
    checkOutTime = models.DateTimeField(null=True)
    overtime = models.DateTimeField(null=True,blank=True)
    name=models.CharField(max_length=255,null=True)
    duration = models.FloatField(null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)
        
    def calculate_duration(self):
        if self.checkOutTime:
            duration = self.checkOutTime - self.checkInTime
            return duration.total_seconds() / 3600.0  # Convert to hours
        else:
            return 0

class Events(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)
 
    class Meta:  
        db_table = "tblevents"
        
        