from fastapi import APIRouter
router=APIRouter()
@router.post('/compliance/check')
def chk(body:dict): return {'ok':True,'compliance_ok':True}
