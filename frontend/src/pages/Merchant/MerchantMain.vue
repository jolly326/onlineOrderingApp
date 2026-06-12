<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { showToast, showDialog } from 'vant'
import { useUserStore } from '@/stores/user'
import { orderApi } from '@/api/order'
import { dishApi } from '@/api/dish'

const userStore = useUserStore()
const activeTab = ref(0)

// ============================
// 概况 tab
// ============================
const stats = ref<Record<string, any>>({})
const loadingStats = ref(true)

onMounted(async () => {
  try { const r: any = await orderApi.getMerchantStats(); stats.value = r.data } catch {}
  finally { loadingStats.value = false }
})

// ============================
// 订单 tab
// ============================
const orders = ref<any[]>([]); const loadingOrders = ref(false)
const orderFilter = ref(0)
const orderTabs = [
  { key: '', name: '全部' },
  { key: 'preparing', name: '待出餐' },
  { key: 'waiting_pickup', name: '待取餐' },
  { key: 'completed', name: '已完成' },
]
const tx: Record<string, string> = { pending_payment: '待支付', preparing: '备餐中', waiting_pickup: '待取餐', completed: '已完成', cancelled: '已取消' }

async function loadOrders() {
  loadingOrders.value = true
  try { const s = orderTabs[orderFilter.value]?.key; const r: any = await orderApi.getMerchantList(s || undefined); orders.value = r.data }
  catch {} finally { loadingOrders.value = false }
}

function handleComplete(orderId: string) {
  showDialog({
    title: '出餐', message: '确认已备餐完成？',
    showCancelButton: true, confirmButtonColor: '#1a1a1a', cancelButtonColor: '#aaa',
  }).then(async () => {
    try { await orderApi.updateStatus(orderId, 'waiting_pickup'); showToast('已出餐'); loadOrders() } catch {}
  }).catch(() => {})
}

const pickupCode = ref('')
const confirmPickupOrderId = ref('')
const showPickupDialog = ref(false)

function openPickupDialog(orderId: string) {
  confirmPickupOrderId.value = orderId
  pickupCode.value = ''
  showPickupDialog.value = true
}

async function handlePickupConfirm() {
  if (!pickupCode.value.trim()) { showToast('请输入取餐码'); return }
  try {
    const r: any = await orderApi.merchantConfirmPickup(confirmPickupOrderId.value, pickupCode.value.trim())
    if (r.code !== 200) { throw r }
    showPickupDialog.value = false
    showToast('取餐确认成功')
    loadOrders()
  } catch (e: any) {
    showPickupDialog.value = false
    const msg = e?.message || '取餐码错误'
    showToast(msg)
  }
}

// ============================
// 菜品 tab
// ============================
const dishes = ref<any[]>([]); const loadingDishes = ref(false)
const showDishPopup = ref(false); const showCategoryPicker = ref(false)
const popupMode = ref<'add' | 'edit'>('add')
const editingDishId = ref('')
const newDish = ref({ dish_name: '', price: '', category: 'recommended' })
const uploadFile = ref<File | null>(null)
const previewUrl = ref('')
const imageRemoved = ref(false)

function triggerUpload() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e: Event) => {
    const target = e.target as HTMLInputElement
    if (!target.files || !target.files[0]) return
    const file = target.files[0]
    uploadFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
  input.click()
}
const categories = [
  { value: 'recommended', label: '推荐' }, { value: 'signature', label: '招牌' },
  { value: 'drinks', label: '饮品' }, { value: 'snacks', label: '小吃' },
]
const popupTitle = computed(() => popupMode.value === 'add' ? '新增菜品' : '编辑菜品')
const submitText = computed(() => popupMode.value === 'add' ? '确认添加' : '保存修改')

async function loadDishes() {
  loadingDishes.value = true
  try { const r: any = await dishApi.getAll(); dishes.value = r.data } catch {} finally { loadingDishes.value = false }
}

