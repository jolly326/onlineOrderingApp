/** 用户模块 API */
import request from './index'

export const userApi = {
  /** 注册（支持角色选择） */
  register(data: { username: string; phone: string; password: string; role?: string }) {
    return request.post('/users/register', data)
  },
  /** 登录 */
  login(data: { username: string; password: string }) {
    return request.post('/users/login', data)
  },
  /** 获取个人信息 */
  getProfile() {
    return request.get('/users/profile')
  },
  /** 更新个人信息 */
  updateProfile(data: { username?: string; avatar?: string }) {
    return request.put('/users/profile', data)
  },
}
