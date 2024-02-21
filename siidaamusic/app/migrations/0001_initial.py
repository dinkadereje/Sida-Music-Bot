# Generated by Django 4.2.10 on 2024-02-20 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('total_track', models.IntegerField()),
                ('language', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('global_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('album_art', models.ImageField(upload_to='album_arts')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('audio_file', models.FileField(blank=True, upload_to='tracks')),
                ('duration', models.DurationField()),
                ('track_number', models.PositiveSmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('global_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('track_art', models.ImageField(upload_to='track_arts')),
                ('sample', models.FileField(blank=True, upload_to='sample')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='app.album')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.BigIntegerField()),
                ('payment_type', models.CharField(choices=[('G', 'Global'), ('L', 'Local')], max_length=2)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.album')),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.track')),
            ],
        ),
    ]