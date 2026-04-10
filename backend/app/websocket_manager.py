import asyncio
from typing import Dict, List
from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, task_id: str, websocket: WebSocket):
        await websocket.accept()
        if task_id not in self.active_connections:
            self.active_connections[task_id] = []
        self.active_connections[task_id].append(websocket)

    def disconnect(self, task_id: str, websocket: WebSocket):
        if task_id in self.active_connections:
            self.active_connections[task_id].remove(websocket)
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]

    async def broadcast(self, task_id: str, message: dict):
        if task_id in self.active_connections:
            dead = []
            for websocket in self.active_connections[task_id]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    dead.append(websocket)
            for ws in dead:
                self.active_connections[task_id].remove(ws)


manager = WebSocketManager()