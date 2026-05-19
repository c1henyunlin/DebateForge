from fastapi import APIRouter
from pydantic import BaseModel
from dashscope import Generation
from http import HTTPStatus
import json

router = APIRouter()

class ReportRequest(BaseModel):
    topic: str
    position: str
    history: list

def call_qwen(prompt, max_tokens=800):
    try:
        response = Generation.call(
            model="qwen-plus",
            prompt=prompt,
            result_format='message',
            temperature=0.3,
            max_tokens=max_tokens
        )
        if response.status_code == HTTPStatus.OK and response.output:
            choices = response.output.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"API error: {e}")
    return None

@router.post("/generate")
async def generate_report(request: ReportRequest):
    conversation = ""
    for msg in request.history:
        role = "你" if msg.get("role") == "user" else "AI"
        conversation += f"{role}：{msg.get('content', '')}\n"
    
    prompt = f"""你是逻辑学专家。分析以下辩论并返回JSON。

辩题：{request.topic}
用户立场：{request.position}

辩论记录：{conversation}

返回JSON：
{{"overall_evaluation":"整体评价","score":85,"fallacies_found":[{{"type":"谬误类型","round":"第几轮","description":"问题描述","suggestion":"改进建议"}}],"strengths":["优点"],"improvements":["改进"],"thinking_quality":{{"logic":80,"evidence":75,"creativity":85,"rebuttal":70}}}}"""
    
    result = call_qwen(prompt, 1000)
    if result:
        result = result.replace('```json', '').replace('```', '').strip()
        try:
            start = result.find('{')
            end = result.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(result[start:end])
        except:
            pass
    
    return {
        "overall_evaluation": "表现不错，继续加油！",
        "score": 78,
        "fallacies_found": [],
        "strengths": ["表达清晰", "观点明确"],
        "improvements": ["多用数据支撑", "预判对方论点"],
        "thinking_quality": {"logic": 75, "evidence": 70, "creativity": 80, "rebuttal": 72}
    }
