<template>
  <div class="debate-page">
    <el-card class="header-card">
      <h1>AI辩论对战</h1>
      <p>选择立场和风格，与AI进行实时辩论</p>
    </el-card>

    <el-card v-if="!started" class="setup-card">
      <el-input v-model="topic" placeholder="请输入辩论议题" size="large" style="margin-bottom:20px;" />
      
      <div v-if="prefillAngles.length > 0" style="margin-bottom:15px;padding:12px;background:#f0f9eb;border-radius:8px;">
        <div style="font-size:13px;color:#999;">带入角度（{{ prefillAngles.length }}个）：</div>
        <el-tag v-for="(a,i) in prefillAngles" :key="i" :type="a.position==='正方'?'success':'danger'" size="small" style="margin:2px;">{{ a.position }}：{{ a.angle }}</el-tag>
        <el-button size="small" @click="prefillAngles=[]" style="margin-left:10px;">清空</el-button>
      </div>

      <div style="margin-bottom:20px;">
        <span>立场：</span>
        <el-radio-group v-model="position" size="large">
          <el-radio-button value="正方">正方</el-radio-button>
          <el-radio-button value="反方">反方</el-radio-button>
        </el-radio-group>
      </div>
      <div style="margin-bottom:20px;">
        <span>风格：</span>
        <el-radio-group v-model="style" size="large">
          <el-radio-button value="formal">正式辩论</el-radio-button>
          <el-radio-button value="casual">轻松对话</el-radio-button>
        </el-radio-group>
      </div>
      <el-button type="primary" @click="startDebate" :loading="loading" size="large">开始辩论</el-button>
    </el-card>

    <div v-else>
      <el-card class="debate-header">
        <div style="display:flex;justify-content:space-between;">
          <h3>{{ topic }}</h3>
          <el-radio-group v-model="style" size="small">
            <el-radio-button value="formal">正式</el-radio-button>
            <el-radio-button value="casual">轻松</el-radio-button>
          </el-radio-group>
        </div>
        <div style="display:flex;gap:10px;margin-top:10px;">
          <el-tag type="success">你：{{ position }}</el-tag>
          <el-tag type="danger">AI：{{ aiPosition }}</el-tag>
          <el-tag>回合：{{ round }}</el-tag>
        </div>
      </el-card>

      <el-card class="chat-area">
        <div class="messages" ref="msgBox">
          <div v-for="(msg,i) in messages" :key="i" class="msg-row">
            <div :class="['msg-bubble', msg.role==='user'?'user-msg':'ai-msg']">
              <div class="msg-label">{{ msg.role==='user'?'你':(msg.role==='helper'?'AI助攻':'AI辩手') }}</div>
              <div class="msg-text">{{ msg.content }}</div>
            </div>
          </div>
          <div v-if="thinking" style="text-align:center;color:#999;">AI思考中...</div>
          <div v-if="helpThinking" style="text-align:center;color:#999;">生成思路中...</div>
        </div>
        <div style="margin-top:15px;">
          <el-input v-model="input" type="textarea" :rows="3" placeholder="输入论点... (Ctrl+Enter发送)" @keydown.enter.ctrl="sendMessage" :disabled="thinking" />
          <div style="display:flex;justify-content:space-between;margin-top:10px;">
            <div>
              <el-button type="primary" @click="sendMessage" :disabled="!input.trim()||thinking" size="large">发送</el-button>
              <el-button type="success" @click="getHelp" :disabled="thinking||helpThinking" size="large">AI帮我想</el-button>
            </div>
            <el-button type="warning" @click="endDebate" :disabled="round<1" size="large">结束辩论</el-button>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onActivated, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const topic = ref('')
const position = ref('正方')
const style = ref('formal')
const prefillAngles = ref([])
const started = ref(false)
const loading = ref(false)
const thinking = ref(false)
const helpThinking = ref(false)
const sessionId = ref(null)
const aiPosition = ref('')
const messages = ref([])
const round = ref(0)
const input = ref('')
const msgBox = ref(null)

