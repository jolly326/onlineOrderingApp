<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showDialog, showToast } from 'vant'
import { useCartStore } from '@/stores/cart'
import { orderApi } from '@/api/order'

const router = useRouter(); const cartStore = useCartStore(); const loading = ref(false)
onMounted(() => { cartStore.fetchCart() })

async function handleQtyChange(itemId: string, newQty: number) {
  if (newQty <= 0) { await cartStore.removeItem(itemId) }
  else { await cartStore.updateItem(itemId, newQty) }
}

function handleClear() { showDialog({ title: '提示', message: '清空购物车吗？', showCancelButton: true, cancelButtonColor: '#aaa' }).then(() => cartStore.clearCart()).catch(() => {}) }
async function handleCheckout() {
  if (!cartStore.items.length) { showToast('购物车是空的'); return }
  loading.value = true
  try { const r: any = await orderApi.create(); showToast('订单已创建'); router.push(`/payment/${r.data.order.order_id}`) }
  catch {} finally { loading.value = false }
}
</script>

<template>
  <div class="m-page">
    <div class="page-header">
      <div class="page-title">购物车</div>
      <div class="page-actions">
        <span v-if="cartStore.items.length" class="count-badge">{{ cartStore.itemCount }}</span>
        <button v-if="cartStore.items.length" class="head-clear" @click="handleClear">清空</button>
      </div>
    </div>

    <div v-if="!cartStore.items.length" class="empty-state">
      <div class="empty-icon">🛒</div>
      <p class="empty-text">购物车是空的</p>
      <button class="primary-btn" @click="router.push('/home')">去点餐</button>
    </div>

    <div v-else class="item-list">
      <div v-for="item in cartStore.items" :key="item.item_id" class="item-card">
        <div class="item-img">
          <van-image v-if="item.dish.image" :src="item.dish.image" fit="cover" width="80" height="80" round />
          <div v-else class="item-img-ph">☕</div>
        </div>
        <div class="item-info">
          <div class="item-name">{{ item.dish.dish_name }}</div>
          <div class="item-price">¥<strong>{{ item.dish.price }}</strong></div>
        </div>
        <div class="item-stepper">
          <van-stepper :model-value="item.quantity" min="0" max="99" theme="round" button-size="30" input-width="36" @change="(v: number) => handleQtyChange(item.item_id, v)" />
        </div>
      </div>
    </div>

    <div v-if="cartStore.items.length" class="cart-bar">
      <div class="bar-total">合计 <strong>¥{{ cartStore.total.toFixed(2) }}</strong></div>
      <button class="primary-btn" :disabled="loading" @click="handleCheckout">{{ loading ? '提交中...' : '结算' }}</button>
    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 130px; }

.page-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 20px 6px;
}
.page-title { font-size: 28px; font-weight: 900; color: #1a1a1a; padding: 0 4px; }
.page-actions { display: flex; align-items: center; gap: 10px; }
.count-badge {
  background: #1a1a1a; color: #fff; font-size: 16px; font-weight: 700;
  width: 36px; height: 36px; border-radius: 50%; display: flex;
  align-items: center; justify-content: center;
}
.head-clear {
  padding: 8px 18px; border: 2px solid #ddd; border-radius: 20px;
  background: #fff; font-size: 14px; font-weight: 600; color: #888;
  cursor: pointer; transition: all 0.2s;
}
.head-clear:active { transform: scale(0.94); background: #f5f5f5; }

.empty-state { text-align: center; padding: 100px 20px; }
.empty-icon { font-size: 100px; line-height: 1; margin-bottom: 20px; }
.empty-text { color: #aaa; font-size: 18px; margin: 0 0 32px; }

.item-list { padding: 10px 24px; }
.item-card {
  display: flex; align-items: center; background: #fff; border-radius: 28px;
  padding: 14px 18px; margin-bottom: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.item-img { margin-right: 14px; flex-shrink: 0; }
.item-img-ph { width: 80px; height: 80px; background: #f0ebe6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; }
.item-info { flex: 1; min-width: 0; display: flex; flex-direction: column; justify-content: center; gap: 2px; }
.item-name { font-size: 18px; font-weight: 700; color: #1a1a1a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.item-price { font-size: 16px; color: #ff6b6b; font-weight: 600; }
.item-price strong { font-size: 24px; font-weight: 800; }
.item-stepper { flex-shrink: 0; margin-left: 10px; }

.cart-bar {
  position: fixed; bottom: 115px; left: 20px; right: 20px;
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; background: #fff; border-radius: 32px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02), 0 8px 24px rgba(0,0,0,0.06), 0 20px 48px rgba(0,0,0,0.04);
}
.bar-total { text-align: left; font-size: 14px; color: #888; flex: 1; }
.bar-total strong { font-size: 26px; color: #ff6b6b; font-weight: 800; }
.primary-btn { padding: 16px 24px; border: none; border-radius: 28px; background: #1a1a1a; color: #fff; font-size: 17px; font-weight: 800; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.primary-btn:active { transform: scale(0.96); }
.primary-btn:disabled { opacity: 0.6; }
</style>
