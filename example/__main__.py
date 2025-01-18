from daedalus.core.factory import DaedalusFactory
from example.src.main_module import MainModule

app = DaedalusFactory(
    module=MainModule,
    framework='fastapi'  # or 'falcon' for the falcon
)

app.serve(
    port=8000,
    host='localhost',
    cors=True
)