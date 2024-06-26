# Generated by Django 4.1.5 on 2023-02-04 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state_name', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'state',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
                ('dob', models.DateField()),
                ('age', models.IntegerField()),
                ('contact', models.BigIntegerField()),
                ('gender', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('zipcode', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adminlawyer.city')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adminlawyer.state')),
            ],
            options={
                'db_table': 'client',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='adminlawyer.state'),
        ),
    ]
