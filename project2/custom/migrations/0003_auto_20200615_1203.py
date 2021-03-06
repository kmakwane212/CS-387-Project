# Generated by Django 3.0 on 2020-06-15 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0002_auto_20200615_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='corona_warrior',
            name='area',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom.Area'),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='area',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom.Area'),
        ),
        migrations.AlterField(
            model_name='official',
            name='area',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='custom.Area'),
        ),
    ]
