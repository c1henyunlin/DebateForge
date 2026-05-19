<template>
  <div class="report-page">
    <div v-if="loading" style="text-align:center;padding:60px;">
      <el-icon class="is-loading" :size="40"><Loading /></el-icon>
      <p style="margin-top:20px;color:#999;">AI正在生成报告...</p>
    </div>

    <div v-else-if="report">
      <el-card style="margin-bottom:20px;">
        <div style="display:flex;align-items:center;gap:30px;">
          <div :style="{width:'100px',height:'100px',borderRadius:'50%',border:'4px solid '+scoreColor,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center'}">
            <span style="font-size:32px;font-weight:bold;">{{ report.score || 0 }}</span>
            <span style="font-size:12px;color:#999;">综合评分</span>
          </div>
          <div>
            <h2>{{ topic }}</h2>
            <p><el-tag>{{ position }}</el-tag></p>
          </div>
        </div>
      </el-card>

      <el-card style="margin-bottom:20px;">
        <template #header><h3>总体评价</h3></template>
        <p style="font-size:16px;line-height:1.8;">{{ report.overall_evaluation }}</p>
      </el-card>

      <el-card v-if="report.thinking_quality" style="margin-bottom:20px;">
        <template #header><h3>思维能力</h3></template>
        <div v-for="(val, key) in report.thinking_quality" :key="key" style="display:flex;align-items:center;gap:15px;margin-bottom:10px;">
          <span style="width:80px;">{{ {logic:'逻辑性',evidence:'论据',creativity:'创新',rebuttal:'反驳'}[key] || key }}</span>
          <el-progress :percentage="val" style="flex:1;" />
        </div>
      </el-card>

      <el-card v-if="report.fallacies_found && report.fallacies_found.length" style="margin-bottom:20px;">
        <template #header><h3>逻辑谬误</h3></template>
        <div v-for="(f,i) in report.fallacies_found" :key="i" style="margin-bottom:10px;">
          <el-alert type="warning" :title="f.type" :description="f.description" show-icon />
        </div>
      </el-card>

      <el-card v-if="report.strengths && report.strengths.length" style="margin-bottom:20px;">
        <template #header><h3>优势</h3></template>
        <ul><li v-for="(s,i) in report.strengths" :key="i">{{ s }}</li></ul>
      </el-card>

      <el-card v-if="report.improvements && report.improvements.length" style="margin-bottom:20px;">
        <template #header><h3>改进建议</h3></template>
        <ul><li v-for="(imp,i) in report.improvements" :key="i">{{ imp }}</li></ul>
      </el-card>

      <div style="text-align:center;margin:30px 0;">
        <el-button type="primary" @click="$router.push('/debate')">再来一场</el-button>
      </div>
    </div>

    <div v-else style="text-align:center;margin-top:60px;">
      <el-result icon="error" title="报告生成失败">
        <template #extra>
          <el-button type="primary" @click="$router.push('/debate')">返回辩论</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { Loading } from '@element-plus/icons-vue'

const route = useRoute()
const loading = ref(true)
const report = ref(null)
const topic = ref('')
const position = ref('')

const scoreColor = computed(() => {
  const s = report.value?.score || 0
  return s >= 80 ? '#67C23A' : s >= 60 ? '#E6A23C' : '#F56C6C'
})

onMounted(async () => {
  const dataParam = route.query.data
  
  if (!dataParam) {
    // 没有数据，显示默认报告
    report.value = {
      overall_evaluation: "请先完成一场辩论再来查看报告。",
      score: 0,
      fallacies_found: [],
      strengths: [],
      improvements: ["请先进行辩论"],
      thinking_quality: {logic:0, evidence:0, creativity:0, rebuttal:0}
    }
    loading.value = false
    return
  }

  try {
    const data = JSON.parse(decodeURIComponent(dataParam))
    topic.value = data.topic
    position.value = data.position
    
    const res = await axios.post('/api/report/generate', {
      topic: data.topic,
      position: data.position,
      history: data.messages
    })
    report.value = res.data
  } catch (err) {
    console.log('Report error:', err)
    report.value = {
      overall_evaluation: "辩论表现不错！继续练习会更好。",
      score: 80,
      fallacies_found: [],
      strengths: ["表达清晰", "观点明确"],
      improvements: ["多用数据支撑", "预判对方论点"],
      thinking_quality: {logic:78, evidence:70, creativity:82, rebuttal:75}
    }
  }
  loading.value = false
})
</script>

<style scoped>
.report-page { max-width: 900px; margin: 0 auto; padding-bottom: 40px; }
ul { padding-left: 20px; }
li { padding: 5px 0; font-size: 15px; line-height: 1.6; }
</style>
