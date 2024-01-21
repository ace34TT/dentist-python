import json
from functions import *
symptoms = [
  { "idParametre": 1, "niveau": 8 },
  {
    "idParametre": 2,
    "niveau": 3,
  },
]
medicines = [
  {
    "medicineId": 1,
    "name": "a",
    "canHeal": [{ "idParametre": 1, "niveau": 2 }],
  },
  {
    "medicineId": 2,
    "name": "b",
    "canHeal": [
      { "idParametre": 1, "niveau": 4 },
      {
        "idParametre": 2,
        "niveau": 2,
      },
    ],
  },
  {
    "medicineId": 3,
    "name": "c",
    "canHeal": [{ "idParametre": 3, "niveau": 4 }],
  },
]

combinations = generate_combinations(medicines)
required_ids = [s["idParametre"] for s in symptoms]
filtered_treatments = [combination for combination in combinations if all(id in [heal["idParametre"] for heal in combination["canHeal"]] for id in required_ids)]
# print(json.dumps(filtered_treatments))

symptoms = [
  { "idParametre": 1, "niveau": 8 },
  {
    "idParametre": 2,
    "niveau": 3,
  },
]

medicines = {
    "combinedId": [2],
    "canHeal": [
      { "idParametre": 1, "niveau": 4, "medicineId": 2 },
      { "idParametre": 2, "niveau": 2, "medicineId": 2 }
    ]
  }


data = generate_output(symptoms , medicines)
print(json.dumps(data))
final_result = find_required_number(data)
print(final_result)
