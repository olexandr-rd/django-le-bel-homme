# Generated by Django 4.2.1 on 2023-05-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('le_bel_homme', '0016_alter_perfume_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfume',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
