# Generated by Django 4.0.3 on 2022-06-17 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.CharField(max_length=100, verbose_name='Descripcion')),
                ('isSuperAdmin', models.BooleanField(default=False, verbose_name='Super admin')),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'Role',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cp', models.CharField(max_length=255)),
                ('town', models.CharField(max_length=255)),
                ('state', models.CharField(default='Oaxaca', max_length=255)),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('street', models.CharField(max_length=255)),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
                ('town', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.town')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'db_table': 'Address',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=150)),
                ('paternal_surname', models.CharField(max_length=150, null=True)),
                ('mothers_maiden_name', models.CharField(max_length=150, null=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status_delete', models.BooleanField(default=False, verbose_name='Status Delete')),
                ('address', models.ForeignKey(choices=[(1, 'Administrador'), (2, 'Cliente')], on_delete=django.db.models.deletion.CASCADE, to='users.address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('role', models.ForeignKey(choices=[(1, 'Administrador'), (2, 'Cliente')], on_delete=django.db.models.deletion.CASCADE, to='users.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'Users',
                'ordering': ('id',),
            },
        ),
    ]
