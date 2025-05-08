import asyncio
import websockets
import time
import ssl
import json
import base64
import datetime
import uuid

from loguru import logger

async def test_ws():
    uri = "wss://10.8.123.4:9604/client-ws"

    # Create an SSL context that bypasses verification (for self-signed certificates)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE        
    retries = 3
    timeout = 100  # Set connection timeout to 100 seconds
    message_received = False

    session_id = str(uuid.uuid4())

    # Retry mechanism
    for attempt in range(retries):
        try:
            logger.info(f"Attempting to connect (Attempt {attempt + 1}/{retries})...")

            # Use `websockets.connect` to establish the WebSocket connection
            async with websockets.connect(uri, ssl=ssl_context) as websocket:
                logger.success("WebSocket connected successfully!")

                # Send message
                await websocket.send(json.dumps({
                    "type": "text-input",
                    "text": "Hello from client!",
                    "images": []
                }))

                # Continuously receive messages until the connection is closed
                while True:
                    try:
                        # Set timeout control, wait for a response up to `timeout` seconds
                        response = await asyncio.wait_for(websocket.recv(), timeout)
                        # logger.info("Received:", response)

                        # Print response content
                        # print("\n" + "="*40)
                        try:
                            data = json.loads(response)                            
                            # print(json.dumps(data, indent=2, ensure_ascii=False))
                            if "audio" == data["type"]:
                                if data["audio"]:
                                    try:
                                        # Extract the base64-encoded audio data
                                        audio_base64 = data["audio"]
                                        # Decode the base64 string into binary WAV data
                                        audio_bytes = base64.b64decode(audio_base64)
                                        # Generate a timestamp string like "20240507_153012"
                                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                                        filename = f"output_{session_id[:8]}_{timestamp}.wav"
                                        with open(filename, "wb") as f:
                                            f.write(audio_bytes)
                                        # logger.info(f"Save audio to {filename}")
                                        print(data["display_text"]["text"])
                                    except Exception as e:
                                        logger.error(f"An error occurred: {e}")
                            elif "backend-synth-complete" == data["type"]:
                                logger.info("backend synth complete")
                                message_received = True
                                break
                            elif "group-update" == data["type"]:
                                logger.info(data["type"])
                            elif "full-text" == data["type"]:
                                logger.success(data["text"])
                            elif "set-model-and-conf" == data["type"]:
                                logger.info(data["type"])
                            elif "control" == data["type"]:
                                logger.info(f'{data["type"]}: {data["text"]}')
                            else:
                                print(f"Received JSON: {data['type']}")
                            with open("output.jsonl", "a", encoding="utf-8") as f:
                                f.write(json.dumps(data, ensure_ascii=False) + "\n")
                        except json.JSONDecodeError:
                            if isinstance(response, bytes):
                                print(f"📦 Received binary data ({len(response)} bytes)")
                            else:
                                print("📨 Received text:")
                                print(response)
                        # print("="*40 + "\n")
                        
                    except asyncio.TimeoutError:
                        logger.error("No response received from server within timeout period.")
                        break  # Exit the loop after timeout
                if message_received:
                    logger.info("complete message received, exit loop...")
                    break
        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.InvalidHandshake) as e:
            logger.error(f"WebSocket connection failed: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        
        if attempt < retries - 1:
            logger.warning("Retrying in 5 seconds...")
            await asyncio.sleep(5)

    else:
        logger.error("Failed to connect after several attempts.")

# Run WebSocket test client
asyncio.run(test_ws())


'''
# chrome console
let ws = new WebSocket("wss://10.8.123.4:9604/client-ws");
ws.onopen = () => ws.send("hello from browser");
ws.onmessage = (e) => console.log("Received:", e.data);
'''