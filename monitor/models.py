from django.db import models
# from django.contrib.auth.models import User
# Create your models here.


class MonitorHost(models.Model):
    asset=models.OneToOneField('assets.Asset',verbose_name='资产',on_delete=None)
    host_groups = models.ForeignKey('MonitorHostGroup',verbose_name='业务组',on_delete=None)
    templates = models.ManyToManyField("MonitorTemplate",blank=True) # A D E
    monitored_by_choices = (
        ('agent','Agent'),
        ('snmp','SNMP'),
        ('wget','WGET'),
    )
    monitored_by = models.CharField(verbose_name='监控方式',max_length=64,choices=monitored_by_choices)
    host_alive_check_interval = models.IntegerField(verbose_name="主机存活状态检测间隔", default=30)
    memo = models.TextField(verbose_name="备注",blank=True,null=True)

    class Meta:
        db_table = "MonitorHost"
        verbose_name_plural = '监控资产'

    def __str__(self):
        return self.asset.server.hostname


class MonitorHostGroup(models.Model):
    host_group=models.OneToOneField('assets.BusinessUnit',verbose_name='业务组',on_delete=None)
    name = models.CharField(verbose_name='业务组',max_length=64,unique=True)
    templates = models.ManyToManyField("MonitorTemplate",blank=True)
    memo = models.TextField(verbose_name="备注",blank=True,null=True)

    class Meta:
        db_table = "MonitorHostGroup"
        verbose_name_plural = '监控主机组'

    def __str__(self):
        return self.name


class MonitorServiceIndex(models.Model):
    name = models.CharField(verbose_name="监控服务指标",max_length=64) #Linux cpu idle
    key =models.CharField(max_length=64,unique=True) #idle
    data_type_choices = (
        ('int',"int"),
        ('float',"float"),
        ('str',"string")
    )
    data_type = models.CharField(verbose_name='指标数据类型',max_length=32,choices=data_type_choices,default='int')
    memo = models.CharField(verbose_name="备注",max_length=128,blank=True,null=True)

    class Meta:
        db_table = "MonitorServiceIndex"
        verbose_name_plural = '监控服务指标'

    def __str__(self):
        return "%s.%s" %(self.name,self.key)


class MonitorService(models.Model):
    name = models.CharField(verbose_name='监控服务名称',max_length=64,unique=True)
    interval = models.IntegerField(verbose_name='监控间隔',default=60)
    plugin_name = models.CharField(verbose_name='插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('MonitorServiceIndex',verbose_name=u"指标列表",blank=True)
    has_sub_service = models.BooleanField(default=False,help_text=u"如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡") #如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡
    memo = models.CharField(verbose_name="备注",max_length=128,blank=True,null=True)

    class Meta:
        db_table = 'MonitorService'
        verbose_name_plural = '监控服务'

    def __str__(self):
        return self.name


class MonitorTemplate(models.Model):
    name = models.CharField(verbose_name='模版名称',max_length=64,unique=True)
    services = models.ManyToManyField('MonitorService',verbose_name="服务列表")
    triggers = models.ManyToManyField('Trigger',verbose_name="触发器列表",blank=True)

    class Meta:
        db_table = 'MonitorTemplate'
        verbose_name_plural = '监控模板'

    def __str__(self):
        return self.name


class TriggerExpression(models.Model):
    trigger = models.ForeignKey('Trigger', verbose_name="所属触发器",on_delete=None)
    service = models.ForeignKey('MonitorService', verbose_name="关联服务",on_delete=None)
    service_index = models.ForeignKey('MonitorServiceIndex', verbose_name="关联服务指标",on_delete=None)
    specified_index_key = models.CharField(verbose_name="只监控专门指定的指标key", max_length=64, blank=True, null=True)
    operator_type_choices = (('eq', '='), ('lt', '<'), ('gt', '>'))
    operator_type = models.CharField(verbose_name="运算符", choices=operator_type_choices, max_length=32)
    data_calc_type_choices = (
        ('avg', 'Average'),
        ('max', 'Max'),
        ('hit', 'Hit'),
        ('last', 'Last'),
    )
    data_calc_func = models.CharField(verbose_name="数据处理方式", choices=data_calc_type_choices, max_length=64)
    data_calc_args = models.CharField(verbose_name="函数传入参数", help_text=u"若是多个参数,则用,号分开,第一个值是时间", max_length=64)
    threshold = models.IntegerField(verbose_name="阈值")
    logic_type_choices = (('or', 'OR'), ('and', 'AND'))
    logic_type = models.CharField(verbose_name="与一个条件的逻辑关系", choices=logic_type_choices, max_length=32, blank=True, null=True)

    def __str__(self):
        return "%s %s(%s(%s))" % (self.service_index, self.operator_type, self.data_calc_func, self.data_calc_args)

    class Meta:
        db_table = 'TriggerExpression'
        verbose_name_plural = '监控属性'


class Trigger(models.Model):
    name = models.CharField(verbose_name='触发器名称', max_length=64)
    severity_choices = (
        (1, 'Information'),
        (2, 'Warning'),
        (3, 'Average'),
        (4, 'High'),
        (5, 'Diaster'),
    )
    severity = models.IntegerField(verbose_name='告警级别', choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField(verbose_name="备注", blank=True, null=True)

    class Meta:
        db_table = 'Trigger'
        verbose_name_plural = '触发器'

    def __str__(self):
        return "<serice:%s, severity:%s>" % (self.name, self.get_severity_display())


class Action(models.Model):
    """报警策略"""
    name = models.CharField(max_length=64, unique=True)
    host_groups = models.ManyToManyField('assets.BusinessUnit', blank=True)
    hosts = models.ManyToManyField('MonitorHost', blank=True)
    triggers = models.ManyToManyField('Trigger', blank=True, help_text=u"想让哪些trigger触发当前报警动作")
    interval = models.IntegerField(verbose_name=u'告警间隔(s)', default=300)
    operations = models.ManyToManyField('ActionOperation',verbose_name="报警动作")
    recover_notice = models.BooleanField(verbose_name=u'故障恢复后发送通知消息', default=True)
    recover_subject = models.CharField(max_length=128, blank=True, null=True)
    recover_message = models.TextField(blank=True, null=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'Action'
        verbose_name_plural = '报警策略'

    def __str__(self):
        return self.name


class ActionOperation(models.Model):
    """报警动作"""
    name = models.CharField(max_length=64)
    step = models.SmallIntegerField(verbose_name="第n次告警", default=1, help_text="当trigger触发次数小于这个值时就执行这条记录里报警方式")
    action_type_choices = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('script', 'RunScript'),
    )
    action_type = models.CharField(verbose_name="动作类型", choices=action_type_choices, default='email', max_length=64)
    notifiers = models.ManyToManyField('eye.UserProfile', verbose_name=u"通知对象", blank=True)
    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''
    msg_format = models.TextField(verbose_name="消息格式", default=_msg_format)

    class Meta:
        db_table = 'ActionOperation'
        verbose_name_plural = '报警动作'

    def __str__(self):
        return self.name


class EventLog(models.Model):
    """存储报警及其它事件日志"""
    event_type_choices = ((0, '报警事件'), (1, '维护事件'))
    event_type = models.SmallIntegerField(choices=event_type_choices, default=0)
    host = models.ForeignKey("MonitorHost",on_delete=None)
    trigger = models.ForeignKey("Trigger", blank=True, null=True,on_delete=None)
    log = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'EventLog'
        verbose_name_plural = '报警日志'

    def __str__(self):
        return "host%s  %s" % (self.host, self.log)



