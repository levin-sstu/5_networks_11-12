import asyncio
import websockets

clients = set()

async def echo(websocket):
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the message to all connected clients
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except:
        pass
    finally:
        clients.remove(websocket)

async def main():
    server = await websockets.serve(echo, "localhost", 6789)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
