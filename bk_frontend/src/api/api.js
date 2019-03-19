import { $axios } from './axios'

// 调取api Demo
export const getDemoApi = params => {
  return $axios.get('/get_demo_api/', { params: params })
}

// 获取左侧菜单数据
export const getMenu = params => {
  return $axios.get('/api/sysmanage/menus/tree/', { params: params })
}
