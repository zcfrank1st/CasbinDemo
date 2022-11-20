import base64
import binascii
 
import casbin
import casbin_sqlalchemy_adapter
from postgresql_watcher import PostgresqlWatcher
 
from fastapi import FastAPI
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
from starlette.middleware.authentication import AuthenticationMiddleware
 
from fastapi_authz import CasbinMiddleware
 
 
# ------------
ADAPTER_URL='postgresql+psycopg2://postgres:1234@127.0.0.1/postgres'
MODEL_PATH='./rbac_model.conf'
WATCHER_HOST='127.0.0.1'
WATCHER_PORT='5432'
WATCHER_USER='postgres'
WATCHER_PASSWORD='1234'
WATCHER_DBNAME='postgres'
# ------------
 
 
app = FastAPI()
 
class BasicAuth(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None
 
        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")
 
        username, _, password = decoded.partition(":")
        return AuthCredentials(["authenticated"]), SimpleUser(username)
 
adapter = casbin_sqlalchemy_adapter.Adapter(ADAPTER_URL)
enforcer = casbin.Enforcer(MODEL_PATH, adapter)
watcher = PostgresqlWatcher(host=WATCHER_HOST, port=WATCHER_PORT, user=WATCHER_USER, password=WATCHER_PASSWORD, dbname=WATCHER_DBNAME)
watcher.set_update_callback(enforcer.load_policy)
enforcer.set_watcher(watcher)
 
app.add_middleware(CasbinMiddleware, enforcer=enforcer)
app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())
 
@app.get('/')
async def index():
    return "If you see this, you have been authenticated."
 
 
@app.get('/dataset1/protected')
async def auth_test():
    return "You must be alice to see this."

@app.get('/update')
async def update():
    return  watcher.update()