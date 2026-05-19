<template>
  <div class="history-page">
    <h1>历史记录</h1>

    <el-card style="margin-bottom:20px;">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="辩论记录" name="debates">
          <div v-if="debates.length === 0" style="text-align:center;padding:40px;color:#999;">
            暂无辩论记录，去<a href="/debate" @click.prevent="$router.push('/debate')" style="color:#409EFF;">辩论对战</a>吧！
          </div>
          
          <el-table v-else :data="debates" style="width:100%">
            <el-table-column prop="topic" label="辩题" min-width="200" />
            <el-table-column prop="position" label="立场" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.position==='正方'?'success':'danger'" size="small">{{ scope.row.position }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="rounds" label="回合" width="70" />
            <el-table-column prop="time" label="时间" width="160" />
            <el-table-column label="操作" width="180">
              <template #default="scope">
                <el-button size="small" @click="viewDetail(scope.row)">查看</el-button>
                <el-button size="small" type="danger" @click="deleteDebate(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="角度生成" name="angles">
          <div v-if="angles.length === 0" style="text-align:center;padding:40px;color:#999;">
            暂无角度生成记录
          </div>
          <el-table v-else :data="angles" style="width:100%">
            <el-table-column prop="topic" label="议题" />
            <el-table-column prop="time" label="时间" width="180" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="dialogVisible" title="辩论详情" width="700px">
      <div v-if="detailDebate">
        <p><strong>辩题：</strong>{{ detailDebate.topic }}</p>
        <p><strong>立场：</strong><el-tag :type="detailDebate.position==='正方'?'success':'danger'" size="small">{{ detailDebate.position }}</el-tag></p>
        <p><strong>回合数：</strong>{{ detailDebate.rounds }}</p>
        <p><strong>时间：</strong>{{ detailDebate.time }}</p>
        
        <el-divider>辩论记录</el-divider>
        <div class="detail-chat">
          <div v-for="(msg,i) in detailDebate.messages" :key="i" class="detail-msg">
            <div :class="msg.role==='user'?'user':'ai'">
              <strong>{{ msg.role==='user'?'你':'AI辩手' }}：</strong>
              {{ msg.content }}
            </div>
          </div>
        </div>

        <div v-if="detailDebate.report" style="margin-top:15px;">
          <el-divider>分析报告</el-divider>
          <p><strong>评分：</strong>{{ detailDebate.report.score || 'N/A' }}</p>
          <p><strong>评价：</strong>{{ detailDebate.report.overall_evaluation }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const activeTab = ref('debates')
const debates = ref([])
const angles = ref([])
const dialogVisible = ref(false)
const detailDebate = ref(null)

onMounted(async () => {
  try {
    const dRes = await axios.get('/api/history/debates')
    debates.value = dRes.data
    const aRes = await axios.get('/api/history/angles')
    angles.value = aRes.data
  } catch (err) {
    // 后端不可用时从localStorage加载
    loadFromLocal()
  }
})

const loadFromLocal = () => {
  const saved = localStorage.getItem('debate_history_all')
  if (saved) {
    try { debates.value = JSON.parse(saved) } catch {}
  }
}

const viewDetail = (item) => {
  detailDebate.value = item
  dialogVisible.value = true
}

const deleteDebate = async (id) => {
  try {
    await axios.delete('/api/history/debates/' + id)
  } catch {}
  debates.value = debates.value.filter(d => d.id !== id)
}
</script>

<style scoped>
.history-page { max-width: 1000px; margin: 0 auto; }
.detail-chat { max-height: 300px; overflow-y: auto; padding: 10px; background: #f5f7fa; border-radius: 8px; }
.detail-msg { margin-bottom: 10px; }
.detail-msg .user { color: #409EFF; }
.detail-msg .ai { color: #E6A23C; }
</style>
