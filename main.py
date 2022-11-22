import casbin
import casbin_sqlalchemy_adapter
from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware 
from fastapi_authz import CasbinMiddleware
import yaml

from middleware import BasicAuth


with open('config.yaml', 'r') as f:
    config_dict = yaml.safe_load(f)

ADAPTER_URI=config_dict['adapter_uri']
MODEL_PATH=config_dict['model_path']
 
 
app = FastAPI()

adapter = casbin_sqlalchemy_adapter.Adapter(ADAPTER_URI)
enforcer = casbin.Enforcer(MODEL_PATH, adapter)

# def load(event):
#     enforcer.load_policy()
# from watcher import RedisWatcher
# enforcer.set_watcher(RedisWatcher(load, ))

from scheduler import SyncPolicy
SyncPolicy(lambda: enforcer.load_policy()).start()
 
app.add_middleware(CasbinMiddleware, enforcer=enforcer)
app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())
 
@app.get('/')
async def index():
    return "If you see this, you have been authenticated."
 
 
@app.get('/dataset1/protected')
async def auth_test():
    return "You must be alice to see this."
