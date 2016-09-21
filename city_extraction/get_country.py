import ast
import json
import codecs
import re

annotations_file = 'annotations_with_text_1-25.json'
#annotations_file = 'annotations_with_text_26-50.json'

city_to_country_dict_file = 'city_to_country_dict.json'

city_to_country_dict = json.load(codecs.open(city_to_country_dict_file, 'r', 'utf-8'))

#city_to_country_dict = map(lambda x:x.lower(),city_to_country_dict)

count_of_zero_cities = 0
count_of_single_cities = 0
count_of_multiple_cities = 0

def get_correct_cities(line):
	return ast.literal_eval(line)['correct_cities']

with open(annotations_file, 'r') as f:
	for index,line in enumerate(f):
		print(index)
		correct_cities = get_correct_cities(line)
		print(correct_cities)
		country_count_dict = {}
		length = len(correct_cities)
		if(length == 0):
			count_of_zero_cities += 1
		elif(length == 1):
			count_of_single_cities += 1
		else:
			count_of_multiple_cities += 1
		for city in correct_cities:
			countries = city_to_country_dict[city]
			distinct_countries = set(countries)
			for country in distinct_countries:
				if country in country_count_dict:
					country_count_dict[country] += 1
				else:
					country_count_dict[country] = 1
		print(country_count_dict)
		
print(count_of_zero_cities)
print(count_of_single_cities)
print(count_of_multiple_cities)