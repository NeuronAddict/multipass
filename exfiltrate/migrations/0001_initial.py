# Generated by Django 3.0.3 on 2020-02-13 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Credential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=400)),
                ('password', models.CharField(max_length=400)),
                ('found_date', models.DateTimeField(auto_now=True)),
                ('domain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exfiltrate.Domain')),
            ],
        ),
    ]
