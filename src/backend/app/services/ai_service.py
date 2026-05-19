import os
import json
import random
from typing import Dict
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.model = os.getenv("MODEL_NAME", "qwen-plus")
        self.use_mock = False
        
        if self.api_key and len(self.api_key) > 20:
            try:
                import dashscope
                dashscope.api_key = self.api_key
                self.use_mock = False
                print(f"Qianwen API ready: {self.model}")
            except Exception as e:
                print(f"Init failed: {e}")
                self.use_mock = True
        else:
            print("No valid API key, using mock")
            self.use_mock = True
    
    async def generate_angles(self, topic: str) -> Dict:
        if self.use_mock:
            print("Using mock data")
            return self._mock_data(topic)
        
        try:
            return await self._call_qianwen(topic)
        except Exception as e:
            print(f"API error: {e}")
            return self._mock_data(topic)
    
    async def _call_qianwen(self, topic: str) -> Dict:
        from dashscope import Generation
        
        prompt = f"""请针对以下议题生成正反双方各3个论证角度。严格按JSON格式返回。

议题：{topic}

JSON格式：
{{"topic":"{topic}","pro_position":[{{"angle":"角度名","argument":"2-3句论证","type":"逻辑/数据/情感"}},...],"con_position":[...]}}

要求：角度针对具体议题，有深度，类型标注准确。"""
        
        print(f"Calling API for: {topic}")
        
        response = Generation.call(
            model=self.model,
            prompt=prompt,
            result_format='message',
            temperature=0.8,
            max_tokens=2000
        )
        
        if response.status_code == HTTPStatus.OK:
            content = response.output.choices[0].message.content
            print(f"API raw: {content[:200]}")
            
            content = content.replace('```json', '').replace('```', '').strip()
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                result = json.loads(content[start:end])
                result['topic'] = topic
                return result
        
        print(f"API failed: {response.status_code}")
        return self._mock_data(topic)
    
    def _mock_data(self, topic: str) -> Dict:
        return {
            "topic": topic,
            "pro_position": [
                {"angle": f"关于{topic}的个人自由", "argument": f"在{topic}上，个人应享有自主选择权。这尊重个体差异，激发创新。", "type": "逻辑"},
                {"angle": f"数据支持", "argument": f"调查显示，{topic}方面持开放态度的群体满意度高出30%。", "type": "数据"},
                {"angle": f"人文关怀", "argument": f"每个受{topic}影响的人都有自己的感受，理解他们很重要。", "type": "情感"}
            ],
            "con_position": [
                {"angle": f"社会秩序", "argument": f"{topic}若完全放开可能冲击秩序，需要平衡。", "type": "逻辑"},
                {"angle": f"风险数据", "argument": f"研究显示{topic}相关决策失败率达35%，需谨慎。", "type": "数据"},
                {"angle": f"保护弱者", "argument": f"并非人人都能为{topic}做出明智选择，弱者需要保护。", "type": "情感"}
            ]
        }
    
    async def debate_reply(self, message: str, history: list) -> str:
        if not self.use_mock:
            try:
                from dashscope import Generation
                ctx = "\n".join([f"对方: {h.get('user','')}\n你: {h.get('ai','')}" for h in history[-3:]])
                response = Generation.call(
                    model=self.model,
                    prompt=f"辩论：\n{ctx}\n\n对方：{message}\n\n反驳（2-3句）：",
                    temperature=0.8,
                    max_tokens=300
                )
                if response.status_code == HTTPStatus.OK:
                    return response.output.choices[0].message.content
            except Exception as e:
                print(f"Debate API error: {e}")
        
        replies = ["有趣的观点，但忽略了另一方面...", "这个论证前提值得商榷。", "我理解你的立场，但数据不支持。"]
        return random.choice(replies)
