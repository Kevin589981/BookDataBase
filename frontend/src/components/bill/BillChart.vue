<script setup>
import { ref, onMounted, watch, defineProps } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const chartContainer = ref(null)
let chart = null

// 初始化图表
const initChart = () => {
  if (chartContainer.value) {
    chart = echarts.init(chartContainer.value)
    updateChart()
    
    // 响应窗口大小变化
    window.addEventListener('resize', () => {
      chart && chart.resize()
    })
  }
}

// 更新图表数据
const updateChart = () => {
  if (!chart) return
  
  const option = {
    title: {
      text: '账单流水趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params) {
        const data = params[0]
        return `${data.name}<br/>${data.seriesName}: ¥${data.value.toFixed(2)}`
      }
    },
    xAxis: {
      type: 'category',
      data: props.chartData.dates || [],
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '金额 (¥)',
      axisLabel: {
        formatter: value => `¥${value}`
      }
    },
    series: [
      {
        name: '账单金额',
        type: 'line',
        data: props.chartData.amounts || [],
        smooth: true,
        itemStyle: {
          color: '#2196f3'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(33, 150, 243, 0.5)' },
              { offset: 1, color: 'rgba(33, 150, 243, 0.1)' }
            ]
          }
        }
      }
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    }
  }
  
  // 设置加载状态
  if (props.loading) {
    chart.showLoading({
      text: '加载中...',
      maskColor: 'rgba(255, 255, 255, 0.8)',
      color: '#2196f3'
    })
  } else {
    chart.hideLoading()
    chart.setOption(option)
  }
}

// 监听数据变化
watch(() => props.chartData, () => {
  updateChart()
}, { deep: true })

// 监听加载状态
watch(() => props.loading, () => {
  if (props.loading) {
    chart && chart.showLoading({
      text: '加载中...',
      maskColor: 'rgba(255, 255, 255, 0.8)',
      color: '#2196f3'
    })
  } else {
    chart && chart.hideLoading()
  }
})

onMounted(() => {
  initChart()
})
</script>

<template>
  <div class="chart-container">
    <div ref="chartContainer" class="chart"></div>
    <div v-if="!chartData.dates || chartData.dates.length === 0 && !loading" class="no-data">
      <p>暂无账单流水数据</p>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
  margin-bottom: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
}

.chart {
  width: 100%;
  height: 100%;
}

.no-data {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  color: #666;
}
</style>