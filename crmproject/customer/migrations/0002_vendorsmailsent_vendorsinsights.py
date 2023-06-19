# Generated by Django 4.2.2 on 2023-06-17 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorsMailSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=300, null=True)),
                ('body', models.CharField(blank=True, max_length=1000, null=True)),
                ('represent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.representatives')),
            ],
        ),
        migrations.CreateModel(
            name='VendorsInsights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_date', models.DateField(blank=True, null=True)),
                ('current_date', models.DateField(blank=True, null=True)),
                ('next_date', models.DateField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
        ),
    ]
