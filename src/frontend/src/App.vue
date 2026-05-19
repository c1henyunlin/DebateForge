<template>
  <div id="app">
    <el-container>
      <el-header>
        <el-menu
          :default-active="activeIndex"
          mode="horizontal"
          router
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/">
            <span>🏠 辩论锻炉</span>
          </el-menu-item>
          <el-menu-item index="/angle-generation">角度生成</el-menu-item>
          <el-menu-item index="/debate">辩论对战</el-menu-item>
          <el-menu-item index="/history">历史记录</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeIndex = ref('/')

watch(() => route.path, (newPath) => {
  activeIndex.value = newPath
})
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 
               'Microsoft YaHei', Arial, sans-serif;
}
.el-header {
  padding: 0;
}
.el-main {
  min-height: calc(100vh - 60px);
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
