# Generated by Django 3.2.3 on 2021-05-31 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20210530_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='category',
        ),
        migrations.AddField(
            model_name='posts',
            name='category',
            field=models.ManyToManyField(related_name='posts', to='blogs.Categories'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='picture',
            field=models.ImageField(upload_to='./static/images'),
        ),
    ]
