# Generated by Django 4.2.5 on 2023-10-25 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nerdapp', '0016_remove_subasta_id_subasta_id_subasta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subasta',
            name='id_subasta',
        ),
        migrations.AddField(
            model_name='subasta',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]