#!/usr/bin/python3
# coding=utf-8
import json

need_language = {
	"de": None,
	"en": None,
	"es": None,
	"fr": None,
	"it": None,
	"ja": None,
	"ko": None,
	"nl": None,
	"pt": None,
	"sv": None,
	"zh": None,
	"zh-hans": None,
	"zh-hant": None,
}

def convert_language_names(language_names):
	ln = {}
	for key,value in language_names.items():
		if not key in need_language:
			continue
		ln[key] = value["value"]
	for key in need_language.keys():
		if not key in ln:
			print(language_names["en"], "has not ", key)
	return ln

"""
standardized structure:
[
	{
		"country_iso2": "CN",
		"country_iso3": "CHN",
		"language_names": {
			"zh": "中国",
			"en": "China"
		},
		"subdivisions": [
			{
				"code": "CN-BJ",
				"language_names": {
					"zh": "北京",
					"en": "Beijing"
				},
				"url": "/wiki/Beijing",
				"wiki_page_id": ""
			}
		]
	}
]
"""
with open("../country_codes.json", 'r') as f:
	countries = json.load(f)
	std_countries = []
	for country in countries:
		std_country = {
			"country_iso2": country["country_iso2"],
			"country_iso3": country["country_iso3"],
			"language_names": convert_language_names(country["language_names"]),
			"url": country["url"],
			"wiki_page_id": country["wiki_page_id"],
		}
		if std_country["country_iso2"] == "TW":
			std_country["language_names"] = {
				"en": "Taiwan",
				"zh-hans": "台湾",
				"zh-hant": "台灣",
				"zh": "台湾",
				"ja": "台湾",
				"pt": "Taiwan"
			}
		subdivisions = []
		exist = {}
		if not "subdivisions" in country:
			std_countries.append(std_country)
			continue
		for subdivision in country["subdivisions"]:
			#if subdivision["code"] in ["TD-BA", "CN-HK", "DO-DN", "GE-AB"]: # repeat
			#	break
			if subdivision["code"] in exist:
				break
				raise Exception(subdivision["code"])
			state = {
				"code": subdivision["code"],
				"url": subdivision["url"],
				"wiki_page_id": subdivision["wiki_page_id"],
				"language_names": convert_language_names(subdivision["language_names"]),
			}
			exist[subdivision["code"]] = None
			subdivisions.append(state)
		std_country["subdivisions"] = subdivisions
		std_countries.append(std_country)
	with open("../std_country_codes.json", 'w', encoding='utf8') as std_file:
		json.dump(std_countries, std_file, ensure_ascii=False)
