from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, str] = {}
        self.chat_history: list[str] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def add_user(self, websocket: WebSocket, username: str):
        self.active_connections[websocket] = username

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def broadcast(self, message: str):
        self.chat_history.append(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    async def send_history(self, websocket: WebSocket):
        for msg in self.chat_history:
            await websocket.send_text(msg)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("room.html", {"request": request})

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket)
    manager.add_user(websocket, username)
    await manager.send_history(websocket)
    await manager.broadcast(f"📢 {username} joined the chat.")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"👋 {username} left the chat.")
