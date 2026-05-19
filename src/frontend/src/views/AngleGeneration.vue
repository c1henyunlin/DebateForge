<template>
  <div class="angle-page">
    <el-card class="header-card">
      <h1>💡 多角度论证生成</h1>
      <p>输入议题生成论证角度，点击角度加入辩论准备区，可多选</p>
    </el-card>
    
    <!-- 辩论准备区 -->
    <div v-if="selectedAngles.length > 0" class="debate-prep">
      <el-card>
        <template #header>
          <span>🗣️ 辩论准备区（{{ selectedAngles.length }}个角度）</span>
        </template>
        <el-tag 
          v-for="(item, i) in selectedAngles" 
          :key="i" 
          :type="item.position === '正方' ? 'success' : 'danger'"
          closable
          @close="removeAngle(i)"
          size="large"
          style="margin: 4px;"
        >
          {{ item.position }}：{{ item.angle }}
        </el-tag>
        <div v-if="selectedAngles.length === 0" style="color:#999;">点击下方角度卡片来添加</div>
        <div style="margin-top: 12px;">
          <el-button type="primary" @click="goToDebateWithAngles" size="large">
            <el-icon><ChatDotRound /></el-icon>
            用这{{ selectedAngles.length }}个角度去辩论
          </el-button>
          <el-button @click="selectedAngles = []">清空</el-button>
        </div>
      </el-card>
    </div>

    <el-card class="input-card">
      <el-input v-model="topic" type="textarea" :rows="3" placeholder="请输入议题" />
      <div style="margin-top: 15px; text-align: center;">
        <el-button type="primary" @click="generate" :loading="loading" size="large">生成论证角度</el-button>
        <el-button @click="topic='大学是否应该取消期末考试'">示例</el-button>
        <el-button type="success" @click="goToDebateWithAngles" :disabled="!topic.trim()" size="large">
          <el-icon><ChatDotRound /></el-icon> 去辩论
        </el-button>
      </div>
    </el-card>

    <div v-if="error"><el-alert :title="error" type="error" show-icon @close="error=''" /></div>

    <div v-if="result" style="margin-top: 20px;">
      <el-row :gutter="24">
        <el-col :span="12">
          <el-card>
            <template #header>
              <el-tag type="success" size="large">正方观点（支持）</el-tag>
            </template>
            <div 
              v-for="(a, i) in result.pro_position" :key="i" 
              class="angle-card" :class="{ selected: isSelected(a.angle, '正方') }"
              @click="toggleAngle(a.angle, '正方')"
            >
              <div class="angle-top">
                <h3>{{ i+1 }}. {{ a.angle }}</h3>
                <el-icon v-if="isSelected(a.angle, '正方')" color="#67C23A" :size="20"><CircleCheckFilled /></el-icon>
              </div>
              <el-tag size="small">{{ a.type }}</el-tag>
              <p>{{ a.argument }}</p>
            </div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <el-tag type="danger" size="large">反方观点（反对）</el-tag>
            </template>
            <div 
              v-for="(a, i) in result.con_position" :key="i" 
              class="angle-card con" :class="{ selected: isSelected(a.angle, '反方') }"
              @click="toggleAngle(a.angle, '反方')"
            >
              <div class="angle-top">
                <h3>{{ i+1 }}. {{ a.angle }}</h3>
                <el-icon v-if="isSelected(a.angle, '反方')" color="#F56C6C" :size="20"><CircleCheckFilled /></el-icon>
              </div>
              <el-tag size="small">{{ a.type }}</el-tag>
              <p>{{ a.argument }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ChatDotRound, CircleCheckFilled } from '@element-plus/icons-vue'

const router = useRouter()
const topic = ref('')
const loading = ref(false)
const result = ref(null)
const error = ref('')
const selectedAngles = ref([])

const mockData = {
  pro_position: [
    {"angle": "减轻学生压力", "argument": "期末考试给学生带来巨大心理压力，取消考试可以让学生更专注于真正的学习。", "type": "情感"},
    {"angle": "多元评估更科学", "argument": "单一考试无法全面反映学生能力，多维度评估更公平有效。", "type": "逻辑"},
    {"angle": "国际趋势支持", "argument": "哈佛、MIT等顶尖大学已逐步减少传统考试权重，学生满意度提升25%。", "type": "数据"}
  ],
  con_position: [
    {"angle": "学习效果检验", "argument": "考试是检验学习成果的有效手段，没有考试学生可能缺乏学习动力。", "type": "逻辑"},
    {"angle": "公平性保证", "argument": "标准化考试提供了相对公平的评估标准，避免主观评价的不公。", "type": "逻辑"},
    {"angle": "就业竞争力", "argument": "78%的企业HR认为考试成绩是衡量应届生学习能力的重要参考。", "type": "数据"}
  ]
}

const generate = async () => {
  if (!topic.value.trim()) { error.value = '请输入议题'; return }
  loading.value = true; error.value = ''; result.value = null
  try {
    const response = await axios.post('/api/angle/generate', { topic: topic.value })
    result.value = response.data
  } catch (err) {
    result.value = { topic: topic.value, ...mockData }
  }
  loading.value = false
}

const isSelected = (angle, position) => {
  return selectedAngles.value.some(a => a.angle === angle && a.position === position)
}

const toggleAngle = (angle, position) => {
  const idx = selectedAngles.value.findIndex(a => a.angle === angle && a.position === position)
  if (idx >= 0) {
    selectedAngles.value.splice(idx, 1)
  } else {
    selectedAngles.value.push({ angle, position })
  }
}

const removeAngle = (index) => {
  selectedAngles.value.splice(index, 1)
}

const goToDebateWithAngles = () => {
  if (!topic.value.trim()) return
  localStorage.setItem('debate_topic', topic.value)
  localStorage.setItem('debate_angles', JSON.stringify(selectedAngles.value))
  router.push('/debate')
}
</script>

<style scoped>
.angle-page { max-width: 1200px; margin: 0 auto; }
.header-card { margin-bottom: 20px; }
.input-card { margin-bottom: 20px; }
.debate-prep { margin-bottom: 20px; }
.angle-card { 
  padding: 12px; margin-bottom: 12px; background: #f9f9f9; 
  border-radius: 8px; border: 2px solid transparent;
  cursor: pointer; transition: all 0.2s;
}
.angle-card:hover { background: #f0f9eb; border-color: #67C23A; }
.angle-card.con:hover { background: #fef0f0; border-color: #F56C6C; }
.angle-card.selected { background: #e8f4e8; border-color: #67C23A; }
.angle-card.con.selected { background: #fde8e8; border-color: #F56C6C; }
.angle-top { display: flex; justify-content: space-between; align-items: center; }
.angle-card h3 { margin: 0; font-size: 15px; }
.angle-card p { line-height: 1.5; color: #555; margin: 8px 0 0 0; }
</style>
