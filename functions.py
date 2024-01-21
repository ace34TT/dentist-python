import pandas as pd
import numpy as np

def generate_combinations(arr):
    result = []
    for length in range(1, len(arr) + 1):
        combinations = get_combinations(arr, length)
        for combination in combinations:
            combined_id = [item["medicineId"] for item in combination]
            can_heal = list({frozenset(item.items()) for item in [inner_item for item in combination for inner_item in item["canHeal"]]})
            result.append({
                "combinedId": combined_id,
                "canHeal": [dict(item) for item in can_heal],
            })
    return result

def get_combinations(arr, length, start = 0, current = []):
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
    output = {'medicineId': [], 'efficiency': [], 'number': [], 'parameter': [], 'required': []}
    for symptom in symptoms:
        for medicine in medicines['canHeal']:
            if symptom['idParametre'] == medicine['idParametre']:
                output['medicineId'].append(medicine['medicineId'])
                output['efficiency'].append(medicine['niveau'])
                output['number'].append(0)  # Assuming 'number' is always 0 as per your example
                output['parameter'].append(medicine['idParametre'])
                output['required'].append(symptom['niveau'])
    return output


def find_required_number(data):
    df = pd.DataFrame(data)

    # Calculate the number of medicines needed
    df['number'] = np.ceil(df['required'] / df['efficiency']).astype(int)

    # Group by medicineId and parameter, and sum the number
    result = df.groupby(['medicineId', 'parameter'])['number'].sum().reset_index()

    # Calculate the result
    result['result'] = result['number'] * df['efficiency']
    return result