/**
 * 用户状态管理（使用 sessionStorage 支持多Tab独立登录）
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { userApi } from '@/api/user'

const S = sessionStorage

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<any>(null)
  const token = ref<string | null>(S.getItem('access_token'))

  const isLogin = computed(() => !!token.value)
  const isMerchant = computed(() => userInfo.value?.role === 'merchant')

  /** 保存登录状态 */
  function setLogin(data: { user: any; tokens: { access: string } }) {
    userInfo.value = data.user
    token.value = data.tokens.access
    S.setItem('access_token', data.tokens.access)
    S.setItem('user_info', JSON.stringify(data.user))
  }

  /** 从 sessionStorage 恢复状态 */
  function restore() {
    const saved = S.getItem('user_info')
    if (saved) {
      userInfo.value = JSON.parse(saved)
    }
  }

  /** 登出 */
  function logout() {
    userInfo.value = null
    token.value = null
    S.removeItem('access_token')
    S.removeItem('user_info')
  }

  /** 刷新用户信息 */
  async function refreshProfile() {
    try {
      const res: any = await userApi.getProfile()
      userInfo.value = res.data
      S.setItem('user_info', JSON.stringify(res.data))
    } catch {
      // ignore
    }
  }

  return { userInfo, token, isLogin, isMerchant, setLogin, restore, logout, refreshProfile }
})
