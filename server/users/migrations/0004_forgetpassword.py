# Generated by Django 3.2.25 on 2024-10-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20240928_1327'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgetPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
