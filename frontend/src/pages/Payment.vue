<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import { orderApi } from '@/api/order'
import { paymentApi } from '@/api/payment'

const route = useRoute(); const router = useRouter()
const order = ref<any>(null); const payType = ref('wechat'); const loading = ref(false)
const paid = ref(false); const payOk = ref(false)

onMounted(async () => {
  try { const r: any = await orderApi.getDetail(route.params.orderId as string); order.value = r.data }
  catch { router.push('/orders') }
})

async function handlePay() {
  loading.value = true
  try {
    const r: any = await paymentApi.pay(route.params.orderId as string, payType.value)
    payOk.value = r.data.pay_status === 'success'
    paid.value = true
    if (payOk.value) showToast('支付成功')
    else showToast('支付失败')
  } catch {} finally { loading.value = false }
}
</script>

<template>
  <div class="m-page">
    <div class="page-header">
      <button class="back-btn" @click="paid && payOk ? router.push('/orders') : router.back()">
        <van-icon name="arrow-left" size="20" color="#fff" />
      </button>
      <div class="page-title">{{ paid ? '支付结果' : '支付' }}</div>
    </div>

    <!-- 支付结果状态 -->
    <div v-if="paid" class="result-card">
      <div v-if="payOk" class="rc-icon rc-ok">✅</div>
      <div v-else class="rc-icon rc-fail"><van-icon name="cross" size="40" color="#ff6b6b" /></div>
      <div class="rc-title">{{ payOk ? '支付成功' : '支付失败' }}</div>
      <div class="rc-desc">{{ payOk ? '已通知商家，请等待备餐' : '请重试或换个方式支付' }}</div>
      <div v-if="payOk" class="rc-id">{{ order?.order_id }}</div>
    </div>

    <!-- 支付金额 -->
    <div v-if="!paid" class="amount-card">
      <div class="ac-label">支付金额</div>
      <div class="ac-value">¥{{ order?.total_money || '0.00' }}</div>
    </div>

    <!-- 支付方式选择 -->
    <div v-if="!paid" class="section-bar"><span class="section-dot"></span>支付方式</div>
    <div v-if="!paid" class="pay-options">
      <div :class="['po-item', { active: payType === 'wechat' }]" @click="payType = 'wechat'">
        <span class="po-icon">💚</span>
        <span class="po-label">微信支付</span>
        <van-icon name="success" :color="payType === 'wechat' ? '#1a1a1a' : '#eee'" size="22" />
      </div>
      <div :class="['po-item', { active: payType === 'alipay' }]" @click="payType = 'alipay'">
        <span class="po-icon">💙</span>
        <span class="po-label">支付宝</span>
        <van-icon name="success" :color="payType === 'alipay' ? '#1a1a1a' : '#eee'" size="22" />
      </div>
    </div>

    <!-- 订单信息 -->
    <div v-if="order" class="section-bar"><span class="section-dot"></span>订单信息</div>
    <div v-if="order" class="info-card">
      <div class="i-row"><span>编号</span><span>{{ order.order_id }}</span></div>
      <div class="i-row"><span>时间</span><span>{{ order.create_time }}</span></div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-bar">
      <button v-if="!paid" class="primary-btn" :disabled="loading" @click="handlePay">
        {{ loading ? '支付中...' : `支付 ¥${order?.total_money || '0.00'}` }}
      </button>
      <template v-if="paid">
        <button v-if="payOk" class="primary-btn" @click="router.push('/orders')">订单</button>
        <button v-else class="primary-btn" @click="paid = false; payOk = false">重试</button>
        <button class="ghost-btn" @click="router.push('/home')">首页</button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 100px; }

.page-header { display: flex; align-items: center; gap: 14px; padding: 20px 20px 6px; }
.back-btn { width: 48px; height: 48px; border-radius: 50%; border: none; background: #1a1a1a; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: transform 0.15s; }
.back-btn:active { transform: scale(0.9); }
.page-title { font-size: 26px; font-weight: 900; color: #1a1a1a; }

/* 支付结果 */
.result-card { background: #fff; border-radius: 32px; padding: 50px 24px; text-align: center; margin: 6px 20px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.rc-icon { margin: 0 auto; }
.rc-ok { font-size: 70px; line-height: 1; }
.rc-fail { width: 90px; height: 90px; background: #fce4ec; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.rc-title { font-size: 28px; font-weight: 900; color: #1a1a1a; margin: 20px 0 8px; }
.rc-desc { font-size: 16px; color: #aaa; }
.rc-id { font-size: 15px; color: #ccc; margin-top: 12px; }

/* 支付金额 */
.amount-card { background: #fff; border-radius: 32px; padding: 40px; text-align: center; margin: 6px 20px 18px; box-shadow: 0 4px 14px rgba(0,0,0,0.05); }
.ac-label { font-size: 16px; color: #aaa; margin-bottom: 10px; }
.ac-value { font-size: 52px; font-weight: 800; color: #ff6b6b; }

.section-bar { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1a1a1a; padding: 0 24px 10px; }
.section-dot { width: 10px; height: 10px; border-radius: 50%; background: #1a1a1a; flex-shrink: 0; }

.pay-options { padding: 0 20px; }
.po-item { display: flex; align-items: center; gap: 16px; background: #fff; border-radius: 28px; padding: 20px; margin-bottom: 12px; border: 3px solid transparent; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.po-item.active { border-color: #1a1a1a; }
.po-icon { font-size: 28px; line-height: 1; }
.po-label { flex: 1; font-size: 18px; font-weight: 500; }

.info-card { margin: 0 20px 18px; background: #fff; border-radius: 28px; padding: 18px 22px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.i-row { display: flex; justify-content: space-between; font-size: 16px; padding: 10px 0; color: #888; }
.i-row span:last-child { color: #555; }

.action-bar { padding: 6px 20px 30px; display: flex; flex-direction: column; gap: 12px; }
.primary-btn { width: 100%; padding: 18px; border: none; border-radius: 28px; background: #1a1a1a; color: #fff; font-size: 18px; font-weight: 800; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.15); transition: all 0.2s; }
.primary-btn:active { transform: scale(0.97); }
.primary-btn:disabled { opacity: 0.6; }
.ghost-btn { width: 100%; padding: 16px; border-radius: 28px; border: 2.5px solid #1a1a1a; background: transparent; color: #1a1a1a; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.ghost-btn:active { background: #f5f5f5; }
</style>
