from starlette.requests import Request


class LogHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request = Request(scope, receive=receive)

        async def sender(message):
            if message["type"] == "http.response.start":
                hdrs = {k.decode(): v.decode() for k, v in message["headers"]}
                endpoint = scope.get("endpoint")
                print(
                    f"[HDR] {request.method} {request.url.path} -> {hdrs} via {getattr(endpoint,'__name__',endpoint)}"
                )
            await send(message)

        await self.app(scope, receive, sender)
