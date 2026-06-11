/**
 * Vue Router 路由配置
 * - 未登录自动跳转登录页
 * - 商家路由需要 merchant 角色，登录后跳转商家首页
 * - 用户路由显示用户底部导航，商家路由显示商家底部导航
 */
import { createRouter, createWebHashHistory } from 'vue-router'
import { showDialog } from 'vant'

const S = sessionStorage

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', redirect: '/home' },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/pages/Login.vue'),
      meta: { title: '登录', noAuth: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/pages/Register.vue'),
      meta: { title: '注册', noAuth: true },
    },
    // ===== 用户路由 =====
    {
      path: '/home',
      name: 'Home',
      component: () => import('@/pages/Home.vue'),
      meta: { title: '菜单', showNav: 'user' },
    },
    {
      path: '/dish/:id',
      name: 'DishDetail',
      component: () => import('@/pages/DishDetail.vue'),
      meta: { title: '菜品详情' },
    },
    {
      path: '/cart',
      name: 'Cart',
      component: () => import('@/pages/Cart.vue'),
      meta: { title: '购物车', showNav: 'user' },
    },
    {
      path: '/orders',
      name: 'OrderList',
      component: () => import('@/pages/OrderList.vue'),
      meta: { title: '订单', showNav: 'user' },
    },
    {
      path: '/orders/:id',
      name: 'OrderDetail',
      component: () => import('@/pages/OrderDetail.vue'),
      meta: { title: '订单详情' },
    },
    {
      path: '/payment/:orderId',
      name: 'Payment',
      component: () => import('@/pages/Payment.vue'),
      meta: { title: '支付' },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/pages/Profile.vue'),
      meta: { title: '我的', showNav: 'user' },
    },
    // ===== 商家路由（精简为2个页面） =====
    {
      path: '/merchant',
      name: 'MerchantHome',
      component: () => import('@/pages/Merchant/MerchantMain.vue'),
      meta: { title: '管理', showNav: 'merchant', requireMerchant: true },
    },
    {
      path: '/merchant/profile',
      name: 'MerchantProfile',
      component: () => import('@/pages/Merchant/MerchantProfile.vue'),
      meta: { title: '我的', showNav: 'merchant', requireMerchant: true },
    },
  ],
})

// 路由守卫
router.beforeEach((to) => {
  const token = S.getItem('access_token')
  const userInfo = JSON.parse(S.getItem('user_info') || 'null')

  // 未登录跳转登录页
  if (!to.meta.noAuth && !token && to.name !== 'Login' && to.name !== 'Register') {
    showDialog({ title: '提示', message: '请先登录', confirmButtonColor: '#1a1a1a' }).catch(() => {})
    return { name: 'Login' }
  }

  // 商家路由权限校验
  if (to.meta.requireMerchant && userInfo?.role !== 'merchant') {
    showDialog({ title: '提示', message: '仅商家可访问', confirmButtonColor: '#1a1a1a' }).catch(() => {})
    return { name: 'Home' }
  }

  // 商家不能访问用户页面（购物车等）
  const userOnlyRoutes = ['Cart', 'Home', 'DishDetail', 'Payment']
  if (userInfo?.role === 'merchant' && userOnlyRoutes.includes(to.name as string)) {
    return { name: 'MerchantHome' }
  }

  // 用户不能访问商家页面
  const merchantOnlyRoutes = ['MerchantHome', 'MerchantProfile']
  if (userInfo?.role !== 'merchant' && merchantOnlyRoutes.includes(to.name as string)) {
    return { name: 'Home' }
  }
})

export default router
