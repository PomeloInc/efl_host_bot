import asyncio
import json
import websockets

clients = []

async def handle_client(websocket, path):
    clients.append(websocket)
    print(f"Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            await handle_ws_message(websocket, message)
    finally:
        clients.remove(websocket)
        print(f"Client disconnected: {websocket.remote_address}")

async def handle_ws_message(websocket, message):
    print(f"Received message from {websocket.remote_address}: {message}")
    message = json.loads(message)
    message_type = message.get('messageType')
    if message_type == 'clientWebSocket':
        if 'data' in message:
            client_websocket = await websockets.connect(message['data'])
            async for data in client_websocket:
                await websocket.send(data)
    elif message_type == 'sendMessage':
        print("Sending message to clients:", message.get('data'))
        # Broadcast the message to all connected clients
        for client in clients:
            await client.send(message.get('data'))

async def main():
    server = await websockets.serve(handle_client, "localhost", 8888)
    print("WebSocket server started...")
    await server.wait_closed()

asyncio.run(main())
