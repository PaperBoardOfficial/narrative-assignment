# Generated by Django 5.0.6 on 2024-05-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Class', models.CharField(max_length=255)),
                ('School', models.CharField(max_length=255)),
                ('State', models.CharField(max_length=255)),
            ],
        ),
    ]