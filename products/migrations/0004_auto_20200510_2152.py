# Generated by Django 3.0.5 on 2020-05-10 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200510_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airline',
            name='id',
        ),
        migrations.AlterField(
            model_name='airline',
            name='airline_code',
            field=models.CharField(max_length=6, primary_key=True, serialize=False),
        ),
    ]