
class ConditionConfig(object):
    def __init__(self):
        pass

    @classmethod
    def choice_values(cls, server):
        values = []
        tem='%s_%s'%(server,'table_config')
        if hasattr(cls,tem):
            result=getattr(cls,tem)()
            for item in result:
                values.append(item['q'])
        return values

    @classmethod
    def choice_table_config(cls,server):
        table_config='%s_%s'%(server,'table_config')
        if hasattr(cls,table_config):
            func=getattr(cls,table_config)
            return func()
        else:
            return

    @classmethod
    def choice_config(cls,server):
        config='%s_%s'%(server,'config')
        if hasattr(cls,config):
            func=getattr(cls,config)
            return func()
        else:
            return

    @classmethod
    def choice_list(cls,server):
        config='%s_%s'%(server,'list')
        if hasattr(cls,config):
            func=getattr(cls,config)
            return func()
        else:
            return

    @classmethod
    def idc_config(cls):
        values = [
            {'name': 'name', 'text': '机房', 'condition_type': 'input'},
            {'name': 'floor', 'text': '楼层', 'condition_type': 'input'},
        ]
        return values

    @classmethod
    def asset_config(cls):
        values = [
            {'name': 'cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
            {'name': 'device_type_id', 'text': '资产类型', 'condition_type': 'select', 'global_name': 'device_type_list'},
            {'name': 'device_status_id', 'text': '资产状态', 'condition_type': 'select', 'global_name': 'device_status_list'},
        ]
        return values

    @classmethod
    def bindhost_config(cls):
        values = [
            {'name': 'remote_user__username', 'text': '账号', 'condition_type': 'input'},
            {'name': 'host__id', 'text': '所属资产ID', 'condition_type': 'input'},
        ]
        return values


    @classmethod
    def tag_config(cls):
        values = [
            {'name': 'name', 'text': '标签', 'condition_type': 'input'},

        ]
        return values

    @classmethod
    def idc_table_config(cls):
        values = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'name',
                'title': "机房",
                'display': 1,
                'attr': {'name': 'name', 'edit-enable': 'true', 'edit-type': 'input', }
            },
            {
                'q': 'floor',
                'title': "楼层",
                'display': 1,
                'attr': {'name': 'floor', 'edit-enable': 'true', 'edit-type': 'input', }
            },
        ]
        return values

    @classmethod
    def asset_table_config(cls):
        values = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'idc_id',
                'title': "IDC",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'idc__name',
                'title': "IDC",
                'display': 1,
                'attr': {'name': 'idc_id', 'id': '@idc_id', 'edit-enable': 'true', 'edit-type': 'select',
                         'global-name': 'idc_list'}
            },
            {
                'q': 'cabinet_num',
                'title': "机柜号",
                'display': 1,
                'attr': {'name': 'cabinet_num', 'edit-enable': 'true', 'edit-type': 'input', }
            },
            {
                'q': 'cabinet_order',
                'title': "位置",
                'display': 1,
                'attr': {'name': 'cabinet_order', 'edit-enable': 'true', 'edit-type': 'input', }
            },
            {
                'q': 'business_unit_id',
                'title': "业务线ID",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'business_unit__name',
                'title': "业务线",
                'display': 1,
                'attr': {'name': 'business_unit_id', 'id': '@business_unit_id', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'business_unit_list'}
            },
            {
                'q': 'device_status_id',
                'title': "资产状态",
                'display': 2,
                'attr': {'name': 'device_status_id', 'id': '@@device_status_list', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_status_list'}
            },
            {
                'q': 'device_type_id',
                'title': "资产类型",
                'display': 2,
                'attr': {'name': 'device_type_id', 'id': '@@device_type_list', 'edit-enable': 'true',
                         'edit-type': 'select',
                         'global-name': 'device_type_list'}
            },
        ]
        return values

    @classmethod
    def tag_table_config(cls):
        values = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'name',
                'title': "标签",
                'display': 1,
                'attr': {'name': 'name', 'edit-enable': 'true', 'edit-type': 'input', }
            },
            # {
            #     'q': 'floor',
            #     'title': "楼层",
            #     'display': 1,
            #     'attr': {'name': 'floor', 'edit-enable': 'true', 'edit-type': 'input', }
            # },
        ]
        return values

    @classmethod
    def bindhost_table_config(cls):
        values = [
            {
                'q': 'id',
                'title': "ID",
                'display': 0,
                'attr': {}
            },
            {
                'q': 'host__id',
                'title': "资产ID",
                'display': 1,
                'attr': {'name': 'asset_id', 'id': '@asset_id', 'edit-enable': 'false', 'edit-type': 'input'}
            },
            {
                'q': 'remote_user__username',
                'title': "账号名",
                'display': 1,
                'attr': {'name': 'username', 'edit-enable': 'true', 'edit-type': 'input', }
            },
            {
                'q': 'remote_user__auth_type',
                'title': "登录方式(0/password,1/key)",
                'display': 1,
                'attr': {'name': 'auth_type', 'edit-enable': 'true', 'edit-type': 'select','global-name': 'auth_type_list'}
            },
            {
                'q': 'remote_user__password',
                'title': "密码",
                'display': 1,
                'attr': {'name': 'password', 'edit-enable': 'true', 'edit-type': 'input'}
            },

            # {
            #     'q': 'host__business_unit__name',
            #     'title': "业务线",
            #     'display': 1,
            #     'attr': {'name': 'business_unit_id', 'id': '@business_unit_id', 'edit-enable': 'false',
            #              'edit-type': 'select',
            #              'global-name': 'business_unit_list'}
            # },
            # {
            #     'q': 'device_status_id',
            #     'title': "资产状态",
            #     'display': 2,
            #     'attr': {'name': 'device_status_id', 'id': '@@device_status_list', 'edit-enable': 'true',
            #              'edit-type': 'select',
            #              'global-name': 'device_status_list'}
            # },
            # {
            #     'q': 'device_type_id',
            #     'title': "资产类型",
            #     'display': 2,
            #     'attr': {'name': 'device_type_id', 'id': '@@device_type_list', 'edit-enable': 'true',
            #              'edit-type': 'select',
            #              'global-name': 'device_type_list'}
            # },
        ]
        return values


