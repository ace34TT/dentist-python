import pandas as pd
import numpy as np
from itertools import combinations
from typing import List, Dict

def generate_medicines(data):
    medicines = []
    for row in data:
        medicine_id, name, param_id, efficiency , price = row

        # Check if the medicine already exists in the list
        medicine_exists = next((m for m in medicines if m["medicineId"] == medicine_id), None)

        # If the medicine doesn't exist, add it to the list
        if not medicine_exists:
            medicines.append({
                "medicineId": medicine_id,
                "name": name,
                "price": price,
                "canHeal": [{"idParametre": param_id, "niveau": efficiency}]
            })
        else:
            # If the medicine already exists, add the parameter to its "canHeal" list
            medicine_exists["canHeal"].append({"idParametre": param_id, "niveau": efficiency})
    return medicines

def generate_combinations(arr):
    result = []
    for length in range(1, len(arr) + 1):
        combinations = get_combinations(arr, length)
        for combination in combinations:
            combined_id = [item['medicineId'] for item in combination]
            flat_items = [
                {'idParametre': inner_item['idParametre'],
                 'niveau': inner_item['niveau'],
                 'medicineId': item['medicineId'],
                 'price':item['price'],
                 }
                for item in combination for inner_item in item['canHeal']
            ]
            can_heal = list({frozenset(item.items()): item for item in flat_items}.values())
            result.append({
                'combinedId': combined_id,
                'canHeal': can_heal,
            })
    return result

def get_combinations(arr, length, start=0, current=None):
    if current is None:
        current = []
    result = []
    if length == 0:
        result.append(current[:])
        return result
    for i in range(start, len(arr)):
        current.append(arr[i])
        result.extend(get_combinations(arr, length - 1, i + 1, current))
        current.pop()
    return result

def generate_output(symptoms, medicines):
    output = {'medicineId': [], 'efficiency': [], 'number': [], 'parameter': [], 'required': [] , 'price' : []}
    for symptom in symptoms:
        for medicine in medicines['canHeal']:
            if symptom['idParametre'] == medicine['idParametre']:
                output['medicineId'].append(medicine['medicineId'])
                output['efficiency'].append(medicine['niveau'])
                output['number'].append(0)  # Assuming 'number' is always 0 as per your example
                output['parameter'].append(medicine['idParametre'])
                output['required'].append(symptom['niveau'])
                output['price'].append(medicine['price'])
                
    return output

def find_required_number(data):
    df = pd.DataFrame(data)

    # Calculate the number of medicines needed
    df['number'] = np.ceil(df['required'] / df['efficiency']).astype(int)

    # Group by medicineId and parameter, and sum the number
    result = df.groupby(['medicineId', 'parameter']).agg({'number': 'sum', 'required': 'first', 'efficiency': 'first', 'price': 'first'}).reset_index()

    # Calculate the result
    result['result'] = result['number'] * result['efficiency']
    
    return result