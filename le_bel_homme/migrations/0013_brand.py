# Generated by Django 4.2.1 on 2023-05-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('le_bel_homme', '0012_remove_perfume_slug_perfume_url_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
    ]
