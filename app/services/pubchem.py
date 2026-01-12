import requests

PUBCHEM_BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

def fetch_drug_info(name: str):
    """ 
    Fetches relevant drug properties for a given drug name from PubChem.
    """
    # Query PubChem API for drug information
    url = f"{PUBCHEM_BASE_URL}/compound/name/{name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        compound_data = data.get("PC_Compounds", [])[0]

        if not compound_data:
          return {"error": "Compound not found"}

        properties = _extract_properties(compound_data)
        cid = properties.get("cid", "Unknown")

        return {
            "iupac_name": properties.get("IUPAC Name", "Unknown"),
            "molecular_formula": properties.get("Molecular Formula", "Unknown"),
            "molecular_weight": properties.get("Molecular Weight", "Unknown"),
            "log_p": properties.get("Log P", "Unknown"),
            "smiles": properties.get("SMILES", "Unknown"),
            "inchi": properties.get("InChI", "Unknown"),
            "cid": properties.get("cid", "Unknown"),
            "image_url": _compound_image_url(cid)
        }
    else:
        return {"error": "Drug not found or API error"}
    

def fetch_similar_compounds(cid: str):
    """ 
    Fetches similar compounds for a given CID from PubChem.
    """

    url = f"{PUBCHEM_BASE_URL}/compound/fastsimilarity_2d/cid/{cid}/cids/json"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        similar_compound_cids = data.get("IdentifierList", {}).get("CID", [])
        return { "cids": similar_compound_cids }
    else:
        return {"error": "Something went wrong"}

# --- private helpers ---

def _extract_properties(compound_data):
    properties = {}
    properties["cid"] = compound_data.get("id", {}).get("id", {}).get("cid", None)

    for prop in compound_data.get("props", [{}]):
        label = prop.get("urn", {}).get("label", "")
        value = prop.get("value", {})

        # Determine the value type and store it accordingly
        for key in ("sval", "ival", "fval", "binary"):
            if key in value:
                properties[label] = value[key]
                break

    return properties

def _compound_image_url(cid):
    if cid != "Unknown":
        return f"{PUBCHEM_BASE_URL}/compound/cid/{cid}/PNG"
    return ""