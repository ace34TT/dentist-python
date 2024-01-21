import json
from functions import *
from database import *
symptoms = [
  { "idParametre": 7, "niveau": 8 },
  {
    "idParametre": 2,
    "niveau": 3,
  },
]
medicines = get_medicines()
# print(json.dumps(medicines))
_medicines = generate_medicines(medicines)
# print(json.dumps(_medicines))
combinations = generate_combinations(_medicines)
# print(json.dumps(combinations))

required_ids = [s['idParametre'] for s in symptoms]
filtered_treatments = [
    combination for combination in combinations
    if all(id in [heal['idParametre'] for heal in combination['canHeal']] for id in required_ids)
]

all_results = []  # Initialize an empty list to store dataframes

for treatment in filtered_treatments:
    data = generate_output(symptoms, treatment)
    final_results = find_required_number(data)
    all_results.append(final_results)  # Append the dataframe to the list

# print(all_results[0])

costs = []

for df in all_results:
    # Calculate cost for the current dataframe
    df['cost'] = df['number'] * df['price']
    total_cost = df['cost'].sum()
    costs.append(total_cost)

# Calculate costs for each dataframe
for df in all_results:
    df['cost'] = df['number'] * df['price']
    total_cost = df['cost'].sum()
    costs.append(total_cost)

# Sort dataframes by the total cost
sorted_dataframes = [x for _, x in sorted(zip(costs, all_results), key=lambda pair: pair[0])]
print(sorted_dataframes)



