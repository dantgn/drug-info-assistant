import requests


def extract_properties(compound_data):
    
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

def get_drug_info_from_pubchem(name: str):
    # Query PubChem API for drug information
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/json"
    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()
        compound_data = data.get("PC_Compounds", [])[0]

        if not compound_data:
          return {"error": "Compound not found"}

        properties = extract_properties(compound_data)
        
        return {
            "iupac_name": properties.get("IUPAC Name", "Unknown"),
            "molecular_formula": properties.get("Molecular Formula", "Unknown"),
            "molecular_weight": properties.get("Molecular Weight", "Unknown"),
            "log_p": properties.get("Log P", "Unknown"),
            "smiles": properties.get("SMILES", "Unknown"),
            "inchi": properties.get("InChI", "Unknown"),
            "cid": properties.get("cid", "Unknown")
        }
    else:
        return {"error": "Drug not found or API error"}