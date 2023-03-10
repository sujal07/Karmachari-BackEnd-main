# Generated by Django 3.2.17 on 2023-02-25 11:24

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Everyone', max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_start', models.TimeField()),
                ('schedule_end', models.TimeField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.department')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=100, null=True)),
                ('amount', models.FloatField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileimg', models.ImageField(default='img.png', upload_to='profile_images')),
                ('dob', models.DateField(auto_now=True)),
                ('phone_number', models.CharField(default=0, max_length=100)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.department')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(choices=[('On Time', 'On Time'), ('Late', 'Late'), ('Absent', 'Absent')], max_length=100, null=True)),
                ('deduction', models.FloatField(null=True)),
                ('bonus', models.FloatField(null=True)),
                ('overttimeBonus', models.FloatField(null=True)),
                ('salary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.salary')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('context', models.TextField(max_length=100000, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.department')),
            ],
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, null=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('duration', models.DateField(default=django.utils.timezone.now)),
                ('leave_type', models.CharField(choices=[('Sick Leave', 'Sick Leave'), ('Vacation', 'Vacation'), ('Emergency', 'Emergency')], max_length=100, null=True)),
                ('message', models.TextField(max_length=100000, null=True)),
                ('status', models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Not Approved', 'Not Approved')], default='Pending', max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tblevents',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfQuestion', models.DateField(null=True)),
                ('checkInTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('checkOutTime', models.DateTimeField(auto_now_add=True, null=True)),
                ('overtime', models.DateTimeField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('duration', models.FloatField(null=True)),
                ('status', models.CharField(choices=[('Late', 'Late'), ('Present', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')], max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
