from fastapi import APIRouter
router=APIRouter()
@router.post('/captions/queue')
def c(body:dict): return {'ok':True,'queued':True}
