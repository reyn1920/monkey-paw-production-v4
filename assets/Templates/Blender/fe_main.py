from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
try:
    from app.routes import automation, webhuman
except Exception:
    automation=None; webhuman=None
app=FastAPI(title='TRAE.AI Runtime Hub',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
@app.get('/health')
async def health(): return {'ok':True}
@app.get('/')
async def root(): return JSONResponse({'message':'TRAE.AI Runtime Hub online','routes':['/health','/automation/toggles','/webhuman/enqueue']})
if automation: app.include_router(automation.router,prefix='/automation',tags=['automation'])
if webhuman: app.include_router(webhuman.router,prefix='/webhuman',tags=['webhuman'])
