/** 购物车模块 API */
import request from './index'

export const cartApi = {
  /** 获取购物车 */
  getCart() {
    return request.get('/cart/')
  },
  /** 添加菜品 */
  addItem(dishId: string, quantity: number = 1) {
    return request.post('/cart/items', { dish_id: dishId, quantity })
  },
  /** 修改数量 */
  updateItem(itemId: string, quantity: number) {
    return request.put(`/cart/items/${itemId}`, { quantity })
  },
  /** 删除菜品项 */
  deleteItem(itemId: string) {
    return request.delete(`/cart/items/${itemId}/delete`)
  },
  /** 清空购物车 */
  clearCart() {
    return request.delete('/cart/clear')
  },
}
