from pydantic import BaseModel
import uvicorn


class DaedalusFactoryOptions(BaseModel):
    port: int
    cors: bool
    log_level: str | int | None

class DaedalusFactory:
    options: DaedalusFactoryOptions

    def __init__(self, options: DaedalusFactoryOptions):
        self.options = options
        self.config = uvicorn.Config("main:app", port=options.port, log_level=options.log_level)
        self.server = uvicorn.Server(self.config)
        self.serve()


    async def serve(self):
        await self.server.serve()