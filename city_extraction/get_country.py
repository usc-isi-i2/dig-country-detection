import ast
import json
import codecs
import re


path = './'
annotations_file = path + 'ann_city_title_state_1_25.json'
#annotations_file = path + 'ann_city_title_state_26_50.json'

city_to_country_dict_file = path + 'city_country_dict_15000_ordered_by_pop.json'
state_to_country_dict_file = path + 'state_country_dict.json'

city_to_country_dict = json.load(codecs.open(city_to_country_dict_file, 'r', 'utf-8'))
state_to_country_dict = json.load(codecs.open(state_to_country_dict_file, 'r', 'utf-8'))

city_to_country_dict_lower = {}
state_to_country_dict_lower = {}

for city, countries in city_to_country_dict.items():
	city_to_country_dict_lower[city.lower()] = countries[0][0]

for state, countries in state_to_country_dict.items():
	state_to_country_dict_lower[state.lower()] = countries

count_of_zero_cities = 0
count_of_single_cities = 0
count_of_multiple_cities = 0
count_of_correct_finds = 0
count_of_no_distinct = 0
count_of_incorrect_finds = 0
count_total = 0

def get_correct_cities(line):
	return ast.literal_eval(line)['correct_cities']

def get_correct_states(line):
	return ast.literal_eval(line)['correct_states']

def get_correct_cities_title(line):
	return ast.literal_eval(line)['correct_cities_title']

def get_correct_country(line):
	return ast.literal_eval(line)['correct_country']

with open(annotations_file, 'r') as f:
	for index, line in enumerate(f):
		count_total += 1
		#print(index)
		correct_cities = get_correct_cities(line)
		correct_states = get_correct_states(line)
		correct_cities_title = get_correct_cities_title(line)
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
			country = city_to_country_dict_lower[city]
			if country in country_count_dict:
				country_count_dict[country] += 1
			else:
				country_count_dict[country] = 1
		for city in correct_cities_title:
			country = city_to_country_dict_lower[city]
			if country in country_count_dict:
				country_count_dict[country] += 1
			else:
				country_count_dict[country] = 1
		for state in correct_states:
			countries = state_to_country_dict_lower[state]
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
			print(correct_states)
			print(correct_cities_title)
			print(country_count_dict)
			print(countrymax)
			print(get_correct_country(line))
		elif(not distinct):
			print("No Distinct Max")
			count_of_no_distinct += 1
			print(correct_cities)
			print(correct_states)
			print(correct_cities_title)
			print(country_count_dict)
			print("Predicted:{}".format(countrymax))
			print("Correct:{}".format(get_correct_country(line)))
		else:
			print("Incorrect Find")
			count_of_incorrect_finds += 1
			print(correct_cities)
			print(correct_states)
			print(correct_cities_title)
			print(country_count_dict)
			print("Predicted:{}".format(countrymax))
			print("Correct:{}".format(get_correct_country(line)))
		print('---------------------------')

print("count_total:{}".format(count_total))
print("count_of_correct_finds:{} [{}%]".format(count_of_correct_finds, (count_of_correct_finds*1.0/count_total)*100))
print("count_of_incorrect_finds:{} [{}%]".format(count_of_incorrect_finds, (count_of_incorrect_finds*1.0/count_total)*100))
print("count_of_multiple_max_cities:{} [{}%]".format(count_of_no_distinct, count_of_no_distinct*1.0/count_total*100))
print("count_of_zero_cities:{} [{}%]".format(count_of_zero_cities, count_of_zero_cities*1.0/count_total*100))
print("count_of_single_cities:{} [{}%]".format(count_of_single_cities, count_of_single_cities*1.0/count_total*100))
print("count_of_multiple_cities:{} [{}%]".format(count_of_multiple_cities, count_of_multiple_cities*1.0/count_total*100))