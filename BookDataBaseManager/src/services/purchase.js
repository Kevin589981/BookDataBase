import api from '@/utils/api'

const API_URL = '/purchase/'

class PurchaseService {
  // 获取所有进货订单
  async getAllPurchaseOrders(params) {
    try {
      // 过滤掉空字符串参数
      const filteredParams = Object.entries(params).reduce((acc, [key, value]) => {
        // 如果值不为空且不为空字符串，则添加到参数中
        if (value !== null && value !== '' && value !== undefined) {
          acc[key] = value
        }
        return acc
      }, {})
      
      const response = await api.get(`${API_URL}orders`, { 
        params: filteredParams
      })
      
      return {
        items: response.data.items || [], // 确保即使没有数据也返回空数组
        total: response.data.total || 0,
        page: response.data.page || 1,
        page_size: response.data.page_size || 10
      }
    } catch (error) {
      console.error('获取进货订单列表失败:', error)
      throw error
    }
  }

  // 创建新进货订单
  async createPurchaseOrder(purchaseData) {
    try {
      const response = await api.post(`${API_URL}create_order/`, purchaseData)
      return response.data
    } catch (error) {
      // 处理特定的错误情况
      if (error.response && error.response.status === 400) {
        // 如果是400错误，检查是否是因为ISBN不存在
        if (error.response.data.detail && error.response.data.detail.includes('ISBN不存在')) {
          throw new Error('ISBN不存在，请提供完整的书籍信息')
        }
      }
      console.error('创建进货订单失败:', error)
      throw error
    }
  }

  // 检查ISBN是否存在
  async checkIsbnExists(isbn) {
    try {
      await api.get(`/books/${isbn}`)
      return true // ISBN存在
    } catch (error) {
      if (error.response && error.response.status === 404) {
        return false // ISBN不存在
      }
      throw error // 其他错误
    }
  }

  // 支付进货订单
  async payPurchaseOrder(orderId) {
    try {
      const response = await api.put(`${API_URL}pay/${orderId}`)
      return response.data
    } catch (error) {
      console.error('支付进货订单失败:', error)
      throw error
    }
  }

  // 退货进货订单
  async returnPurchaseOrder(orderId) {
    try {
      const response = await api.put(`${API_URL}return/${orderId}`)
      return response.data
    } catch (error) {
      console.error('退货进货订单失败:', error)
      throw error
    }
  }

  // 确认到货
  async arrivePurchaseOrder(orderId, retailPrice = null) {
    try {
      const params = retailPrice ? { retail_price: retailPrice } : {}
      const response = await api.put(`${API_URL}arrive/${orderId}`, null, {
        params: params
      })
      return response.data
    } catch (error) {
      console.error('确认到货失败:', error)
      throw error
    }
  }
}

export default new PurchaseService()