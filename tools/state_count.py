#!/usr/bin/python3
# coding=utf-8
import json

with open("../country_codes.json") as f:
	data = json.load(f)
	sum = 0
	for country in data:
		l = 0
		state_codes = []
		if "subdivisions" in country:
			l = len(country["subdivisions"])
			for subdivision in country["subdivisions"]:
				state_codes.append(subdivision["code"])
		print(country["country_iso2"], l)
		print(state_codes)
		sum += l
	print("country_count:",len(data))
	print("sum:",sum)