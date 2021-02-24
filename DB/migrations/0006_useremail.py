# Generated by Django 3.1.5 on 2021-02-23 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0005_chiefcarrier_majorinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('email_no', models.AutoField(primary_key=True, serialize=False)),
                ('user_email', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'USER_EMAIL',
                'managed': False,
            },
        ),
    ]
