from fastapi import APIRouter
router=APIRouter()
@router.post('/dupes/scan')
def s(body:dict): return {'ok':True,'dupes':[]}
