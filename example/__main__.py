from daedalus.core.factory import DaedalusFactory
from example.src.main_module import MainModule

app = DaedalusFactory(MainModule)

app.serve(
    port=8080,
    host='localhost',
    cors=True
)