# Generated by Django 4.2.6 on 2024-03-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteusers', '0003_notification_paid_work_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='housemaid',
            name='rate_per_hour',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]