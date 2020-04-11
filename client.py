import asyncio
import websockets
import sys

async def client():
    uri = "ws://"+sys.argv[1]
    async with websockets.connect(uri) as websocket:
        x_test = '[0.0238,0.0318,0.0422,0.0399,0.0788,0.0766,0.0881,0.1143,0.1594,0.2048,0.2652,0.3100,0.2381,0.1918,0.1430,0.1735,0.1781,0.2852,0.5036,0.6166,0.7616,0.8125,0.7793,0.8788,0.8813,0.9470,1.0000,0.9739,0.8446,0.6151,0.4302,0.3165,0.2869,0.2017,0.1206,0.0271,0.0580,0.1262,0.1072,0.1082,0.0360,0.1197,0.2061,0.2054,0.1878,0.2047,0.1716,0.1069,0.0477,0.0170,0.0186,0.0096,0.0071,0.0084,0.0038,0.0026,0.0028,0.0013,0.0035,0.0060]'

        await websocket.send(x_test)
        print(f"> {x_test}")

        result = await websocket.recv()
        print(f"< {result}")

asyncio.get_event_loop().run_until_complete(client())
