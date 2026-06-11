/** 订单模块 API */
import request from './index'

export const orderApi = {
  /** 提交订单 */
  create() {
    return request.post('/orders/create', {})
  },
  /** 获取用户订单列表 */
  getList(status?: string) {
    const params = status ? { status } : {}
    return request.get('/orders/', { params })
  },
  /** 获取订单详情 */
  getDetail(orderId: string) {
    return request.get(`/orders/${orderId}`)
  },
  /** 获取用户订单数量统计 */
  getOrderCount() {
    return request.get('/orders/count')
  },
  /** 商家获取所有订单 */
  getMerchantList(status?: string) {
    const params = status ? { status } : {}
    return request.get('/orders/merchant', { params })
  },
  /** 获取商家运营统计 */
  getMerchantStats() {
    return request.get('/orders/merchant/stats')
  },
  /** 商家更新订单状态 */
  updateStatus(orderId: string, status: string) {
    return request.put(`/orders/${orderId}/status`, { order_status: status })
  },
  /** 商家确认取餐（输入取餐码） */
  merchantConfirmPickup(orderId: string, pickUpCode: string) {
    return request.put(`/orders/merchant/confirm-pickup/${orderId}`, { pick_up_code: pickUpCode })
  },
}
