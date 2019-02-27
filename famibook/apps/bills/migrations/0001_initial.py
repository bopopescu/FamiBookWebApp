# Generated by Django 2.1.7 on 2019-02-27 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('daybooks', '0001_initial'),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('type', models.IntegerField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('date', models.DateTimeField()),
                ('note', models.TextField(max_length=20)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bills', to='categories.Category')),
                ('daybook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daybooks.Daybook')),
            ],
            options={
                'db_table': 'bills',
            },
        ),
    ]