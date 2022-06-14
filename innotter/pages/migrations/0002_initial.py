# Generated by Django 4.0.5 on 2022-06-14 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tags', '0001_initial'),
        ('pages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='follow_requests',
            field=models.ManyToManyField(related_name='requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='followers',
            field=models.ManyToManyField(related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(related_name='pages', to='tags.tag'),
        ),
    ]
