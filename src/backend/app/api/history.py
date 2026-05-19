from fastapi import APIRouter

router = APIRouter()

# 内存存储（重启后清空）
debate_history = []
angle_history = []

@router.get("/debates")
async def get_debates():
    return debate_history

@router.post("/debates")
async def save_debate(data: dict):
    debate_history.insert(0, {
        "id": len(debate_history) + 1,
        "topic": data.get("topic", ""),
        "position": data.get("position", ""),
        "rounds": data.get("rounds", 0),
        "messages": data.get("messages", []),
        "report": data.get("report", None),
        "time": data.get("time", "")
    })
    return {"status": "ok"}

@router.get("/angles")
async def get_angles():
    return angle_history

@router.post("/angles")
async def save_angle(data: dict):
    angle_history.insert(0, {
        "id": len(angle_history) + 1,
        "topic": data.get("topic", ""),
        "time": data.get("time", "")
    })
    return {"status": "ok"}

@router.delete("/debates/{id}")
async def delete_debate(id: int):
    global debate_history
    debate_history = [d for d in debate_history if d["id"] != id]
    return {"status": "ok"}
