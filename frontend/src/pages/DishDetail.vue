<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import { dishApi } from '@/api/dish'
import { useCartStore } from '@/stores/cart'

const route = useRoute(); const router = useRouter(); const cartStore = useCartStore()
const dish = ref<any>(null); const qty = ref(1)
const total = computed(() => (dish.value?.price * qty.value).toFixed(2))

onMounted(async () => {
  try { const res: any = await dishApi.getDetail(route.params.id as string); dish.value = res.data }
  catch { router.back() }
})

function addToCart() {
  if (!dish.value) return
  cartStore.addDish(dish.value.dish_id, qty.value)
  showToast({ message: `已添加 x${qty.value}`, icon: 'success', duration: 1200 })
}
</script>

<template>
  <div class="m-page" v-if="dish">
    <div class="page-header">
      <button class="back-btn" @click="router.back()"><van-icon name="arrow-left" size="20" color="#fff" /></button>
      <div class="page-title">菜品详情</div>
    </div>

    <div class="detail-img">
      <van-image v-if="dish.image" :src="dish.image" fit="cover" width="100%" height="220" />
      <div v-else class="di-ph">☕</div>
    </div>

    <div class="detail-card">
      <div class="dc-top">
        <div class="dc-name">{{ dish.dish_name }}</div>
        <div class="dc-price">¥<strong>{{ dish.price }}</strong></div>
      </div>
      <div class="dc-sales">月售 {{ dish.month_sales || 0 }}</div>
      <div class="dc-divider"></div>
      <div class="dc-row">
        <span class="dc-label">数量</span>
        <van-stepper v-model="qty" min="1" max="99" theme="round" button-size="34" input-width="40" />
      </div>
    </div>

    <div class="action-bar">
      <button class="add-btn" @click="addToCart">加入 ¥{{ total }}</button>
    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 100px; }

.page-header { display: flex; align-items: center; gap: 14px; padding: 20px 20px 6px; }
.back-btn { width: 48px; height: 48px; border-radius: 50%; border: none; background: #1a1a1a; display: flex; align-items: center; justify-content: center; cursor: pointer; flex-shrink: 0; transition: transform 0.15s; }
.back-btn:active { transform: scale(0.9); }
.page-title { font-size: 26px; font-weight: 900; color: #1a1a1a; }

.detail-img { margin: 6px 20px 0; border-radius: 32px; overflow: hidden; }
.di-ph { width: 100%; height: 220px; background: linear-gradient(135deg, #f0ebe6, #e8e0d8); display: flex; align-items: center; justify-content: center; font-size: 60px; }

.detail-card { margin: 0 20px; background: #fff; border-radius: 32px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
.dc-top { display: flex; justify-content: space-between; align-items: flex-start; }
.dc-name { font-size: 24px; font-weight: 800; color: #1a1a1a; flex: 1; margin-right: 12px; }
.dc-price { color: #ff6b6b; font-size: 15px; flex-shrink: 0; }
.dc-price strong { font-size: 32px; font-weight: 800; }
.dc-sales { font-size: 14px; color: #aaa; margin-top: 6px; }
.dc-divider { height: 2px; background: #f5f3f0; margin: 18px 0; border-radius: 1px; }
.dc-row { display: flex; justify-content: space-between; align-items: center; }
.dc-label { font-size: 17px; font-weight: 600; color: #1a1a1a; }

.action-bar { padding: 20px 20px 30px; }
.add-btn { width: 100%; padding: 18px; border: none; border-radius: 28px; background: #1a1a1a; color: #fff; font-size: 18px; font-weight: 800; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.15); transition: all 0.2s; }
.add-btn:active { transform: scale(0.97); }
</style>
