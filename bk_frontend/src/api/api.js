import { $axios } from './axios'

// 调取api Demo
export const getDemoApi = params => {
  return $axios.get('/get_demo_api/', { params: params })
}

// 获取左侧菜单数据
export const getMenu = params => {
  return $axios.get('/api/sysmanage/menus/tree/', { params: params })
}
// 获取当前用户的权限列表
export const getCurrentPermission = params => {
  return $axios.get('/api/sysmanage/users/current_permission/', { params: params })
}
// 获取角色列表数据
export const getGroups = params => {
  return $axios.get('/api/sysmanage/groups/', { params: params })
}
// 新增/编辑角色数据时获取用户
export const getUserSelect = params => {
  return $axios.get('/api/sysmanage/users/select/', { params: params })
}
// 获取菜单树状结构数据
export const getMenuTree = params => {
  return $axios.get('/api/sysmanage/menus/tree/', { params: params })
}
// 获取单个角色的对应权限数据
export const getMenuAuthority = params => {
  return $axios.get(`/api/sysmanage/groups/${params.id}/`, params)
}
// 编辑角色数据
export const editGroups = params => {
  return $axios.put(`/api/sysmanage/groups/${params.id}/`, params)
}
// 添加角色数据
export const addGroups = params => {
  return $axios.post('/api/sysmanage/groups/', params)
}
// 删除角色数据
export const deleteGroups = params => {
  return $axios.delete(`/api/sysmanage/groups/${params.id}/`, params)
}
// 启用/禁用角色
export const groupsStatus = params => {
  return $axios.put('/api/sysmanage/groups/status/', params)
}
