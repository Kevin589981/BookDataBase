import api from '@/utils/api'

const saleService = {
  // 创建销售订单
  async createSaleOrder(items, paymentMethod) {
    // 直接发送items数组作为请求体，payment_method作为查询参数
    const response = await api.post(`/sale/?payment_method=${encodeURIComponent(paymentMethod || '')}`, items)
    return response.data
  },
  
  // 获取所有销售订单
  async getAllSaleOrders(params = {}) {
    try {
      // 过滤掉空字符串参数
      const filteredParams = Object.entries(params).reduce((acc, [key, value]) => {
        // 如果值不为空且不为空字符串，则添加到参数中
        if (value !== null && value !== '' && value !== undefined) {
          acc[key] = value
        }
        return acc
      }, {})
      
      const response = await api.get('/sale/', { params: filteredParams })
      
      return {
        items: response.data.data || [], // 确保即使没有数据也返回空数组
        total: response.data.total || 0,
        page: response.data.page || 1,
        page_size: response.data.page_size || 10
      }
    } catch (error) {
      console.error('获取销售订单失败:', error)
      throw error
    }
  },
  
  // 获取销售订单详情
  async getSaleOrderDetail(orderId) {
    const response = await api.get(`/sale/${orderId}`)
    return response.data
  }
}

export default saleService