async function toggleDish(dish: any) {
  const ns = !dish.status
  try { await dishApi.updateStatus(dish.dish_id, ns); dish.status = ns; showToast(ns ? '已上架' : '已下架') } catch {}
}

function removeImage() {
  uploadFile.value = null
  previewUrl.value = ''
  imageRemoved.value = true
}

function openAddPopup() {
  popupMode.value = 'add'; editingDishId.value = ''
  newDish.value = { dish_name: '', price: '', category: 'recommended' }
  uploadFile.value = null; previewUrl.value = ''; imageRemoved.value = false
  showDishPopup.value = true
}

function openEditPopup(dish: any) {
  popupMode.value = 'edit'; editingDishId.value = dish.dish_id
  newDish.value = { dish_name: dish.dish_name, price: String(dish.price), category: dish.category }
  const img = Array.isArray(dish.images) && dish.images.length ? dish.images[0] : ''
  previewUrl.value = img
  uploadFile.value = null; imageRemoved.value = false
  showDishPopup.value = true
}

function closePopup() { showDishPopup.value = false; popupMode.value = 'add' }

function selectCategory(val: string) { newDish.value.category = val; showCategoryPicker.value = false }

function getCategoryLabel(v?: string) { return categories.find(c => c.value === (v || newDish.value.category))?.label || '推荐' }

async function saveDish() {
  if (!newDish.value.dish_name.trim() || !newDish.value.price) { showToast('请填写完整信息'); return }
  try {
    const fd = new FormData()
    fd.append('dish_name', newDish.value.dish_name)
    fd.append('price', newDish.value.price)
    fd.append('category', newDish.value.category)
    if (uploadFile.value) {
      fd.append('image', uploadFile.value)
    } else if (imageRemoved.value) {
      fd.append('remove_image', 'true')
    }
    if (popupMode.value === 'add') { await dishApi.create(fd); showToast('添加成功') }
    else { await dishApi.update(editingDishId.value, fd); showToast('修改成功') }
    closePopup(); loadDishes()
  } catch {}
}

function confirmDelete(dishId: string, name: string) {
  showDialog({
    title: '确认删除', message: `确定删除菜品"${name}"吗？`,
    showCancelButton: true, confirmButtonColor: '#1a1a1a', cancelButtonColor: '#aaa',
  }).then(async () => {
    try { await dishApi.remove(dishId); showToast('删除成功'); closePopup(); loadDishes() } catch {}
  }).catch(() => {})
}

function switchTab(i: number) {
  activeTab.value = i
  if (i === 1 && orders.value.length === 0) loadOrders()
  if (i === 2 && dishes.value.length === 0) loadDishes()
}

const tabConfigs = [
  { icon: '📊', name: '概况' },
  { icon: '📋', name: '订单' },
  { icon: '🍽️', name: '菜品' },
]
</script>

