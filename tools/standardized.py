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
				"it": "Taiwan",
				"pt": "Taiwan",
				"sv": "Taiwan",
				"de": "Taiwan",
				"en": "Taiwan",
				"ja": "台湾",
				"nl": "Taiwan",
				"es": "Taiwán",
				"fr": "Taïwan",
				"ko": "타이완",
				"zh": "台湾",
				"zh-hant": "臺灣"
			}
		elif std_country["country_iso2"] == "KR":
			std_country["language_names"] = {
				"es": "Corea del Sur",
				"fr": "Corée du Sud",
				"it": "Corea del Sud",
				"ko": "대한민국",
				"pt": "Coreia do Sul",
				"de": "Südkorea",
				"en": "South Korea",
				"ja": "大韓民国",
				"nl": "Zuid-Korea",
				"zh": "韩国",
				"sv": "Sydkorea"
			}
		elif std_country["country_iso2"] == "CN":
			std_country["language_names"] = {
				"it": "Cina",
				"pt": "China",
				"ja": "中国",
				"zh": "中国",
				"fr": "Chine",
				"ko": "중국",
				"sv": "Kina",
				"de": "China",
				"en": "China",
				"nl": "China",
				"es": "China"
			}
		elif std_country["country_iso2"] == "NL":
			std_country["language_names"] = {
				"zh": "荷兰",
				"es": "Países Bajos",
				"it": "Paesi Bassi",
				"pt": "Países Baixos",
				"ja": "オランダ",
				"nl": "Nederland",
				"fr": "Pays-Bas",
				"ko": "네덜란드",
				"sv": "Nederländerna",
				"de": "Niederlande",
				"en": "Netherlands"
			}
		elif std_country["country_iso2"] == "ML":
			std_country["language_names"] = {
				"sv": "Mali",
				"zh": "马里",
				"es": "Malí",
				"ja": "マリ共和国",
				"nl": "Mali",
				"de": "Mali",
				"it": "Mali",
				"ko": "말리",
				"en": "Mali",
				"fr": "Mali",
				"pt": "Mali"
			}
		elif std_country["country_iso2"] == "CZ":
			std_country["language_names"] = {
				"zh": "捷克",
				"fr": "Tchéquie",
				"ja": "チェコ",
				"nl": "Tsjechië",
				"de": "Tschechien",
				"en": "Czechia",
				"it": "Repubblica Ceca",
				"ko": "체코",
				"pt": "Tcheca",
				"sv": "Tjeckien",
				"es": "Chequia"
			}
		subdivisions = []
		exist = {}
		if not "subdivisions" in country:
			std_countries.append(std_country)
			continue
		for subdivision in country["subdivisions"]:
			#if subdivision["code"] in ["TD-BA", "CN-HK", "DO-DN", "GE-AB"]: # repeat
			#	break
			if subdivision["code"] in ["CN-HK", "CN-TW", "CN-MO"]:
				continue
			if subdivision["code"] in exist:
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
