# Generated by Django 4.2.4 on 2023-08-29 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_added_by_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'course')},
        ),
    ]