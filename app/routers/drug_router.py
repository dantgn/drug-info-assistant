from fastapi import APIRouter, HTTPException, Query
from app.services.drug_info import get_drug_info_from_pubchem

router = APIRouter()

@router.get("/drug")
def get_drug_info(name: str = Query(..., description="Name of the drug to request information")):
    info = get_drug_info_from_pubchem(name)
    if "error" in info:
        raise HTTPException(status_code=404, detail=info["error"])

    return info
