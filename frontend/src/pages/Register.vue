<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { userApi } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter(); const userStore = useUserStore()
const username = ref(''); const phone = ref(''); const password = ref(''); const confirmPwd = ref(''); const loading = ref(false)
const selectedRole = ref<'user' | 'merchant'>('user')

const roles = [
  { value: 'user' as const, icon: '🙋', label: '我要点餐', desc: '浏览菜单、下单点餐' },
  { value: 'merchant' as const, icon: '🏪', label: '我是商家', desc: '管理菜品、处理订单' },
]

async function handleRegister() {
  if (password.value !== confirmPwd.value) return
  loading.value = true
  try {
    const r: any = await userApi.register({
      username: username.value,
      phone: phone.value,
      password: password.value,
      role: selectedRole.value,
    })
    userStore.setLogin(r.data)
    showToast('注册成功')
    router.push(selectedRole.value === 'merchant' ? '/merchant' : '/home')
  } catch {} finally { loading.value = false }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-head">
        <span class="ah-emoji">☕</span>
        <div>
          <div class="ah-title">创建账号</div>
          <div class="ah-sub">选择您的身份</div>
        </div>
      </div>

      <!-- 角色选择卡片 -->
      <div class="role-grid">
        <button
          v-for="r in roles"
          :key="r.value"
          :class="['role-card', { active: selectedRole === r.value }]"
          @click="selectedRole = r.value"
        >
          <span class="rc-emoji">{{ r.icon }}</span>
          <div class="rc-info">
            <span class="rc-label">{{ r.label }}</span>
            <span class="rc-desc">{{ r.desc }}</span>
          </div>
          <span v-if="selectedRole === r.value" class="rc-check"><van-icon name="success" size="18" /></span>
        </button>
      </div>

      <van-form @submit="handleRegister">
        <div class="input-box">
          <van-field v-model="username" placeholder="昵称" :rules="[{ required: true, message: '请输入昵称' }]" />
          <van-field v-model="phone" placeholder="手机号" maxlength="11" type="tel" :rules="[{ required: true, message: '请输入手机号' }, { pattern: /^1\d{10}$/, message: '手机号格式错误' }]" />
          <van-field v-model="password" placeholder="密码（至少6位）" type="password" :rules="[{ required: true }, { pattern: /^.{6,}$/, message: '密码至少6位' }]" />
          <van-field v-model="confirmPwd" placeholder="确认密码" type="password" :rules="[{ required: true }, { validator: () => password === confirmPwd, message: '密码不一致' }]" />
        </div>
        <van-button round block type="primary" native-type="submit" :loading="loading" size="large" style="height:54px">注 册</van-button>
      </van-form>
      <div class="auth-foot">已有账号？<router-link to="/login">登录</router-link></div>
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
.auth-head { display: flex; align-items: center; gap: 18px; margin-bottom: 24px; }
.ah-emoji { font-size: 44px; line-height: 1; flex-shrink: 0; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.10)); }
.ah-title { font-size: 28px; font-weight: 900; color: #1a1a1a; line-height: 1; margin-bottom: 4px; }
.ah-sub { font-size: 14px; color: #aaa; }

/* 角色选择卡片 */
.role-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 28px; }
.role-card {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  padding: 20px 16px 18px; border: 2px solid #eee; background: #fafafa;
  border-radius: 28px; cursor: pointer; transition: all 0.2s; position: relative;
}
.role-card:active { transform: scale(0.96); }
.role-card.active { border-color: #1a1a1a; background: #fff; box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
.rc-emoji { font-size: 38px; line-height: 1; }
.rc-info { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.rc-label { font-size: 18px; font-weight: 800; color: #1a1a1a; }
.rc-desc { font-size: 12px; color: #aaa; font-weight: 500; }
.rc-check {
  position: absolute; top: 8px; right: 8px;
  width: 26px; height: 26px; border-radius: 50%;
  background: #1a1a1a; display: flex; align-items: center; justify-content: center;
}

.input-box { background: #f5f3f0; border-radius: 28px; padding: 4px 0; margin-bottom: 28px; }
.input-box :deep(.van-field) { padding: 16px 20px; font-size: 16px; }
.auth-foot { text-align: center; margin-top: 24px; font-size: 15px; color: #aaa; }
.auth-foot a { color: #1a1a1a; text-decoration: none; font-weight: 700; }
</style>
