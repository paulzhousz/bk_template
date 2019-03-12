import { $axios } from './axios'

// 调取api Demo
export const getDemoApi = params => {
  return $axios.get('/get_demo_api/', { params: params })
}