from django.db import models

# Create your models here.


class Task(models.Model):
    """批量任务记录表"""
    user = models.ForeignKey("eye.UserProfile",on_delete=None)
    task_type_choices = ((0,'cmd'),(1,'file_transfer'))
    task_type = models.SmallIntegerField(choices=task_type_choices)
    content = models.TextField(verbose_name="任务内容")
    hosts = models.ManyToManyField("assets.BindHost")
    date  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.task_type,self.content)


class TaskLogDetail(models.Model):
    task = models.ForeignKey("Task",on_delete=None)
    bind_host = models.ForeignKey("assets.BindHost",on_delete=None)
    result = models.TextField()

    status_choices = ((0,'success'),(1,'failed'),(2,'init'))
    status = models.SmallIntegerField(choices=status_choices)

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True,null=True)


    def __str__(self):
        return "%s %s" %(self.bind_host,self.status)