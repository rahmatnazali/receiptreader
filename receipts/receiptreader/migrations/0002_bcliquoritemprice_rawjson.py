# Generated by Django 2.2.4 on 2019-09-02 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('receiptreader', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rawJson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timeStamp', models.DateField(auto_now_add=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receiptreader.Document')),
            ],
        ),
        migrations.CreateModel(
            name='BCLiquorItemPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateField(auto_now_add=True)),
                ('currentPrice', models.DecimalField(decimal_places=2, max_digits=6)),
                ('regularPrice', models.DecimalField(decimal_places=2, max_digits=6)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receiptreader.BCLiquorItem')),
            ],
        ),
    ]
