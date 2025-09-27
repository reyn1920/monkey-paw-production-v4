from fastapi import APIRouter
router=APIRouter()
@router.post('/scheduler/seed_all')
def seed(): return {'ok':True,'seeded':6}
@router.post('/scheduler/enable_shorts')
def en(body:dict): return {'ok':True,'per_day':body.get('per_day',3)}
@router.get('/scheduler/queue')
def q(): return {'ok':True,'queue':[]}
