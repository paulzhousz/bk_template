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
// 编辑角色数据
export const editGroups = params => {
  return $axios.post('/api/sysmanage/groups/{id}/', params)
}
// 添加角色数据
export const addGroups = params => {
  return $axios.post('/api/sysmanage/groups/', params)
}
// 删除角色数据
export const deleteGroups = params => {
  return $axios.post('/api/sysmanage/groups/{id}/', params)
}
// 禁用角色
export const groupsStatus = params => {
  return $axios.post('/api/sysmanage/groups/status/', params)
}
