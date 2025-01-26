import os
import json
import websocket
import gradio as gr

import constants
from app import get_voice

url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
_OPEN_AI_API_KEY = constants.OPENAI_KEY
_OPEN_AI_MODEL = constants.OPENAI_MODEL

headers = [
    "Authorization: Bearer " + _OPEN_AI_API_KEY,
    "OpenAI-Beta: realtime=v1"
]

def on_open(ws):
    print("Connected to server.")

def on_message(ws, message):
    data = json.loads(message)
    print("Received event:", json.dumps(data, indent=2))

ws = websocket.WebSocketApp(
    url,
    header=headers,
    on_open=on_open,
    on_message=on_message,
)

demo = gr.Interface(
    fn=get_voice,
    inputs=gr.Audio(sources="microphone", type="filepath", format="wav"),
    outputs=gr.Audio(),
    title="Ask your query",
)


ws.run_forever()