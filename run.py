from backend.cyfox_backend import Cyfox
from frontend.main import CyfoxFrontend

backend = Cyfox()
frontend = CyfoxFrontend(backend)

frontend.run()
