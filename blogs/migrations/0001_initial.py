# Generated by Django 3.2.3 on 2021-06-03 13:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ForbiddenWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField(default=18, validators=[django.core.validators.MaxValueValidator(60), django.core.validators.MinValueValidator(18)])),
                ('is_blocked', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Replies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='replies', to='blogs.comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogs.users')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogs.users')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogs.categories')),
                ('dislikes', models.ManyToManyField(related_name='dislikes', to='blogs.Users')),
                ('likes', models.ManyToManyField(related_name='likes', to='blogs.Users')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogs.tags')),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='blogs.posts'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blogs.users'),
        ),
    ]
