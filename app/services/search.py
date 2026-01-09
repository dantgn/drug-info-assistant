import requests


def _extract_properties(compound_data):
    
    properties = {}

    for prop in compound_data.get("props", [{}]):
        label = prop.get("urn", {}).get("label", "")
        value = prop.get("value", {})

        # Determine the value type and store it accordingly
        if "sval" in value:
            properties[label] = value["sval"]
        elif "ival" in value:
            properties[label] = value["ival"]
        elif "fval" in value:
            properties[label] = value["fval"]
        elif "binary" in value:
            properties[label] = value["binary"]

    return properties

def get_drug_info_from_pubchem(name: str):
    # Query PubChem API for drug information
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/json"
    response = requests.get(url)

    if response.status_code == 200:

        data = response.json()

        # Get the first compound data
        compound_data = data.get("PC_Compounds", [])[0]
        
        # Extract properties once
        properties = _extract_properties(compound_data)

        # Now we can directly access the required properties from the dictionary
        iupac_name = properties.get("IUPAC Name", "Unknown")
        molecular_formula = properties.get("Molecular Formula", "Unknown")
        molecular_weight = properties.get("Molecular Weight", "Unknown")
        log_p = properties.get("Log P", "Unknown")
        smiles = properties.get("SMILES", "Unknown")
        inchi = properties.get("InChI", "Unknown")

        return { 
            "name": iupac_name,
            "molecular_formula": molecular_formula,
            "molecular_weight": molecular_weight,
            "log_p": log_p,
            "smiles": smiles,
            "inchi": inchi,
        }
    else:
        return {"error": "Drug not found or API error"}