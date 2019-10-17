# Generated by Django 2.2.6 on 2019-10-17 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('receiptreader', '0007_auto_20191017_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billfrom',
            name='receipt',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='receiptreader.Receipt'),
        ),
        migrations.AlterField(
            model_name='billto',
            name='receipt',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='receiptreader.Receipt'),
        ),
        migrations.AlterField(
            model_name='lineitem',
            name='receipt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='receiptreader.Receipt'),
        ),
    ]
