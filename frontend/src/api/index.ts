/**
 * Axios 请求封装
 * 统一处理请求/响应拦截、Token管理、错误提示
 */
import axios from 'axios'
import { showDialog, showNotify } from 'vant'

const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

const S = sessionStorage

// 请求拦截：自动携带 Token
request.interceptors.request.use(
  (config) => {
    const token = S.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截：统一处理错误（居中弹窗）
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const data = error.response?.data

    if (status === 401) {
      // token 过期，清除登录态跳转登录页
      S.removeItem('access_token')
      S.removeItem('user_info')
      showDialog({ title: '提示', message: '登录已过期，请重新登录', confirmButtonColor: '#1a1a1a' }).then(() => {
        window.location.hash = '#/login'
      }).catch(() => {})
    } else if (data?.message) {
      showDialog({ title: '提示', message: data.message, confirmButtonColor: '#1a1a1a' }).catch(() => {})
    } else {
      showDialog({ title: '提示', message: '网络错误，请稍后重试', confirmButtonColor: '#1a1a1a' }).catch(() => {})
    }

    return Promise.reject(error)
  }
)

export default request
