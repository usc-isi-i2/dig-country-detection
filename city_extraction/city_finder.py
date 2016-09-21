import ast
import json
import codecs
import re

city_to_country_dict_file = 'city_to_country_dict.json'
ground_truth_file = 'ground_truth.json'
output_annotations_file = 'annotations_with_text.json'

names = json.load(codecs.open(city_to_country_dict_file, 'r', 'utf-8'))

names = map(lambda x:x.lower(),names)

single_word = set()
mul_words = {}

for city in names:
	if ' ' not in city:
		single_word.add(city)
	else:
		tokens = city.split(" ")
		if tokens[0] in mul_words:
			mul_words[tokens[0]].append(city)
		else:
			mul_words[tokens[0]] = [city]

print("Dictionaries Loaded")

def get_ann_cities(read_text):
	read_text = read_text.lower()
	tokens = re.split(' |,|!',read_text)
	annotated_cities = []
	for token in tokens:
		if token in single_word:
			annotated_cities.append(token)
		if token in mul_words:
			for word in mul_words.get(token):
				if word in read_text:
					annotated_cities.append(word)
	return annotated_cities


def city_extractor(line):
	read_text = ast.literal_eval(line)['high_recall_readability_text']
	annotated_cities = get_ann_cities(read_text)
	return dict(annotated_cities = annotated_cities, correct_cities= [], high_recall_readability_text = read_text)

file = open(output_annotations_file, "w")
with open(ground_truth_file, 'r') as f:
	for index,line in enumerate(f):
		print(index)
		city_extractor(line)
		file.write(json.dumps(city_extractor(line)))
		file.write("\n")
file.close()