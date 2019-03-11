from django.db import models


class IDC(models.Model):
    """
    机房信息
    """
    name = models.CharField(verbose_name='机房', max_length=32)
    floor = models.IntegerField(verbose_name='楼层', default=1)

    class Meta:
        db_table = "IDC"
        verbose_name_plural = "IDC机房表"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField(verbose_name='资产标签', max_length=32, unique=True)

    class Meta:
        db_table = "Tag"
        verbose_name_plural = "资产标签表"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )
    device_status_choices = (
        (1, 'Online'),
        (2, 'Down'),
        (3, 'Unreachable'),
        (4, 'Problem'),
    )

    device_type_id = models.IntegerField(verbose_name='资产类型',choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(verbose_name='资产状态',choices=device_status_choices, default=1)

    cabinet_num = models.CharField(verbose_name='机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=30, null=True, blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True, on_delete=None)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True, on_delete=None)

    tag = models.ManyToManyField('Tag')

    latest_date = models.DateField(auto_now=True,verbose_name='更新日期',null=True)
    create_at = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')

    class Meta:
        db_table = "Asset"
        verbose_name_plural = "资产信息表"

    def __str__(self):
        return "%s-%s" % (self.cabinet_num, self.cabinet_order)


class Server(models.Model):
    """
    服务器信息
    """
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)

    hostname = models.GenericIPAddressField(verbose_name='服务器名称',unique=True)
    sn = models.CharField(verbose_name='SN号', max_length=64, db_index=True)
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)

    manage_ip = models.GenericIPAddressField(verbose_name='管理IP', null=True, blank=True)

    os_platform = models.CharField(verbose_name='系统', max_length=16, null=True, blank=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=16, null=True, blank=True)

    cpu_count = models.IntegerField(verbose_name='CPU个数', null=True, blank=True)
    cpu_physical_count = models.IntegerField(verbose_name='CPU物理个数', null=True, blank=True)
    cpu_model = models.CharField(verbose_name='CPU型号', max_length=128, null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间', blank=True)
    port = models.CharField(verbose_name='端口', max_length=16, null=True, blank=True)

    class Meta:
        db_table = "Server"
        verbose_name_plural = "服务器信息表"

    def __str__(self):
        return self.hostname


class BusinessUnit(models.Model):
    """主机组/业务组"""
    name = models.CharField(verbose_name='业务组', max_length=64, unique=True)
    bind_hosts = models.ManyToManyField("BindHost")
    contact = models.ForeignKey('eye.UserGroup', verbose_name='业务联系人', related_name='c',on_delete=None)
    manager = models.ForeignKey('eye.AdminInfo', verbose_name='系统管理员', related_name='m',on_delete=None)

    class Meta:
        db_table = "BusinessUnit"
        verbose_name_plural = "业务组表"

    def __str__(self):
        return self.name


class RemoteUser(models.Model):
    """存储远程用户名密码"""
    username = models.CharField(verbose_name='服务器账号',max_length=64)
    auth_type_choices = ((0,'ssh/password'),(1,'ssh/key'))
    auth_type = models.SmallIntegerField(choices=auth_type_choices,default=0)
    password = models.CharField(verbose_name='服务器密码',max_length=128,blank=True,null=True)

    def __str__(self):
        return "%s(%s)%s" %( self.username,self.get_auth_type_display(),self.password)

    class Meta:
        db_table = "RemoteUser"
        unique_together = ('username','auth_type','password')


class BindHost(models.Model):
    """绑定远程主机和远程用户的对应关系"""
    host = models.ForeignKey("Asset",on_delete=None)
    remote_user = models.ForeignKey("RemoteUser",on_delete=models.CASCADE)

    def __str__(self):
        return "%s -> %s" %(self.host,self.remote_user)

    class Meta:
        db_table = "BindHost"
        unique_together = ("host","remote_user")


class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField(verbose_name='插槽位', max_length=8)
    model = models.CharField(verbose_name='磁盘型号', max_length=32)
    capacity = models.FloatField(verbose_name='磁盘容量GB')
    pd_type = models.CharField(verbose_name='磁盘类型', max_length=32)
    server_obj = models.ForeignKey('Server',on_delete=None)

    class Meta:
        db_table = "Disk"
        verbose_name_plural = "硬盘表"

    def __str__(self):
        return self.slot


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField(verbose_name='网卡名称', max_length=128)
    hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=64)
    netmask = models.CharField(max_length=64)
    ipaddrs = models.CharField(verbose_name='ip地址', max_length=256)
    up = models.BooleanField(verbose_name='是否更新',default=False)
    server_obj = models.ForeignKey('Server',on_delete=None)

    class Meta:
        db_table = "NIC"
        verbose_name_plural = "网卡表"

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField(verbose_name='插槽位', max_length=32)
    manufacturer = models.CharField(verbose_name='制造商', max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=64)
    capacity = models.FloatField(verbose_name='容量', null=True, blank=True)
    sn = models.CharField(verbose_name='内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField(verbose_name='速度', max_length=16, null=True, blank=True)
    server_obj = models.ForeignKey('Server',on_delete=None)

    class Meta:
        db_table = "Memory"
        verbose_name_plural = "内存表"

    def __str__(self):
        return self.slot


class AssetRecord(models.Model):
    """
    资产变更记录,creator为空时，表示是资产汇报的数据。
    """
    asset_obj = models.ForeignKey('Asset',on_delete=None)
    content = models.TextField(verbose_name='变更内容',null=True)
    creator = models.ForeignKey('eye.UserProfile', null=True, blank=True,on_delete=None)
    create_at = models.DateTimeField(verbose_name='创建日期',auto_now_add=True)

    class Meta:
        db_table = "AssetRecord"
        verbose_name_plural = "资产记录表"

    def __str__(self):
        return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


class ErrorLog(models.Model):
    """
    错误日志,如：agent采集数据错误 或 运行错误
    """
    asset_obj = models.ForeignKey('Asset', null=True, blank=True,on_delete=None)
    title = models.CharField(max_length=16)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ErrorLog"
        verbose_name_plural = "错误日志表"

    def __str__(self):
        return self.title




