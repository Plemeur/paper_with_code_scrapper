import json
with open('dataset.json', 'r') as f:
    papers_dict = json.load(f)


dataset_cleaned = {}

for key, attributes in papers_dict.items():
    dataset_cleaned[key] = {}
    for attribute, values in attributes.items():
        if attribute == "link":
            dataset_cleaned[key][attribute] = values
        else:
            # Sets items are not JSON Serializable.
            dataset_cleaned[key][attribute] = list(set(values))

with open('dataset_cleaned.json', 'w') as f:
    json.dump(dataset_cleaned, f)