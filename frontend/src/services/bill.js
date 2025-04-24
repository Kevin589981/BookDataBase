import api from '@/utils/api'

class BillService {
  // 获取所有账单
  async getAllBills(params) {
    try {
      // 过滤掉空字符串参数
      const filteredParams = Object.entries(params).reduce((acc, [key, value]) => {
        // 如果值不为空且不为空字符串，则添加到参数中
        if (value !== null && value !== '' && value !== undefined) {
          acc[key] = value
        }
        return acc
      }, {})
      
      const response = await api.get('/bills/', { 
        params: filteredParams
      })
      
      return {
        items: response.data.items || [], 
        total: response.data.total || 0,
        page: response.data.page || 1,
        page_size: response.data.page_size || 10
      }
    } catch (error) {
      console.error('获取账单列表失败:', error)
      throw error
    }
  }

  // 获取账单流水趋势数据
  async getBillTrends(params = {}) {
    try {
      // 确保按时间排序
      const trendParams = {
        ...params,
        sort_by: 'transaction_time',
        sort_order: 'asc',
        page_size: 100 // 获取更多数据以便绘制图表
      }
      
      // 过滤掉空参数
      const filteredParams = Object.entries(trendParams).reduce((acc, [key, value]) => {
        if (value !== null && value !== '' && value !== undefined) {
          acc[key] = value
        }
        return acc
      }, {})
      
      const response = await api.get('/bills/', { 
        params: filteredParams
      })
      
      // 处理数据以适合图表展示
      const items = response.data.items || []
      const dates = []
      const amounts = []
      
      // 按日期分组并计算每日总额
      const dailyTotals = items.reduce((acc, bill) => {
        // 提取日期部分
        const date = bill.transaction_time.split('T')[0]
        if (!acc[date]) {
          acc[date] = 0
        }
        // 根据账单类型处理金额（进货为负，零售为正）
        const amount = bill.bill_type === '进货' ? -parseFloat(bill.amount) : parseFloat(bill.amount)
        acc[date] += amount
        return acc
      }, {})
      
      // 将分组数据转换为数组
      Object.entries(dailyTotals)
        .sort(([dateA], [dateB]) => new Date(dateA) - new Date(dateB))
        .forEach(([date, amount]) => {
          dates.push(date)
          amounts.push(amount)
        })
      
      return {
        dates,
        amounts
      }
    } catch (error) {
      console.error('获取账单流水趋势数据失败:', error)
      throw error
    }
  }
}

export default new BillService()