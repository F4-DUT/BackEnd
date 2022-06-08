from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


import asyncio
import websockets


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def info(request):
  asyncio.run(ws())
  return Response("Respuesta")

async def ws():
    async with websockets.serve(echo, "localhost", 8002):
        await asyncio.Future()  # run forever

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)