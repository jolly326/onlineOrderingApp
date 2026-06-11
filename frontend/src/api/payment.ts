/** 支付模块 API */
import request from './index'

export const paymentApi = {
  /** 发起支付 */
  pay(orderId: string, payType: string = 'wechat') {
    return request.post('/payments/pay', { order_id: orderId, pay_type: payType })
  },
  /** 查询支付状态 */
  getStatus(payId: string) {
    return request.get(`/payments/${payId}/status`)
  },
}
