# DebateForge API 文档

## 接口列表

### 角度生成
- `POST /api/angle/generate` - 生成正反方论证角度

### 辩论对战
- `POST /api/debate/start` - 开始辩论
- `POST /api/debate/message` - 发送辩论消息
- `POST /api/debate/help` - AI助攻

### 逻辑报告
- `POST /api/report/generate` - 生成分析报告

### 历史记录
- `GET /api/history/debates` - 获取辩论历史
- `POST /api/history/debates` - 保存辩论记录
- `GET /api/history/angles` - 获取角度历史
