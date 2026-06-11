<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { orderApi } from '@/api/order'

const router = useRouter()
const tabs = [
  { key: '', name: '全部' },
  { key: 'pending_payment', name: '待支付' },
  { key: 'preparing', name: '备餐中' },
  { key: 'waiting_pickup', name: '待取餐' },
  { key: 'completed', name: '已完成' },
]
const activeTab = ref(0); const orders = ref<any[]>([]); const loading = ref(false)
const tx: Record<string, string> = { pending_payment: '待支付', preparing: '备餐中', waiting_pickup: '待取餐', completed: '已完成', cancelled: '已取消' }

async function loadOrders() {
  loading.value = true
  try { const s = tabs[activeTab.value]?.key; const r: any = await orderApi.getList(s || undefined); orders.value = r.data }
  catch {} finally { loading.value = false }
}

onMounted(loadOrders)
</script>

<template>
  <div class="m-page">
    <div class="page-header">
      <div class="page-title">我的订单</div>
    </div>

    <div class="tab-scroll">
      <div class="tab-pills">
        <button v-for="(t, i) in tabs" :key="t.key"
          :class="['pill', { active: activeTab === i }]"
          @click="activeTab = i; loadOrders()">{{ t.name }}</button>
      </div>
    </div>

    <van-loading v-if="loading" size="24" style="margin:50px 0;text-align:center" />
    <van-empty v-else-if="orders.length === 0" description="暂无订单" image-size="120" />

    <div v-else class="order-list">
      <div v-for="o in orders" :key="o.order_id" class="order-card" @click="router.push(`/orders/${o.order_id}`)">
        <div class="oc-top">
          <span class="oc-id">#{{ o.order_id }}</span>
          <span :class="['status-tag', `status-tag--${o.order_status}`]">{{ tx[o.order_status] }}</span>
        </div>
        <div class="oc-items">
          <div v-for="item in o.items.slice(0, 3)" :key="item.order_item_id" class="oc-row">
            <span class="oc-name">{{ item.dish_name }}</span>
            <span class="oc-qty">x{{ item.quantity }}</span>
          </div>
          <div v-if="o.items.length > 3" class="oc-more">还有 {{ o.items.length - 3 }} 件商品</div>
        </div>
        <div class="oc-bottom">
          <span class="oc-time">{{ o.create_time }}</span>
          <span class="oc-total">¥{{ o.total_money }}</span>
        </div>
        <div v-if="o.order_status === 'pending_payment'" class="oc-action">
          <button class="oc-btn" @click.stop="router.push(`/payment/${o.order_id}`)">支付</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 90px; }
.page-header { padding: 20px 20px 6px; }
.page-title { font-size: 28px; font-weight: 900; color: #1a1a1a; padding: 0 4px; }
.tab-scroll { padding: 8px 24px 18px; overflow-x: auto; scrollbar-width: none; }
.tab-scroll::-webkit-scrollbar { display: none; }
.tab-pills { display: flex; gap: 12px; width: max-content; }
.pill { padding: 12px 24px; border-radius: 32px; font-size: 15px; font-weight: 600; background: #fff; color: #888; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.04); white-space: nowrap; }
.pill:active { transform: scale(0.94); }
.pill.active { background: #1a1a1a; color: #fff; font-weight: 700; box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
.order-list { padding: 10px 24px 20px; }
.order-card { background: #fff; border-radius: 28px; padding: 20px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.oc-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.oc-id { font-size: 15px; font-weight: 700; color: #1a1a1a; }
.oc-items { padding: 10px 0; }
.oc-row { display: flex; justify-content: space-between; align-items: center; padding: 5px 0; }
.oc-name { font-size: 15px; font-weight: 600; color: #1a1a1a; }
.oc-qty { font-size: 14px; color: #888; }
.oc-more { font-size: 13px; color: #bbb; padding: 5px 0; }
.oc-bottom { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; border-top: 2px solid #f5f3f0; }
.oc-time { font-size: 12px; color: #bbb; }
.oc-total { font-weight: 800; color: #ff6b6b; font-size: 20px; }
.oc-action { text-align: right; margin-top: 12px; }
.oc-btn { padding: 10px 24px; border: none; border-radius: 22px; background: #1a1a1a; color: #fff; font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.oc-btn:active { transform: scale(0.94); }
</style>
