/**
 * 购物车状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { cartApi } from '@/api/cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref<any[]>([])
  const total = ref(0)
  const itemCount = ref(0)

  /** 获取购物车 */
  async function fetchCart() {
    try {
      const res: any = await cartApi.getCart()
      items.value = res.data.items || []
      total.value = res.data.total || 0
      itemCount.value = items.value.reduce((sum: number, item: any) => sum + item.quantity, 0)
    } catch {
      // ignore
    }
  }

  /** 添加菜品 */
  async function addDish(dishId: string, quantity = 1) {
    await cartApi.addItem(dishId, quantity)
    await fetchCart()
  }

  /** 更新数量 */
  async function updateItem(itemId: string, quantity: number) {
    await cartApi.updateItem(itemId, quantity)
    await fetchCart()
  }

  /** 删除菜品 */
  async function removeItem(itemId: string) {
    await cartApi.deleteItem(itemId)
    await fetchCart()
  }

  /** 清空购物车 */
  async function clearCart() {
    await cartApi.clearCart()
    items.value = []
    total.value = 0
    itemCount.value = 0
  }

  return { items, total, itemCount, fetchCart, addDish, updateItem, removeItem, clearCart }
})
