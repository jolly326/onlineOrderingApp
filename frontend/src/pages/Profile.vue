<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import { useUserStore } from '@/stores/user'
import { userApi } from '@/api/user'
import { orderApi } from '@/api/order'

const router = useRouter(); const userStore = useUserStore()
const showNameDialog = ref(false); const newName = ref('')
const orderCounts = ref<Record<string, number>>({})
const loading = ref(true)

onMounted(async () => {
  if (userStore.userInfo) newName.value = userStore.userInfo.username
  try {
    const r: any = await orderApi.getOrderCount()
    orderCounts.value = r.data
  } catch {} finally { loading.value = false }
})

function handleLogout() {
  showDialog({
    title: '提示', message: '确定退出登录吗？',
    showCancelButton: true, confirmButtonColor: '#ff6b6b', cancelButtonColor: '#aaa',
  }).then(() => { userStore.logout(); showToast('已退出'); router.push('/login') }).catch(() => {})
}
function openNameEdit() { newName.value = userStore.userInfo?.username || ''; showNameDialog.value = true }
async function saveName() {
  if (!newName.value.trim()) return
  try { await userApi.updateProfile({ username: newName.value }); await userStore.refreshProfile(); showNameDialog.value = false; showToast('已更新') } catch {}
}
function openAbout() { showDialog({ title: '关于我们', message: '在线点餐平台 v1.0\n\n专注为您提供便捷、快速的点餐体验。' }).catch(() => {}) }
</script>

<template>
  <div class="m-page">
    <!-- 顶部欢迎（与管理页一致） -->
    <div class="page-header">
      <div class="welcome-card">
        <div class="wc-left">
          <span class="wc-emoji">🙋</span>
          <div class="wc-info">
            <div class="wc-greet">我的账号</div>
            <div class="wc-name">{{ userStore.userInfo?.username || '用户' }}</div>
            <div class="wc-phone">{{ userStore.userInfo?.phone || '未绑定手机' }}</div>
          </div>
        </div>
      </div>
    </div>

    <van-dialog v-model:show="showNameDialog" title="修改昵称" show-cancel-button @confirm="saveName" :confirm-button-color="'#1a1a1a'" :cancel-button-color="'#aaa'">
      <div class="dialog-input-wrap">
        <input v-model="newName" placeholder="请输入新昵称" maxlength="20" class="dialog-input" />
      </div>
    </van-dialog>

    <!-- 我的订单概览 -->
    <div class="section-bar"><span class="section-dot"></span>我的订单</div>
    <div v-if="!loading" class="order-stats">
      <div class="stat-card" @click="router.push('/orders')">
        <div class="sc-num">{{ orderCounts.pending_payment || 0 }}</div>
        <div class="sc-label">待支付</div>
      </div>
      <div class="stat-card" @click="router.push('/orders')">
        <div class="sc-num">{{ orderCounts.waiting_pickup || 0 }}</div>
        <div class="sc-label">待取餐</div>
      </div>
    </div>

    <!-- 设置菜单 -->
    <div class="section-bar"><span class="section-dot"></span>设置</div>
    <div class="settings-list">
      <div class="set-item" @click="openNameEdit">
        <span class="set-emoji">✏️</span>
        <span class="set-label">修改昵称</span>
        <van-icon name="arrow" color="#ddd" size="20" />
      </div>
      <div class="set-divider"></div>
      <div class="set-item" @click="openAbout">
        <span class="set-emoji">ℹ️</span>
        <span class="set-label">关于我们</span>
        <van-icon name="arrow" color="#ddd" size="20" />
      </div>
    </div>

    <div class="logout-wrap">
      <button class="logout-btn" @click="handleLogout">退出登录</button>
    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 100px; }

/* ===== 顶部欢迎（与管理页一致） ===== */
.page-header { padding: 20px 20px 8px; }
.welcome-card {
  display: flex; align-items: center; gap: 16px;
  background: linear-gradient(135deg, #fff 0%, #fcfcfc 100%);
  border-radius: 32px; padding: 20px 28px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02), 0 8px 24px rgba(0,0,0,0.06), 0 20px 48px rgba(0,0,0,0.04);
}
.wc-left { display: flex; align-items: center; gap: 16px; }
.wc-emoji { font-size: 38px; line-height: 1; flex-shrink: 0; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.10)); }
.wc-info { display: flex; flex-direction: column; gap: 4px; }
.wc-greet { font-size: 14px; color: #aaa; font-weight: 500; }
.wc-name { font-size: 26px; font-weight: 900; color: #1a1a1a; line-height: 1; }
.wc-phone { font-size: 15px; color: #aaa; margin-top: 2px; }

/* ===== section ===== */
.section-bar { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1a1a1a; padding: 14px 24px 10px; }
.section-dot { width: 10px; height: 10px; border-radius: 50%; background: #1a1a1a; flex-shrink: 0; }

/* ===== 订单统计卡片 ===== */
.order-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 0 24px 4px; }
.stat-card {
  background: #fff; border-radius: 24px; padding: 20px 10px 16px;
  text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  cursor: pointer; transition: all 0.2s;
}
.stat-card:active { transform: scale(0.94); }
.sc-num { font-size: 32px; font-weight: 900; color: #1a1a1a; margin-bottom: 6px; }
.sc-label { font-size: 14px; color: #888; font-weight: 600; }

/* ===== 设置菜单（与管理页一致） ===== */
.settings-list {
  margin: 0 24px; background: #fff; border-radius: 28px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05); overflow: hidden;
}
.set-item {
  display: flex; align-items: center; gap: 16px;
  padding: 20px 24px; cursor: pointer; transition: background 0.2s;
}
.set-item:active { background: #f8f6f4; }
.set-emoji { font-size: 28px; line-height: 1; flex-shrink: 0; }
.set-label { flex: 1; font-size: 18px; font-weight: 700; color: #1a1a1a; }
.set-divider { height: 1px; background: #f0ede8; margin: 0 24px; }

/* ===== 退出 ===== */
.logout-wrap { padding: 24px 24px 30px; }
.logout-btn {
  width: 100%; padding: 16px; border: 2.5px solid #ff6b6b;
  border-radius: 28px; background: transparent; color: #ff6b6b;
  font-size: 18px; font-weight: 800; cursor: pointer;
  transition: all 0.2s;
}
.logout-btn:active { background: #fff5f5; transform: scale(0.97); }

/* ===== 弹窗 ===== */
.dialog-input-wrap { padding: 20px 24px 8px; }
.dialog-input { width: 100%; border: 2px solid #e0ddd8; background: #f9f8f6; border-radius: 16px; padding: 16px; font-size: 18px; outline: none; box-sizing: border-box; }
.dialog-input:focus { border-color: #1a1a1a; background: #fff; }
</style>
