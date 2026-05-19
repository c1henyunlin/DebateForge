from fastapi import APIRouter
from pydantic import BaseModel
from dashscope import Generation
from http import HTTPStatus
import random

router = APIRouter()
sessions = {}

class StartRequest(BaseModel):
    topic: str
    position: str
    angle: str = ""
    style: str = "formal"

class MessageRequest(BaseModel):
    session_id: int
    message: str
    style: str = "formal"

class HelpRequest(BaseModel):
    topic: str
    position: str
    context: str
    style: str = "formal"

def call_qwen(prompt, max_tokens=300):
    try:
        response = Generation.call(
            model="qwen-plus",
            prompt=prompt,
            result_format='message',
            temperature=0.8,
            max_tokens=max_tokens
        )
        if response.status_code == HTTPStatus.OK and response.output:
            choices = response.output.get('choices', [])
            if choices:
                return choices[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"API error: {e}")
    return None

@router.post("/start")
async def start(request: StartRequest):
    ai_pos = "正方" if request.position == "反方" else "反方"
    angle_text = f"\n对方预设角度：{request.angle}" if request.angle else ""
    
    style_guide = ""
    if request.style == "formal":
        style_guide = "\n请用正式辩论风格：使用'对方辩友''我方认为'等标准辩论用语，逻辑严密。"
    else:
        style_guide = "\n请用轻松对话风格：口语化表达，但论点仍需清晰。"
    
    prompt = f"""你正在参加辩论。
辩题：{request.topic}
你的立场：{ai_pos}（{'支持' if ai_pos == '正方' else '反对'}）{angle_text}{style_guide}

请发表开场白，2-3句话。"""
    
    opening = call_qwen(prompt, 250)
    if not opening:
        opening = f"作为{ai_pos}，我认为此议题值得深入探讨。" if request.style == "formal" else f"我选{ai_pos}！来吧～"
    
    sid = random.randint(10000, 99999)
    sessions[sid] = {
        "topic": request.topic,
        "user_pos": request.position,
        "ai_pos": ai_pos,
        "style": request.style,
        "history": []
    }
    
    return {"session_id": sid, "opening_message": opening, "ai_position": ai_pos}

@router.post("/message")
async def message(request: MessageRequest):
    session = sessions.get(request.session_id)
    if not session:
        return {"ai_response": "会话已过期。", "round_number": 0}
    
    style_guide = "用正式辩论风格回复。" if request.style == "formal" else "用轻松口语化风格回复。"
    
    history_text = ""
    for h in session["history"][-4:]:
        history_text += f"【{session['user_pos']}】{h['user']}\n【{session['ai_pos']}】{h['ai']}\n"
    
    prompt = f"""辩题：{session['topic']}
你的立场：【{session['ai_pos']}】
{style_guide}

对话：{history_text}
对方（{session['user_pos']}）：{request.message}

请反驳，3-5句话。"""
    
    reply = call_qwen(prompt, 400)
    if not reply:
        reply = f"作为{session['ai_pos']}，我需要更多角度分析。"
    
    session["history"].append({"user": request.message, "ai": reply})
    return {"ai_response": reply, "round_number": len(session["history"])}

@router.post("/help")
async def help(request: HelpRequest):
    style_note = "用正式辩论框架。" if request.style == "formal" else "用口语化表达。"
    
    prompt = f"""你是辩论教练，只帮【{request.position}】方出主意。你的立场必须和学员一致。

辩题：{request.topic}
学员立场：{request.position}

最近对话：
{request.context}

请给学员1个反驳思路或新角度。记住：
1. 你站【{request.position}】，不要站到对面去
2. 给出具体的反击点或新论据
3. {style_note}
4. 1-2句话"""
    
    suggestion = call_qwen(prompt, 250)
    if not suggestion:
        suggestion = f"作为{request.position}，试试从这个角度切入反驳。"
    return {"suggestion": suggestion}
