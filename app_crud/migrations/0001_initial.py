# Generated by Django 4.2 on 2023-05-18 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='custom_user',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('is_superuser', models.BooleanField(default=False)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('repassword', models.CharField(max_length=255)),
            ],
        ),
    ]