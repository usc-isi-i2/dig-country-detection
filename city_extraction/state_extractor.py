import ast
import json
import codecs
import re

path = '../'
state_to_country_dict_file = path + 'state_country_dict.json'
ground_truth_file = path + 'ann_city_title.json'
output_annotations_file = path + 'ann_city_title_state.json'

names = json.load(codecs.open(state_to_country_dict_file, 'r', 'utf-8'))

names = map(lambda x:x.lower(),names)

single_word = set()
mul_words = {}

for state in names:
	if ' ' not in state:
		single_word.add(state)
	else:
		tokens = state.split(" ")
		if tokens[0] in mul_words:
			mul_words[tokens[0]].append(state)
		else:
			mul_words[tokens[0]] = [state]

print("Dictionaries Loaded")

def get_ann_states(read_text):
	read_text = read_text.lower()
	tokens = re.split(' |,|!|\.',read_text)
	annotated_states = []
	for token in tokens:
		if token in single_word:
			annotated_states.append(token)
		if token in mul_words:
			for word in mul_words.get(token):
				if word in read_text:
					annotated_states.append(word)
	return annotated_states

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def state_extractor(line):
	read_text = ast.literal_eval(line)['high_recall_readability_text']
	line = ast.literal_eval(line)
	annotated_states = get_ann_states(read_text)
	return merge_two_dicts(line, dict(annotated_states = annotated_states, correct_states = []))

file = open(output_annotations_file, "w")
with open(ground_truth_file, 'r') as f:
	for index, line in enumerate(f):
		print(index)
		state_extractor(line)
		file.write(json.dumps(state_extractor(line)))
		file.write("\n")
file.close()