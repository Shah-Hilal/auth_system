# Generated by Django 5.1 on 2024-08-13 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='payment_terms',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_package',
            field=models.CharField(max_length=255),
        ),
    ]
