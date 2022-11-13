# Generated by Django 4.1.3 on 2022-11-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='')),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('category', models.ManyToManyField(to='product.category')),
            ],
        ),
    ]
