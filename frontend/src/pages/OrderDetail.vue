<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderApi } from '@/api/order'

const route = useRoute(); const router = useRouter(); const order = ref<any>(null)
const tx: Record<string, string> = { pending_payment: '待支付', preparing: '备餐中', waiting_pickup: '待取餐', completed: '已完成', cancelled: '已取消' }
onMounted(async () => {
  try { const r: any = await orderApi.getDetail(route.params.id as string); order.value = r.data }
  catch { router.back() }
})
</script>

<template>
  <div class="m-page" v-if="order">
    <div class="page-header">
      <button class="back-btn" @click="router.back()"><van-icon name="arrow-left" size="20" color="#fff" /></button>
      <div class="page-title">订单详情</div>
    </div>

    <div class="status-card">
      <div class="sc-icon">
        <span v-if="order.order_status === 'waiting_pickup'" style="font-size:34px">🛍️</span>
        <span v-else-if="order.order_status === 'preparing'" style="font-size:34px">👨‍🍳</span>
        <van-icon v-else name="description" size="34" color="#1a1a1a" />
      </div>
      <div class="sc-info">
        <div class="sc-status">{{ tx[order.order_status] }}</div>
        <div class="sc-sub">
          <template v-if="order.pick_up_code">取餐码 <strong>{{ order.pick_up_code }}</strong></template>
          <template v-else>{{ order.create_time }}</template>
        </div>
      </div>
    </div>

    <div class="section-bar"><span class="section-dot"></span>商品清单</div>
    <div class="section-card">
      <div v-for="item in order.items" :key="item.order_item_id" class="s-row">
        <span>{{ item.dish_name }}</span><span>¥{{ item.price }} × {{ item.quantity }}</span>
      </div>
      <div class="s-divider"></div>
      <div class="s-total"><span>合计</span><span class="st-price">¥{{ order.total_money }}</span></div>
    </div>

    <div class="section-bar"><span class="section-dot"></span>订单信息</div>
    <div class="section-card">
      <div class="s-row"><span style="color:#888">编号</span><span>{{ order.order_id }}</span></div>
      <div class="s-row"><span style="color:#888">时间</span><span>{{ order.create_time }}</span></div>
      <div v-if="order.pick_up_code" class="s-row"><span style="color:#888">取餐码</span><span class="s-code">{{ order.pick_up_code }}</span></div>
    </div>

    <div class="action-bar">
      <button v-if="order.order_status === 'pending_payment'" class="primary-btn" @click="router.push(`/payment/${order.order_id}`)">支付</button>

    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 100px; }

.page-header { display: flex; align-items: center; gap: 14px; padding: 20px 20px 6px; }
.back-btn { width: 48px; height: 48px; border-radius: 50%; border: none; background: #1a1a1a; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: transform 0.15s; }
.back-btn:active { transform: scale(0.9); }
.page-title { font-size: 26px; font-weight: 900; color: #1a1a1a; }

.status-card { background: #fff; border-radius: 32px; padding: 28px 24px; display: flex; align-items: center; gap: 18px; margin: 6px 20px 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.sc-icon { width: 64px; height: 64px; background: #f5f3f0; border-radius: 22px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.sc-info { flex: 1; }
.sc-status { font-size: 22px; font-weight: 800; color: #1a1a1a; margin-bottom: 6px; }
.sc-sub { font-size: 15px; color: #888; }
.sc-sub strong { font-size: 28px; color: #1a1a1a; letter-spacing: 5px; margin-left: 8px; }

.section-bar { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1a1a1a; padding: 0 24px 10px; }
.section-dot { width: 10px; height: 10px; border-radius: 50%; background: #1a1a1a; flex-shrink: 0; }
.section-card { margin: 0 20px 18px; background: #fff; border-radius: 28px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.s-row { display: flex; justify-content: space-between; font-size: 16px; padding: 10px 0; color: #555; }
.s-divider { height: 2px; background: #f5f3f0; margin: 14px 0; border-radius: 1px; }
.s-total { display: flex; justify-content: space-between; font-size: 17px; font-weight: 600; color: #1a1a1a; }
.st-price { color: #ff6b6b; font-size: 22px; font-weight: 800; }
.s-code { color: #1a1a1a; font-weight: 700; font-size: 20px; letter-spacing: 4px; }

.action-bar { padding: 6px 20px 30px; display: flex; flex-direction: column; gap: 12px; }
.primary-btn { width: 100%; padding: 18px; border: none; border-radius: 28px; background: #1a1a1a; color: #fff; font-size: 18px; font-weight: 800; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.15); transition: all 0.2s; }
.primary-btn:active { transform: scale(0.97); }
.ghost-btn { width: 100%; padding: 16px; border-radius: 28px; border: 2.5px solid #1a1a1a; background: transparent; color: #1a1a1a; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.ghost-btn:active { background: #f5f5f5; }
</style>
