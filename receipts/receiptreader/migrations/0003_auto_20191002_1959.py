# Generated by Django 2.2.4 on 2019-10-02 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receiptreader', '0002_bcliquoritemprice_rawjson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawjson',
            name='text',
        ),
        migrations.AddField(
            model_name='rawjson',
            name='file',
            field=models.FileField(null=True, upload_to='jsons'),
        ),
        migrations.AddField(
            model_name='rawjson',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
