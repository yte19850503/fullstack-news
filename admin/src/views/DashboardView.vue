<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stat-cards">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_users }}</div>
            <div class="stat-label">用户总数</div>
            <div class="stat-extra">今日新增 {{ stats.today_new_users }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_articles }}</div>
            <div class="stat-label">文章总数</div>
            <div class="stat-extra">今日新增 {{ stats.today_new_articles }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_comments }}</div>
            <div class="stat-label">评论总数</div>
            <div class="stat-extra">今日新增 {{ stats.today_new_comments }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ stats.total_categories + stats.total_tags }}</div>
            <div class="stat-label">分类 / 标签</div>
            <div class="stat-extra">{{ stats.total_categories }} 分类 · {{ stats.total_tags }} 标签</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>文章状态分布</template>
          <div ref="pieRef" class="chart"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>今日新增</template>
          <div ref="barRef" class="chart"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { getStats } from '@/api/stats'
import type { Stats } from '@/types'

const stats = reactive<Stats>({
  total_users: 0,
  total_articles: 0,
  total_comments: 0,
  total_categories: 0,
  total_tags: 0,
  published_articles: 0,
  draft_articles: 0,
  active_users: 0,
  today_new_users: 0,
  today_new_articles: 0,
  today_new_comments: 0,
})

const pieRef = ref<HTMLDivElement>()
const barRef = ref<HTMLDivElement>()
let pieChart: echarts.ECharts | null = null
let barChart: echarts.ECharts | null = null

function renderCharts() {
  if (pieRef.value) {
    pieChart = echarts.init(pieRef.value)
    const archived = Math.max(0, stats.total_articles - stats.published_articles - stats.draft_articles)
    pieChart.setOption({
      tooltip: { trigger: 'item' },
      legend: { bottom: 0 },
      series: [
        {
          type: 'pie',
          radius: ['40%', '70%'],
          data: [
            { value: stats.published_articles, name: '已发布', itemStyle: { color: '#67c23a' } },
            { value: stats.draft_articles, name: '草稿', itemStyle: { color: '#e6a23c' } },
            { value: archived, name: '已归档', itemStyle: { color: '#909399' } },
          ],
        },
      ],
    })
  }

  if (barRef.value) {
    barChart = echarts.init(barRef.value)
    barChart.setOption({
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: ['用户', '文章', '评论'] },
      yAxis: { type: 'value' },
      series: [
        {
          type: 'bar',
          data: [stats.today_new_users, stats.today_new_articles, stats.today_new_comments],
          itemStyle: { color: '#409eff', borderRadius: [4, 4, 0, 0] },
        },
      ],
    })
  }
}

function handleResize() {
  pieChart?.resize()
  barChart?.resize()
}

onMounted(async () => {
  const data = await getStats()
  Object.assign(stats, data)
  renderCharts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  pieChart?.dispose()
  barChart?.dispose()
})
</script>

<style scoped>
.stat-cards .stat-item {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.stat-extra {
  font-size: 12px;
  color: #b1b3b8;
  margin-top: 4px;
}

.chart {
  height: 300px;
}
</style>