<template>
  <div class="m-page">
    <!-- 顶部欢迎 -->
    <div class="page-header">
      <div class="welcome-card">
        <div class="wc-left">
          <span class="wc-emoji">🏪</span>
          <div class="wc-info">
            <div class="wc-greet">欢迎回来</div>
            <div class="wc-name">{{ userStore.userInfo?.username || '商家' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页面内 Tab 切换 -->
    <div class="page-tabs">
      <button v-for="(t, i) in tabConfigs" :key="i"
        :class="['pt-btn', { active: activeTab === i }]"
        @click="switchTab(i)">
        <span class="pt-icon">{{ t.icon }}</span>
        <span class="pt-name">{{ t.name }}</span>
      </button>
    </div>

    <!-- ======================== 概况 TAB ======================== -->
    <template v-if="activeTab === 0">
      <!-- 核心数据 -->
      <div class="section-bar"><span class="section-dot"></span>今日数据</div>
      <van-loading v-if="loadingStats" size="28" style="margin:30px 0;text-align:center" />
      <div v-else class="data-grid">
        <div class="data-card dc-dark">
          <div class="dc-num">{{ stats.today_orders || 0 }}</div>
          <div class="dc-label">今日订单</div>
        </div>
        <div class="data-card dc-light">
          <div class="dc-num dc-money">¥{{ stats.today_revenue || '0.00' }}</div>
          <div class="dc-label">今日收入</div>
        </div>
      </div>

      <!-- 待处理概览 -->
      <div class="section-bar"><span class="section-dot"></span>待处理</div>
      <div v-if="!loadingStats" class="alert-grid">
        <div v-for="a in [
          { key: 'preparing', emoji: '👨‍🍳', label: '备餐中' },
          { key: 'waiting_pickup', emoji: '📌', label: '待取餐' },
          { key: 'pending_payment', emoji: '⏳', label: '待支付' },
        ]" :key="a.key" class="alert-card"
          :class="{ 'has-items': (stats[a.key] || 0) > 0 }"
          @click="activeTab = 1; orderFilter = orderTabs.findIndex(t => t.key === a.key); loadOrders()">
          <div class="ac-top">
            <span class="ac-emoji">{{ a.emoji }}</span>
            <span class="ac-count">{{ stats[a.key] || 0 }}</span>
          </div>
          <div class="ac-label">{{ a.label }}</div>
        </div>
      </div>
    </template>

    <!-- ======================== 订单 TAB ======================== -->
    <template v-if="activeTab === 1">
      <div class="section-bar"><span class="section-dot"></span>订单管理</div>

      <div class="order-filter">
        <button v-for="(t, i) in orderTabs" :key="t.key"
          :class="['of-btn', { active: orderFilter === i }]"
          @click="orderFilter = i; loadOrders()">{{ t.name }}</button>
      </div>

      <van-loading v-if="loadingOrders" size="28" style="margin:30px 0;text-align:center" />
      <van-empty v-else-if="orders.length === 0" description="暂无订单" image-size="120" />

      <div v-else class="order-list">
        <div v-for="o in orders" :key="o.order_id" class="order-card">
          <div class="oc-top">
            <span class="oc-id">#{{ o.order_id }}</span>
            <span :class="['status-tag', `status-tag--${o.order_status}`]">{{ tx[o.order_status] }}</span>
          </div>
          <div class="oc-items">
            <div v-for="item in o.items" :key="item.order_item_id" class="oc-row">
              <span>{{ item.dish_name }}</span><span>x{{ item.quantity }}</span>
            </div>
          </div>
          <div class="oc-bottom">
            <span class="oc-time">{{ o.create_time }}</span>
            <span class="oc-total">¥{{ o.total_money }}</span>
          </div>
          <div v-if="o.order_status === 'preparing'" class="oc-action">
            <button class="oc-btn" @click="handleComplete(o.order_id)">出餐</button>
          </div>
          <div v-else-if="o.order_status === 'waiting_pickup'" class="oc-action">
            <div class="oc-pickup">
              <span class="op-label">取餐码</span>
              <span class="op-code">{{ o.pick_up_code || '—' }}</span>
            </div>
            <button class="oc-btn" @click.stop="openPickupDialog(o.order_id)">确认取餐</button>
          </div>
          <div v-else-if="o.order_status === 'pending_payment'" class="oc-action">
            <span class="oc-wait">等待顾客支付</span>
          </div>
        </div>
      </div>
    </template>

    <!-- ======================== 菜品 TAB ======================== -->
    <template v-if="activeTab === 2">
      <div class="section-bar"><span class="section-dot"></span>菜品管理</div>
      <div class="dish-toolbar">
        <button class="dt-add-btn" @click="openAddPopup">+ 新增菜品</button>
      </div>

      <van-loading v-if="loadingDishes" size="28" style="margin:30px 0;text-align:center" />
      <van-empty v-else-if="dishes.length === 0" description="暂无菜品" image-size="120" />

      <div v-else class="dish-list">
        <div v-for="dish in dishes" :key="dish.dish_id" class="dish-card" @click="openEditPopup(dish)">
          <div class="dc-left">
            <div v-if="dish.image" class="dc-img">
              <van-image :src="dish.image" fit="cover" width="72" height="72" radius="16" />
            </div>
            <div v-else class="dc-img dc-ph">☕</div>
            <div class="dc-info">
              <div class="dc-name">{{ dish.dish_name }}</div>
              <span class="dc-price"><small>¥</small><strong>{{ dish.price }}</strong></span>
            </div>
          </div>
          <div class="dc-right" @click.stop>
            <van-switch :model-value="dish.status" active-color="#1a1a1a" @change="toggleDish(dish)" size="24" />
          </div>
        </div>
      </div>
    </template>

    <!-- ====== 菜品新增/编辑弹出层 ====== -->
    <van-popup v-model:show="showDishPopup" position="bottom" round :style="{ maxHeight: '85vh' }">
      <div class="dish-popup">
        <div class="dp-header">
          <div class="dp-hleft">
            <span class="dp-emoji">✨</span>
            <span class="dp-title">{{ popupTitle }}</span>
          </div>
          <div class="dp-hright">
            <button v-if="popupMode === 'edit'" class="dp-del-btn" @click="confirmDelete(editingDishId, newDish.dish_name)">删除</button>
            <button class="dp-btn" @click="closePopup"><van-icon name="cross" size="20" color="#999" /></button>
          </div>
        </div>
        <div class="dp-body">
          <div class="dp-field">
            <div class="dp-label"><span class="dp-dot"></span>菜品名称</div>
            <div class="dp-input-wrap">
              <input v-model="newDish.dish_name" placeholder="请输入菜品名称" maxlength="50" class="dp-input" />
            </div>
          </div>
          <div class="dp-field">
            <div class="dp-label"><span class="dp-dot"></span>价格</div>
            <div class="dp-input-wrap dp-input-price">
              <span class="dp-unit">¥</span>
              <input v-model="newDish.price" placeholder="0.00" type="number" class="dp-input" />
            </div>
          </div>
          <div class="dp-field">
            <div class="dp-label"><span class="dp-dot"></span>分类</div>
            <div class="dp-input-wrap dp-select" @click="showCategoryPicker = true">
              <span class="dp-val">{{ getCategoryLabel() }}</span>
              <van-icon name="arrow" size="16" color="#ccc" />
            </div>
          </div>
          <div class="dp-field">
            <div class="dp-label"><span class="dp-dot"></span>菜品图片</div>
            <div v-if="!previewUrl" class="dp-up-trigger" @click="triggerUpload">
              <van-icon name="photograph" size="36" color="#ccc" />
              <span class="dp-up-text">点击上传图片</span>
            </div>
            <div v-else class="dp-preview">
              <img :src="previewUrl" class="dp-preview-img" />
              <button class="dp-remove" @click="removeImage">删除</button>
            </div>
          </div>
        </div>
        <div class="dp-footer">
          <button class="dp-submit" @click="saveDish">{{ submitText }}</button>
        </div>
      </div>
    </van-popup>

    <!-- 分类选择 -->
    <van-popup v-model:show="showCategoryPicker" position="bottom" round :style="{ maxHeight: '60vh' }">
      <div class="cat-popup">
        <div class="cp-header">
          <span class="cp-emoji">📂</span>
          <span class="cp-title">选择分类</span>
          <button class="cp-close" @click="showCategoryPicker = false"><van-icon name="cross" size="20" color="#999" /></button>
        </div>
        <div class="cp-list">
          <button v-for="c in categories" :key="c.value"
            :class="['cp-item', { active: newDish.category === c.value }]"
            @click="selectCategory(c.value)">
            <span>{{ c.label }}</span>
            <van-icon v-if="newDish.category === c.value" name="success" size="18" color="#fff" />
          </button>
        </div>
      </div>
    </van-popup>

    <!-- ====== 确认取餐弹窗 ====== -->
    <van-dialog v-model:show="showPickupDialog" title="确认取餐" show-cancel-button
      @confirm="handlePickupConfirm"
      :confirm-button-color="'#1a1a1a'" :cancel-button-color="'#aaa'">
      <div class="pickup-wrap">
        <p class="pickup-hint">请输入顾客出示的取餐码</p>
        <input v-model="pickupCode" placeholder="6位取餐码" maxlength="6" class="pickup-input" />
      </div>
    </van-dialog>
  </div>
</template>

<style scoped>
.m-page { min-height: 100vh; background: #f5f3f0; padding-bottom: 100px; }

/* 顶部欢迎 */
.page-header { padding: 20px 20px 4px; }
.welcome-card {
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(135deg, #fff 0%, #fcfcfc 100%);
  border-radius: 32px; padding: 20px 28px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02), 0 8px 24px rgba(0,0,0,0.06), 0 20px 48px rgba(0,0,0,0.04);
}
.wc-left { display: flex; align-items: center; gap: 16px; }
.wc-emoji { font-size: 38px; line-height: 1; flex-shrink: 0; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.10)); }
.wc-info { display: flex; flex-direction: column; gap: 4px; }
.wc-greet { font-size: 14px; color: #aaa; font-weight: 500; }
.wc-name { font-size: 26px; font-weight: 900; color: #1a1a1a; line-height: 1; }
.wc-badge { background: #1a1a1a; color: #fff; font-size: 14px; font-weight: 700; padding: 6px 20px; border-radius: 16px; white-space: nowrap; }

/* 页面 Tab */
.page-tabs {
  display: flex; gap: 10px; padding: 10px 24px 4px;
}
.pt-btn {
  flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px;
  padding: 14px; border: none; background: #fff; border-radius: 24px;
  font-size: 16px; font-weight: 700; color: #aaa; cursor: pointer;
  transition: all 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.pt-btn:active { transform: scale(0.95); }
.pt-btn.active { background: #1a1a1a; color: #fff; box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
.pt-icon { font-size: 20px; line-height: 1; }

/* section */
.section-bar { display: flex; align-items: center; gap: 10px; font-size: 18px; font-weight: 700; color: #1a1a1a; padding: 14px 24px 10px; }
.section-dot { width: 10px; height: 10px; border-radius: 50%; background: #1a1a1a; flex-shrink: 0; }

/* ========== 概况 ========== */
.data-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; padding: 0 24px 8px; }
.data-card { border-radius: 28px; padding: 22px 24px 18px; }
.dc-dark { background: #1a1a1a; }
.dc-light { background: #fff; }
.dc-dark .dc-num { color: #fff; }
.dc-dark .dc-label { color: rgba(255,255,255,0.7); }
.dc-num { font-size: 34px; font-weight: 900; color: #1a1a1a; margin-bottom: 6px; }
.dc-money { color: #ff6b6b !important; }
.dc-label { font-size: 15px; font-weight: 600; color: #888; }

.alert-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; padding: 0 24px 14px; }
.alert-card { background: #fff; border-radius: 24px; padding: 18px 14px 14px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); cursor: pointer; transition: all 0.2s; }
.alert-card:active { transform: scale(0.94); }
.alert-card.has-items { background: #1a1a1a; }
.alert-card.has-items .ac-count { color: #fff; }
.alert-card.has-items .ac-label { color: rgba(255,255,255,0.7); }
.ac-emoji { font-size: 28px; display: block; margin-bottom: 6px; }
.ac-count { font-size: 28px; font-weight: 900; color: #1a1a1a; margin-bottom: 4px; }
.ac-label { font-size: 13px; color: #888; font-weight: 600; }

/* ========== 订单 ========== */
.order-filter { display: flex; gap: 8px; padding: 0 24px 12px; overflow-x: auto; }
.of-btn { padding: 10px 20px; border-radius: 20px; font-size: 14px; font-weight: 700; background: #fff; color: #888; border: none; cursor: pointer; white-space: nowrap; transition: all 0.2s; box-shadow: 0 2px 6px rgba(0,0,0,0.04); }
.of-btn:active { transform: scale(0.94); }
.of-btn.active { background: #1a1a1a; color: #fff; box-shadow: 0 4px 14px rgba(0,0,0,0.12); }

.order-list { padding: 0 24px 20px; }
.order-card { background: #fff; border-radius: 28px; padding: 20px; margin-bottom: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.oc-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.oc-id { font-size: 15px; font-weight: 700; color: #1a1a1a; }
.oc-items { border-top: 2px solid #f5f3f0; border-bottom: 2px solid #f5f3f0; padding: 10px 0; }
.oc-row { display: flex; justify-content: space-between; font-size: 15px; color: #555; padding: 4px 0; }
.oc-bottom { display: flex; justify-content: space-between; align-items: center; padding-top: 12px; }
.oc-total { font-weight: 800; color: #ff6b6b; font-size: 18px; }
.oc-time { font-size: 13px; color: #ccc; }
.oc-action { margin-top: 14px; text-align: right; }
.oc-btn { padding: 10px 24px; border: none; border-radius: 22px; background: #1a1a1a; color: #fff; font-size: 15px; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.oc-btn:active { transform: scale(0.94); }
.oc-wait { font-size: 14px; color: #bbb; font-weight: 500; }
.oc-pickup { display: flex; align-items: center; gap: 12px; background: #f9f8f6; border-radius: 16px; padding: 12px 16px; }
.op-label { font-size: 13px; color: #888; font-weight: 600; }
.op-code { font-size: 22px; font-weight: 900; color: #1a1a1a; letter-spacing: 4px; }

/* ========== 菜品 ========== */
.dish-toolbar { padding: 0 24px 12px; }
.dt-add-btn { width: 100%; padding: 16px; border: 2px dashed #ddd; border-radius: 24px; background: transparent; font-size: 17px; font-weight: 700; color: #888; cursor: pointer; transition: all 0.2s; }
.dt-add-btn:active { border-color: #1a1a1a; color: #1a1a1a; background: #f9f8f6; }

.dish-list { padding: 0 24px 20px; }
.dish-card { display: flex; align-items: center; justify-content: space-between; background: #fff; border-radius: 24px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); cursor: pointer; transition: all 0.2s; }
.dish-card:active { transform: scale(0.98); }
.dc-left { display: flex; align-items: center; gap: 14px; flex: 1; min-width: 0; }
.dc-img { flex-shrink: 0; }
.dc-ph { width: 72px; height: 72px; background: #f0ebe6; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 28px; }
.dc-info { flex: 1; min-width: 0; }
.dc-name { font-size: 20px; font-weight: 900; color: #1a1a1a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 2px; }
.dc-price small { font-size: 14px; color: #ff6b6b; }
.dc-price strong { font-size: 24px; font-weight: 800; color: #ff6b6b; }
.dc-right { flex-shrink: 0; }

/* ===== 菜品弹出层 ===== */
.dish-popup { background: #f5f3f0; border-radius: 32px 32px 0 0; padding: 0 0 env(safe-area-inset-bottom); }
.dp-header { display: flex; align-items: center; justify-content: space-between; padding: 24px 28px 14px; }
.dp-hleft { display: flex; align-items: center; gap: 12px; }
.dp-hright { display: flex; align-items: center; gap: 8px; }
.dp-emoji { font-size: 30px; line-height: 1; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.10)); }
.dp-title { font-size: 22px; font-weight: 900; color: #1a1a1a; }
.dp-btn { width: 40px; height: 40px; border-radius: 50%; border: none; background: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.dp-btn:active { transform: scale(0.9); }
.dp-del-btn { padding: 8px 18px; border: 2px solid #ff6b6b; border-radius: 20px; background: #fff; color: #ff6b6b; font-size: 14px; font-weight: 700; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.dp-del-btn:active { transform: scale(0.94); background: #fff5f5; }
.dp-body { padding: 8px 24px 0; }
.dp-field { margin-bottom: 16px; }
.dp-label { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 700; color: #1a1a1a; margin-bottom: 8px; }
.dp-dot { width: 8px; height: 8px; border-radius: 50%; background: #1a1a1a; flex-shrink: 0; }
.dp-input-wrap { background: #fff; border-radius: 20px; padding: 0 18px; display: flex; align-items: center; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.dp-input { flex: 1; border: none; background: transparent; padding: 14px 0; font-size: 16px; outline: none; color: #1a1a1a; }
.dp-input::placeholder { color: #ccc; }
.dp-input-price .dp-unit { font-size: 18px; font-weight: 800; color: #ff6b6b; margin-right: 6px; flex-shrink: 0; }
.dp-select { cursor: pointer; }
.dp-val { flex: 1; padding: 14px 0; font-size: 16px; color: #1a1a1a; font-weight: 600; }
.dp-up-trigger { width: 100%; height: 140px; border-radius: 22px; background: #f9f8f6; border: 2px dashed #e0ddd8; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; cursor: pointer; transition: all 0.2s; }
.dp-up-trigger:active { border-color: #1a1a1a; background: #f0ebe6; }
.dp-up-text { font-size: 15px; color: #bbb; font-weight: 600; }
.dp-preview { position: relative; width: 100%; border-radius: 22px; overflow: hidden; background: #f0ebe6; aspect-ratio: 2 / 1; }
.dp-preview-img { width: 100%; height: 100%; object-fit: cover; display: block; }
.dp-remove { position: absolute; top: 10px; right: 10px; padding: 6px 16px; border: 2px solid #ff6b6b; border-radius: 18px; background: rgba(255,255,255,0.9); color: #ff6b6b; font-size: 14px; font-weight: 700; cursor: pointer; }
.dp-footer { padding: 16px 24px 24px; }
.dp-submit { width: 100%; padding: 16px; border: none; border-radius: 24px; background: #1a1a1a; color: #fff; font-size: 18px; font-weight: 800; cursor: pointer; box-shadow: 0 6px 20px rgba(0,0,0,0.15); transition: all 0.2s; }
.dp-submit:active { transform: scale(0.97); }

/* ===== 分类选择 ===== */
.cat-popup { background: #f5f3f0; border-radius: 32px 32px 0 0; padding: 0 0 env(safe-area-inset-bottom); }
.cp-header { display: flex; align-items: center; gap: 12px; padding: 24px 28px 14px; }
.cp-emoji { font-size: 26px; line-height: 1; }
.cp-title { flex: 1; font-size: 22px; font-weight: 900; color: #1a1a1a; }
.cp-close { width: 40px; height: 40px; border-radius: 50%; border: none; background: #fff; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.cp-list { padding: 8px 24px 24px; }
.cp-item { display: flex; align-items: center; justify-content: space-between; width: 100%; background: #fff; border: none; border-radius: 22px; padding: 18px 22px; margin-bottom: 10px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.cp-item.active { background: #1a1a1a; color: #fff; }
.cp-item span { font-size: 16px; font-weight: 700; }

/* ===== 确认取餐弹窗 ===== */
.pickup-wrap { padding: 20px 24px 10px; }
.pickup-hint { font-size: 15px; color: #888; margin: 0 0 14px; text-align: center; }
.pickup-input { width: 100%; border: 2px solid #e0ddd8; background: #f9f8f6; border-radius: 16px; padding: 16px; font-size: 22px; font-weight: 800; text-align: center; letter-spacing: 6px; outline: none; box-sizing: border-box; }
.pickup-input:focus { border-color: #1a1a1a; background: #fff; }
</style>
