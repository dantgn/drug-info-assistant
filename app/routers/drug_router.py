from fastapi import APIRouter, HTTPException, Query, Path
from app.services.pubchem import fetch_drug_info, fetch_similar_compounds

router = APIRouter()

@router.get("/drug")
def get_drug_info(name: str = Query(..., description="Name of the drug")):
    response = fetch_drug_info(name)
    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])

    return response

@router.get("/drugs/{cid}/similar-compounds")
def get_similar_compounds(cid: str = Path(..., description="Cid of the drug")):
    response = fetch_similar_compounds(cid)
    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])

    return response