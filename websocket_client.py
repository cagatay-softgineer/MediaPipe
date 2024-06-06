import websocket
import json

# Define the WebSocket server URL
server_url = "ws://localhost:8765"

# Define the list of data to send
data_list = [1, 2, 3, 4, 5] # Test Data

# Convert the list to JSON format
data_json = json.dumps(data_list)

# Define the WebSocket event handlers
def on_message(ws, message):
    """
    Callback function to handle incoming messages from the WebSocket server.

    Args:
        ws (WebSocket): The WebSocket connection object.
        message (str): The message received from the server.

    Returns:
        None
    """
    print(f"Received message: {message}")

def on_error(ws, error):
    """
    Callback function to handle WebSocket errors.

    Args:
        ws (WebSocket): The WebSocket connection object.
        error (Exception): The error that occurred.

    Returns:
        None
    """
    print(f"Error: {error}")

def on_close(ws):
    """
    Callback function to handle the WebSocket connection closing.

    Args:
        ws (WebSocket): The WebSocket connection object.

    Returns:
        None
    """
    print("Connection closed")

def on_open(ws):
    """
    Callback function to handle the opening of the WebSocket connection.

    Args:
        ws (WebSocket): The WebSocket connection object.

    Returns:
        None
    """
    print("Connection opened")
    # Send the JSON data to the WebSocket server
    ws.send(data_json)

# Create a WebSocket connection
ws = websocket.WebSocketApp(server_url,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open

# Run the WebSocket connection
ws.run_forever()