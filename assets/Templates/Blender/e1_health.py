from fastapi import APIRouter
router=APIRouter()
@router.get('/health')
def ok(): return {'ok':True}
