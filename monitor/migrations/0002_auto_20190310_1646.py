# Generated by Django 2.1.7 on 2019-03-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitorhostgroup',
            options={'verbose_name_plural': '监控主机组'},
        ),
        migrations.AlterField(
            model_name='monitorservice',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='监控服务名称'),
        ),
    ]
