"""One-shot demo harness: sends a WS chat that yields a real approval nonce."""
import json
import websocket

ws = websocket.create_connection("ws://127.0.0.1:8765/ws/v1/stream", timeout=30)
ws.send(json.dumps({"action": "chat", "provider": "mock", "messages": [{"role": "user", "content": "Please run a command"}]}))
nonce = None
while True:
    msg = json.loads(ws.recv())
    if msg.get("event") == "tool_proposal":
        print("proposal:", msg["tool_call"]["tool_name"], "| decision:", msg["policy_decision"]["decision"])
        nonce = msg["policy_decision"].get("approval_nonce")
    elif msg.get("event") == "done":
        break
ws.close()
print("NONCE=" + (nonce or "NONE"))
