/** 菜品模块 API */
import request from './index'

export const dishApi = {
  /** 获取上架菜品列表（按分类筛选） */
  getList(category?: string) {
    const params = category ? { category } : {}
    return request.get('/dishes/', { params })
  },
  /** 获取所有菜品（含下架，商家用） */
  getAll() {
    return request.get('/dishes/all')
  },
  /** 获取菜品详情 */
  getDetail(dishId: string) {
    return request.get(`/dishes/${dishId}`)
  },
  /** 新增菜品（商家，multipart上传） */
  create(data: FormData) {
    return request.post('/dishes/create', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  /** 修改菜品（商家，multipart上传） */
  update(dishId: string, data: FormData) {
    return request.put(`/dishes/${dishId}/update`, data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  /** 上下架菜品（商家） */
  updateStatus(dishId: string, status: boolean) {
    return request.put(`/dishes/${dishId}/status`, { status })
  },
  /** 删除菜品（商家） */
  remove(dishId: string) {
    return request.delete(`/dishes/${dishId}/delete`)
  },
}
