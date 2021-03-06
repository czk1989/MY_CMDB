# Generated by Django 2.1.7 on 2019-03-08 09:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assets', '0002_auto_20190308_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.SmallIntegerField(choices=[(0, 'cmd'), (1, 'file_transfer')])),
                ('content', models.TextField(verbose_name='任务内容')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hosts', models.ManyToManyField(to='assets.BindHost')),
                ('user', models.ForeignKey(on_delete=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('status', models.SmallIntegerField(choices=[(0, 'success'), (1, 'failed'), (2, 'init')])),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('bind_host', models.ForeignKey(on_delete=None, to='assets.BindHost')),
                ('task', models.ForeignKey(on_delete=None, to='tasks.Task')),
            ],
        ),
    ]
