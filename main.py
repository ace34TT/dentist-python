import json
from functions import *
from database import *
from flask import Flask, jsonify , request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route('/api/medicaments-par-consultation', methods=['GET'])
# def get_data():
# idConsultaion = request.args.get('idConsultation', 0)
tuples_list = get_parametrePatients_par_consultation(1)
symptoms = [{"idParametre": item[0], "niveau": item[1]} for item in tuples_list]
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
    print(json.dumps(data))
    final_results = find_required_number(data)
    print(final_results)
    all_results.append(final_results)  

# print(all_results[0])

costs = []

for df in all_results:
    # Calculate cost for the current dataframe
    df['cost'] = df['number'] * df['price']
    total_cost = df['cost'].sum()
    costs.append(total_cost)

  # Calculate costs for each dataframe
  # for df in all_results:
  #     df['cost'] = df['number'] * df['price']
  #     total_cost = df['cost'].sum()
  #     costs.append(total_cost)

  # Sort dataframes by the total cost
  # sorted_dataframes = [x for _, x in sorted(zip(costs, all_results), key=lambda pair: pair[0])]
  # print(sorted_dataframes)
  
  # data_list = [df.to_dict(orient='records') for df in sorted_dataframes]
  # return jsonify(data_list)

# if __name__ == '__main__':
#     app.run(debug=True)




