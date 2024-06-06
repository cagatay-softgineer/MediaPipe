import asyncio
import websockets

USERS = set()
port = 8765

async def msg_handler(websocket):
    """
    WebSocket message handler function.

    Registers the user, broadcasts incoming messages from the registered user to all connected users,
    and unregisters the user when the connection is closed.

    Args:
        websocket: The WebSocket connection object.

    Returns:
        None
    """
    global USERS
    try:
        # Register user
        USERS.add(websocket)
        # Broadcast incoming messages from the registered user
        async for message in websocket:
            # print(message)
            websockets.broadcast(USERS, message)
       
    finally:
        # Unregister user
        USERS.remove(websocket)
        

async def main():
    """
    Main asynchronous function to start the WebSocket server.

    Starts the WebSocket server and waits for connections. The port number is always 8765.

    Returns:
        None
    """
    print("Starting websocket server")
    # The port number is always 8765
    server1 = await websockets.serve(msg_handler, '', port)
    await asyncio.gather(server1.wait_closed())


asyncio.run(main())
