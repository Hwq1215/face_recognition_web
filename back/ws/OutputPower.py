import asyncio

class OutputPower():
    async def run(self,arg,s,websocket):
        # 发送消息方法，单独和请求的客户端发消息
        await s('sssss', websocket)
        # 群发消息
        await s('起来hi')
