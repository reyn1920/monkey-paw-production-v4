from fastapi import APIRouter
router=APIRouter()
@router.post('/channel_presets/set')
def setp(body:dict): return {'ok':True,'applied':list((body.get('channels') or {}).keys())}
@router.get('/channel_presets/get')
def getp(): return {'ok':True,'channels':{}}