const loadAngles = () => {
  const t = localStorage.getItem('debate_topic')
  if (t) { topic.value = t; localStorage.removeItem('debate_topic') }
  const a = localStorage.getItem('debate_angles')
  if (a) { 
    prefillAngles.value = JSON.parse(a)
    localStorage.removeItem('debate_angles')
    const proCount = prefillAngles.value.filter(function(x) { return x.position === '正方' }).length
    const conCount = prefillAngles.value.filter(function(x) { return x.position === '反方' }).length
    position.value = proCount >= conCount ? '正方' : '反方'
  }
}

onMounted(loadAngles)
onActivated(loadAngles)

const startDebate = async () => {
  if (!topic.value.trim()) return
  loading.value = true
  const angleText = prefillAngles.value.map(function(a) { return a.position + '：' + a.angle }).join('；')
  
  try {
    const res = await axios.post('/api/debate/start', { topic: topic.value, position: position.value, angle: angleText, style: style.value })
    sessionId.value = res.data.session_id
    aiPosition.value = res.data.ai_position
    if (angleText) {
      messages.value = [{ role: 'user', content: '我的角度：' + angleText }, { role: 'ai', content: res.data.opening_message }]
    } else {
      messages.value = [{ role: 'ai', content: res.data.opening_message }]
    }
  } catch (err) {
    aiPosition.value = position.value === '正方' ? '反方' : '正方'
    sessionId.value = 99999
    messages.value = [{ role: 'ai', content: '作为' + aiPosition.value + '，我认为此议题值得深入探讨。' }]
  }
  prefillAngles.value = []
  round.value = 1
  started.value = true
  loading.value = false
  scrollToBottom()
}

const sendMessage = async () => {
  if (!input.value.trim() || thinking.value) return
  const msg = input.value.trim()
  messages.value.push({ role: 'user', content: msg })
  input.value = ''
  thinking.value = true
  scrollToBottom()
  try {
    const res = await axios.post('/api/debate/message', { session_id: sessionId.value, message: msg, style: style.value })
    messages.value.push({ role: 'ai', content: res.data.ai_response })
    round.value = res.data.round_number
  } catch (err) {
    setTimeout(function() {
      messages.value.push({ role: 'ai', content: '你的观点有道理，但需要从更多角度看。' })
      round.value++
    }, 800)
  }
  thinking.value = false
  scrollToBottom()
}

const getHelp = async () => {
  helpThinking.value = true
  let ctx = ''
  messages.value.slice(-4).forEach(function(m) {
    if (m.role==='ai') ctx += 'AI：' + m.content + '\n'
    if (m.role==='user') ctx += '我：' + m.content + '\n'
  })
  try {
    const res = await axios.post('/api/debate/help', { topic: topic.value, position: position.value, context: ctx, style: style.value })
    messages.value.push({ role: 'helper', content: '💡 ' + res.data.suggestion })
  } catch (err) {
    messages.value.push({ role: 'helper', content: '💡 试试从逻辑漏洞入手反驳。' })
  }
  helpThinking.value = false
  scrollToBottom()
}

const endDebate = () => {
  // 保存到后端历史
  axios.post('/api/history/debates', {
    topic: topic.value,
    position: position.value,
    rounds: round.value,
    messages: messages.value,
    time: new Date().toLocaleString()
  }).catch(function() {})
  // 跳转报告
  const data = encodeURIComponent(JSON.stringify({
    topic: topic.value,
    position: position.value,
    messages: messages.value
  }))
  router.push('/report/1?data=' + data)
}

const scrollToBottom = () => {
  nextTick(function() {
    if (msgBox.value) msgBox.value.scrollTop = msgBox.value.scrollHeight
  })
}
</script>

<style scoped>
.debate-page { max-width: 900px; margin: 0 auto; }
.setup-card { max-width: 600px; margin: 0 auto; }
.debate-header { margin-bottom: 20px; }
.messages { height: 400px; overflow-y: auto; padding: 15px; background: #f5f7fa; border-radius: 8px; margin-bottom: 15px; }
.msg-row { margin-bottom: 15px; }
.msg-bubble { max-width: 75%; padding: 12px 16px; border-radius: 12px; }
.user-msg { margin-left: auto; background: #409EFF; color: #fff; }
.ai-msg { margin-right: auto; background: #fff; border: 1px solid #e0e0e0; }
.msg-label { font-size: 12px; margin-bottom: 5px; opacity: 0.8; }
.msg-text { line-height: 1.6; white-space: pre-wrap; }
</style>
