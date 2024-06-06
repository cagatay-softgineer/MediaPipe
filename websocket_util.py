# WebSocket Client
import websockets

ws_address = "ws://localhost:8765"

# Send message
async def send(message):
    """
    Sends a message to a WebSocket server and waits for a response.

    Args:
        message: The message to send to the WebSocket server.

    Returns:
        str: The response received from the WebSocket server.

    Raises:
        websockets.exceptions.WebSocketException: If an error occurs during the WebSocket communication.

    Example:
        >>> response = await send("Hello, WebSocket!")
        >>> print(response)
        "Received: Hello, WebSocket!"
    """
    async with websockets.connect(ws_address) as websocket:
        await websocket.send(str(message))
        await websocket.recv()