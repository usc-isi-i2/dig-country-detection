import ast
import json
import codecs
import re

#annotations_file = 'annotations_with_alt_1-25.json'
annotations_file = 'annotations_with_alt_26-50.json'
#annotations_file = 'annotations_with_text_1-25.json'
#annotations_file = 'annotations_with_text_26-50.json'


#city_to_country_dict_file = 'city_country_dict_with_alt.json'
city_to_country_dict_file = 'city_country_dict_alternates.json'

city_to_country_dict = json.load(codecs.open(city_to_country_dict_file, 'r', 'utf-8'))

city_to_country_dict_lower = {}

for city,countries in city_to_country_dict.items():
	city_to_country_dict_lower[city.lower()] = countries

#city_to_country_dict = map(lambda x:x.lower(),city_to_country_dict)

count_of_zero_cities = 0
count_of_single_cities = 0
count_of_multiple_cities = 0
count_of_correct_finds = 0
count_of_no_distinct = 0
count_of_incorrect_finds = 0
count_total = 0

def get_correct_cities(line):
	return ast.literal_eval(line)['correct_cities']

def get_correct_country(line):
	return ast.literal_eval(line)['correct_country']

with open(annotations_file, 'r') as f:
	for index,line in enumerate(f):
		count_total += 1
		#print(index)
		correct_cities = get_correct_cities(line)
		#print(correct_cities)
		country_count_dict = {}
		length = len(correct_cities)
		if(length == 0):
			count_of_zero_cities += 1
			continue
		elif(length == 1):
			count_of_single_cities += 1
		else:
			count_of_multiple_cities += 1
		for city in correct_cities:
			countries = city_to_country_dict_lower[city]
			distinct_countries = set(countries)
			for country in distinct_countries:
				if country in country_count_dict:
					country_count_dict[country] += 1
				else:
					country_count_dict[country] = 1
		countmax = 0
		distinct = False
		countrymax = None
		for country, count in country_count_dict.items():
			if(count > countmax):
				countmax = count
				countrymax = country
				distinct = True
			elif(count == countmax):
				distinct = False
		correct_country = get_correct_country(line)
		if(countrymax == correct_country and distinct):
			print("Correct Find")
			count_of_correct_finds += 1
			print(correct_cities)
			print(country_count_dict)
			print(countrymax)
			print(get_correct_country(line))
		elif(not distinct):
			print("No Distinct Max")
			count_of_no_distinct += 1
			print(correct_cities)
			print(country_count_dict)
			print("Predicted:{}".format(countrymax))
			print("Correct:{}".format(get_correct_country(line)))
		else:
			print("Incorrect Find")
			count_of_incorrect_finds += 1
			print(correct_cities)
			print(country_count_dict)
			print("Predicted:{}".format(countrymax))
			print("Correct:{}".format(get_correct_country(line)))
		print('---------------------------')

print("count_total:{}".format(count_total))
print("count_of_correct_finds:{} [{}%]".format(count_of_correct_finds, count_of_correct_finds/count_total*100))
print("count_of_incorrect_finds:{} [{}%]".format(count_of_incorrect_finds, count_of_incorrect_finds/count_total*100))
print("count_of_multiple_max_cities:{} [{}%]".format(count_of_no_distinct, count_of_no_distinct/count_total*100))
print("count_of_zero_cities:{} [{}%]".format(count_of_zero_cities, count_of_zero_cities/count_total*100))
print("count_of_single_cities:{} [{}%]".format(count_of_single_cities, count_of_single_cities/count_total*100))
print("count_of_multiple_cities:{} [{}%]".format(count_of_multiple_cities, count_of_multiple_cities/count_total*100))