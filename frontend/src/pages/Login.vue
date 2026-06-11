<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { userApi } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter(); const userStore = useUserStore()
const username = ref(''); const password = ref(''); const loading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) return
  loading.value = true
  try {
    const r: any = await userApi.login({ username: username.value, password: password.value })
    userStore.setLogin(r.data); showToast('登录成功')
    router.push(r.data.user.role === 'merchant' ? '/merchant' : '/home')
  } catch {} finally { loading.value = false }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-head">
        <span class="ah-emoji">☕</span>
        <div>
          <div class="ah-title">欢迎回来</div>
          <div class="ah-sub">登录后即可点餐</div>
        </div>
      </div>
      <van-form @submit="handleLogin">
        <div class="input-box">
          <van-field v-model="username" placeholder="用户名" :rules="[{ required: true, message: '请输入用户名' }]" />
          <van-field v-model="password" placeholder="密码" type="password" :rules="[{ required: true, message: '请输入密码' }]" />
        </div>
        <van-button round block type="primary" native-type="submit" :loading="loading" size="large" style="height:54px">登 录</van-button>
      </van-form>
      <div class="auth-foot">没有账号？<router-link to="/register">注册</router-link></div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh; background: #f5f3f0;
  display: flex; flex-direction: column; justify-content: center;
  padding: 24px;
}
.auth-card {
  background: #fff;
  border-radius: 32px;
  padding: 40px 32px 32px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02), 0 8px 24px rgba(0,0,0,0.06), 0 20px 48px rgba(0,0,0,0.04);
}
.auth-head { display: flex; align-items: center; gap: 18px; margin-bottom: 32px; }
.ah-emoji { font-size: 44px; line-height: 1; flex-shrink: 0; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.10)); }
.ah-title { font-size: 28px; font-weight: 900; color: #1a1a1a; line-height: 1; margin-bottom: 4px; }
.ah-sub { font-size: 14px; color: #aaa; }
.input-box { background: #f5f3f0; border-radius: 28px; padding: 4px 0; margin-bottom: 28px; }
.input-box :deep(.van-field) { padding: 16px 20px; font-size: 16px; }
.auth-foot { text-align: center; margin-top: 24px; font-size: 15px; color: #aaa; }
.auth-foot a { color: #1a1a1a; text-decoration: none; font-weight: 700; }
</style>
