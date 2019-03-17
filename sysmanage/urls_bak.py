# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'sysmanage.log_views',
    (r'^search_log/$', 'search_log'),
    (r'^export_log_to_excel/$', 'export_log_to_excel'),
    (r'^get_select_log_object/$', 'get_select_log_object'),
    (r'^get_select_log_type/$', 'get_select_log_type'),
)

urlpatterns += patterns(
    'sysmanage.auth_views',
    (r'^sync_user/$', 'sync_user'),   # 同步用户
    (r'^get_user_list/$', 'get_user_list'),  # 获取用户列表
    (r'^get_not_added_user_list/$', 'get_not_added_user_list'),  # 待添加的用户
    (r'^add_user/$', 'add_user'),  # 添加用户
    (r'^delete_user/$', 'delete_user'),  # 删除用户
    (r'^edit_user/$', 'edit_user'),  # 编辑用户
    (r'^disable_user/$', 'disable_user'),  # 禁用用户
    (r'^able_user/$', 'able_user'),  # 启用用户
    (r'^get_group_list/$', 'get_group_list'),  # 获取角色列表
    (r'^get_all_group_list/$', 'get_all_group_list'),  # 获取所有的角色，添加用户的时候用到
    (r'^get_all_user_list/$', 'get_all_user_list'),  # 获取所有的用户，添加组的时候用到
    (r'^add_group/$', 'add_group'),  # 添加组
    (r'^edit_group_info/$', 'edit_group_info'),  # 编辑角色相关信息
    (r'^disable_group/$', 'disable_group'),  # 禁用组
    (r'^able_group/$', 'able_group'),  # 启用组
    (r'^delete_group/$', 'delete_group'),  # 删除组
    (r'^get_all_perms/$', 'get_all_perms'),
    (r'^get_group_detail/$', 'get_group_detail'),  # 组详情
    (r'^edit_group_permission/$', 'edit_group_permission'),  # 编辑角色权限
    (r'^get_user_permission/$', 'get_user_permission'),
)
