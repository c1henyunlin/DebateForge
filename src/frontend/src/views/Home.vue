<template>
  <div class="home">
    <div class="hero">
      <h1>⚔️ DebateForge</h1>
      <p class="subtitle">AI辩论陪练与批判性思维训练平台</p>
      <p class="description">
        通过AI技术，帮助你从多角度思考问题，提升辩论与论证能力
      </p>
      
      <el-row :gutter="20" class="feature-cards">
        <el-col :span="8">
          <el-card shadow="hover" @click="$router.push('/angle-generation')" class="clickable-card">
            <div style="font-size: 40px; margin-bottom: 10px;">💡</div>
            <h3>多角度论证生成</h3>
            <p>输入议题，即刻获得正反双方的多元论证角度，打开写作思路</p>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover" @click="$router.push('/debate')" class="clickable-card">
            <div style="font-size: 40px; margin-bottom: 10px;">🗣️</div>
            <h3>AI辩论对战</h3>
            <p>与AI进行实时辩论，模拟对手立场，提升你的论证与反驳能力</p>
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card shadow="hover" @click="$router.push('/history')" class="clickable-card">
            <div style="font-size: 40px; margin-bottom: 10px;">📊</div>
            <h3>逻辑漏洞检测</h3>
            <p>获得详细的逻辑分析报告，发现思维盲点，持续改进论证能力</p>
          </el-card>
        </el-col>
      </el-row>
      
      <div style="margin-top: 40px;">
        <el-button type="primary" size="large" @click="$router.push('/angle-generation')">
          开始使用
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 60px 20px;
}

.hero h1 {
  font-size: 48px;
  color: #303133;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 24px;
  color: #606266;
  margin-bottom: 20px;
}

.description {
  font-size: 16px;
  color: #909399;
  margin-bottom: 60px;
}

.feature-cards {
  margin-top: 40px;
}

.clickable-card {
  cursor: pointer;
  transition: transform 0.3s;
  height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.clickable-card:hover {
  transform: translateY(-5px);
}

.clickable-card h3 {
  margin: 15px 0;
  color: #303133;
}

.clickable-card p {
  color: #909399;
  font-size: 14px;
  line-height: 1.6;
}
</style>
