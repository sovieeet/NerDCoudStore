# Generated by Django 4.2.5 on 2023-10-25 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nerdapp', '0019_remove_subasta_id_subasta_id_subasta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subasta',
            name='id_subasta',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]