# Generated by Django 2.2.6 on 2019-10-17 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('receiptreader', '0005_bill_billfrom_billto_lineitem_receipt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='receipt',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='receiptreader.Receipt'),
        ),
    ]
