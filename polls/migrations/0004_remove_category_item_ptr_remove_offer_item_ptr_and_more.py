# Generated by Django 4.0.5 on 2022-11-07 11:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_remove_category_id_remove_category_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='item_ptr',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='item_ptr',
        ),
        migrations.AddField(
            model_name='category',
            name='id',
            field=models.CharField(default=None, max_length=99, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.category'),
        ),
        migrations.AddField(
            model_name='category',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offer',
            name='id',
            field=models.CharField(default=None, max_length=99, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='offer',
            name='name',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='offer',
            name='parent_category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.category'),
        ),
        migrations.AddField(
            model_name='offer',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
