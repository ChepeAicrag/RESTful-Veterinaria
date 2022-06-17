# Generated by Django 4.0.3 on 2022-06-17 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
            ],
            options={
                'verbose_name': 'Breed',
                'verbose_name_plural': 'Breedes',
                'db_table': 'Breed',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='TypePet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
            ],
            options={
                'verbose_name': 'TypePet',
                'verbose_name_plural': 'TypesPet',
                'db_table': 'TypePet',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=1)),
                ('color', models.CharField(max_length=100)),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.breed')),
            ],
            options={
                'verbose_name': 'Pet',
                'verbose_name_plural': 'Pets',
                'db_table': 'Pets',
                'ordering': ('id',),
            },
        ),
    ]
