<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { dishApi } from '@/api/dish'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cartStore = useCartStore()
const categories = [
  { key: '', name: '全部', icon: '🔥' },
  { key: 'drinks', name: '饮品', icon: '🧋' },
  { key: 'snacks', name: '小吃', icon: '🍟' },
  { key: 'recommended', name: '推荐', icon: '👍' },
]
const activeCategory = ref('')
const dishes = ref<any[]>([])
const loading = ref(false)

async function loadDishes() {
  loading.value = true
  try {
    const cat = activeCategory.value || undefined
    const res: any = await dishApi.getList(cat)
    dishes.value = res.data
  } catch {} finally { loading.value = false }
}

async function addToCart(dishId: string) {
  await cartStore.addDish(dishId, 1)
  showToast({ message: '已加入购物车', icon: 'success', duration: 1000 })
}

watch(activeCategory, loadDishes)
onMounted(() => { loadDishes(); cartStore.fetchCart() })
</script>

<template>
  <div class="m-page">
    <div class="page-header">
      <div class="page-title">今日菜单</div>
    </div>

    <div class="cat-grid">
      <button v-for="cat in categories" :key="cat.key"
        :class="['cat-btn', { active: activeCategory === cat.key }]"
        @click="activeCategory = cat.key">
        <span class="cat-icon">{{ cat.icon }}</span>
        <span class="cat-name">{{ cat.name }}</span>
      </button>
    </div>

    <div class="section-bar">
      <span class="section-dot"></span>
      {{ activeCategory ? categories.find(c => c.key === activeCategory)?.name : '全部' }}菜单
    </div>

    <van-loading v-if="loading" size="28" style="margin:40px 0;text-align:center" />
    <van-empty v-else-if="dishes.length === 0" image-size="120" />

    <div v-else class="dish-grid">
      <div v-for="dish in dishes" :key="dish.dish_id" class="dish-card" @click="router.push(`/dish/${dish.dish_id}`)">
        <div class="dc-img">
          <van-image v-if="dish.image" :src="dish.image" fit="cover" width="100%" height="150" />
          <div v-else class="dc-img-ph"><span style="font-size:40px">☕</span></div>
        </div>
        <div class="dc-body">
          <div class="dc-info">
            <div class="dc-name">{{ dish.dish_name }}</div>
            <span class="dc-price"><small>¥</small><strong>{{ dish.price }}</strong></span>
          </div>
          <button class="dc-add" @click.stop="addToCart(dish.dish_id)">
            <van-icon name="plus" size="22" color="#fff" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 100px; }

.page-header { padding: 20px 20px 6px; }
.page-title { font-size: 28px; font-weight: 900; color: #1a1a1a; padding: 0 4px; }

.cat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; padding: 10px 24px 20px; }
.cat-btn {
  display: flex; flex-direction: column; align-items: center; gap: 10px;
  padding: 16px 12px 14px; border: none; background: #fff; border-radius: 28px;
  cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.cat-btn:active { transform: scale(0.94); }
.cat-btn.active { background: #1a1a1a; box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
.cat-icon { font-size: 36px; line-height: 1; }
.cat-name { font-size: 15px; font-weight: 500; color: #888; }
.cat-btn.active .cat-name { color: #fff; font-weight: 700; }

.section-bar { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1a1a1a; padding: 10px 24px 8px; }
.section-dot { width: 10px; height: 10px; border-radius: 50%; background: #1a1a1a; flex-shrink: 0; }

.dish-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; padding: 14px 24px 90px; }
.dish-card { background: #fff; border-radius: 28px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.2s; }
.dish-card:active { transform: scale(0.95); }
.dc-img { height: 150px; overflow: hidden; }
.dc-img-ph { width: 100%; height: 100%; background: #f0ebe6; display: flex; align-items: center; justify-content: center; }
.dc-body { padding: 12px; display: flex; gap: 8px; align-items: center; }
.dc-info { flex: 1; display: flex; flex-direction: column; justify-content: center; min-width: 0; gap: 2px; }
.dc-name { font-size: 18px; font-weight: 700; color: #1a1a1a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.dc-price small { font-size: 14px; color: #ff6b6b; }
.dc-price strong { font-size: 26px; font-weight: 800; color: #ff6b6b; }
.dc-add {
  width: 52px; height: 52px; border-radius: 50%; border: none; background: #1a1a1a;
  display: flex; align-items: center; justify-content: center; cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: transform 0.2s; flex-shrink: 0;
}
.dc-add:active { transform: scale(0.88); }
</style>
