# 数据库设计

## 表结构

### debate_sessions
- id, topic, user_position, created_at

### debate_rounds
- id, session_id, round_number, user_message, ai_message

### angle_generations
- id, topic, generated_angles(JSON), created_at

### fallacy_reports
- id, session_id, report_content(JSON), created_at
