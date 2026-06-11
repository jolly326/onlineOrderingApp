<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import 'vant/lib/index.css'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const cartStore = useCartStore()
const userStore = useUserStore()

const showNav = computed(() => route.meta.showNav as string | undefined)

onMounted(() => {
  userStore.restore()
  if (userStore.isLogin && !userStore.isMerchant) cartStore.fetchCart()
})
</script>

<template>
  <div>
    <router-view />

    <!-- 统一底部导航（用户和商家同款深色风格） -->
    <div v-if="showNav === 'user'" class="bottom-nav">
      <button :class="['bn-btn', { active: $route.path === '/home' }]" @click="router.push('/home')">
        <van-icon name="home-o" size="22" /><span>菜单</span>
      </button>
      <button :class="['bn-btn', { active: $route.path === '/cart' }]" @click="router.push('/cart')">
        <van-icon name="cart-o" size="22" /><span>购物车</span>
        <span v-if="cartStore.itemCount" class="bn-badge">{{ cartStore.itemCount }}</span>
      </button>
      <button :class="['bn-btn', { active: $route.path.startsWith('/orders') }]" @click="router.push('/orders')">
        <van-icon name="orders-o" size="22" /><span>订单</span>
      </button>
      <button :class="['bn-btn', { active: $route.path === '/profile' }]" @click="router.push('/profile')">
        <van-icon name="contact-o" size="22" /><span>我的</span>
      </button>
    </div>

    <div v-if="showNav === 'merchant'" class="bottom-nav">
      <button :class="['bn-btn', { active: $route.path === '/merchant' }]" @click="router.push('/merchant')">
        <van-icon name="shop-o" size="22" /><span>管理</span>
      </button>
      <button :class="['bn-btn', { active: $route.path === '/merchant/profile' }]" @click="router.push('/merchant/profile')">
        <van-icon name="manager-o" size="22" /><span>我的</span>
      </button>
    </div>
  </div>
</template>

<style>
@import './style.css';

.bottom-nav {
  position: fixed; bottom: 20px; left: 20px; right: 20px;
  display: flex; background: linear-gradient(135deg, #111 0%, #1a1a1a 100%);
  border-radius: 32px; padding: 8px 10px;
  box-shadow: 0 12px 36px rgba(0,0,0,0.24);
  border: 1px solid rgba(255,255,255,0.06);
  z-index: 99; justify-content: space-around;
}
.bn-btn {
  position: relative; flex: 1;
  display: flex; flex-direction: column; align-items: center; gap: 3px;
  padding: 10px 6px 8px; border: none; background: transparent;
  border-radius: 22px; cursor: pointer; font-size: 12px;
  color: rgba(255,255,255,0.62); transition: all 0.2s;
}
.bn-btn.active {
  background: #fff; color: #1a1a1a; font-weight: 700;
  box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}
.bn-btn .van-icon { font-size: 24px !important; }
.bn-badge {
  position: absolute; top: 2px; right: 50%;
  transform: translateX(18px); min-width: 20px; height: 20px;
  background: #ff6b6b; color: #fff; font-size: 11px; font-weight: 700;
  border-radius: 10px; display: flex; align-items: center;
  justify-content: center; padding: 0 6px;
}
</style>
