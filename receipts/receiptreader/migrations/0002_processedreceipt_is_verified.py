# Generated by Django 2.2.6 on 2019-11-09 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiptreader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='processedreceipt',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
