from fastapi import APIRouter
router=APIRouter()
@router.post('/outro/append_highlight')
def x(body:dict): return {'ok':True,'appended':True}
