# Generated by Django 2.1.7 on 2019-03-08 09:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eye', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessunit',
            name='contact',
            field=models.ForeignKey(on_delete=None, related_name='c', to='eye.UserGroup', verbose_name='业务联系人'),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='manager',
            field=models.ForeignKey(on_delete=None, related_name='m', to='eye.AdminInfo', verbose_name='系统管理员'),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='host',
            field=models.ForeignKey(on_delete=None, to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='bindhost',
            name='remote_user',
            field=models.ForeignKey(on_delete=None, to='assets.RemoteUser'),
        ),
        migrations.AddField(
            model_name='assetrecord',
            name='asset_obj',
            field=models.ForeignKey(on_delete=None, to='assets.Asset'),
        ),
        migrations.AddField(
            model_name='assetrecord',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='assets.BusinessUnit', verbose_name='属于的业务线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=None, to='assets.IDC', verbose_name='IDC机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tag',
            field=models.ManyToManyField(to='assets.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhost',
            unique_together={('host', 'remote_user')},
        ),
    ]
