# Generated by Django 3.0.7 on 2020-08-07 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0005_auto_20200807_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='h9.jpg', upload_to=''),
        ),
    ]
