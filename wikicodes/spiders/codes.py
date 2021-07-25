# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import json

def format_country_wiki_filename(url, country_iso2):
    return "."+url.replace("/wiki/","/country-wiki/",1)+".html"

def format_state_wiki_filename(url, country_iso2):
    return "."+url.replace("/wiki/","/wiki/"+country_iso2+"-",1)+".html"


class CodesSpider(scrapy.Spider):
    BASE_URL = 'https://en.wikipedia.org/'
    name = 'codes'
    start_urls = [
        '{}/wiki/List_of_ISO_3166_country_codes'.format(BASE_URL)
    ]

    def parse(self, response):
        # Get all table rows
        rows = response.xpath('//*[contains(@class,"wikitable sortable")]//tr')

        for row in rows[2:]:
            try:
                country_name = row.xpath('td/a//text()').extract_first()
                alpha_3 = row\
                    .css('a[title="ISO 3166-1 alpha-3"]')\
                    .xpath('span//text()')\
                    .extract_first()
                alpha_2 = row\
                    .css('a[title="ISO 3166-1 alpha-2"]')\
                    .xpath('span//text()')\
                    .extract_first()
                subdivision_link = '{}wiki/ISO_3166-2:{}'.format(
                    self.BASE_URL,
                    alpha_2
                )
                #if alpha_2 != "AL":
                #    continue

                url = row.xpath('td/a/@href').extract_first()
                print("country url:",url)

                result = self.get_wiki_page_id_and_language_names(url, alpha_2, format_country_wiki_filename, "./country-page/")
                # Propagate data with subdivision regions and their codes
                request = scrapy.Request(
                    subdivision_link,
                    callback=self.get_subdivisions,
                    meta={
                        'country_name': country_name,
                        'alpha_2': alpha_2,
                        'alpha_3': alpha_3,
                        'url': url,
                        'wiki_page_id': result["wiki_page_id"],
                        'language_names':  result["language_names"],
                    }
                )
                yield request
            except IndexError:
                print("index error.")
                pass
            #break
    def get_wiki_page_id_and_language_names(self, url, country_iso2, format_wiki_filename, page_dir):
        #name = "."+url.replace("/wiki/","/country-wiki/")+".html"
        name = format_wiki_filename(url, country_iso2)
        data = ""
        try:
            f = open(name)
            data = f.read()
        except FileNotFoundError:
            with requests.get(self.BASE_URL+url) as state_response :
                if state_response.status_code != 200:
                    raise Exception(state_response.status_code)
                data = state_response.content.decode("utf-8")
                with open(name,'w+') as f:
                    f.write(data)
        else:
            f.close()
        rlconf = re.findall(r"RLCONF=({(?:.|\s)*?});", data)
        print(rlconf)
        result = re.findall(r"\"wgWikibaseItemId\":\"(Q\d+)\"", rlconf[0])
        print("country match result:", result)

        # get language names from wiki page
        entity = {}
        name = page_dir+result[0]+".json"
        #name = url.format_page_filename(url, result[0])
        try:
            f = open(name)
            entity = json.load(f)
        except FileNotFoundError:
            with requests.get("https://www.wikidata.org/wiki/Special:EntityData/"+result[0]+".json") as state_response:
                if state_response.status_code != 200:
                    raise Exception(state_response.status_code)
                entity = state_response.json()
                with open(name,'w+') as f:
                    json.dump(entity,f)
        else:
            f.close()
        return {
            "wiki_page_id": result[0],
            "language_names": entity["entities"][result[0]]["labels"],
        }

    def get_subdivisions(self, response):
        divisions = []
        item = {}
        try:
            rows = response.xpath('//*[contains(@class,"wikitable sortable")]//tr')

            # Start looping through all rows, but add only with both code
            # and name extracted
            for row in rows:
                # Extract code
                code = row.xpath('td/span/text()')
                if not code:
                    code = row.xpath('td/span/span/text()')
                code = code.extract_first()

                # Extract name
                name = row.xpath('td/a//text()')
                url = row.xpath('td/a/@href')
                if not name:
                    name = row.xpath('td/span/a//text()')
                    url = row.xpath('td/span/a/@href')
                name = name.extract_first()
                url = url.extract_first()

                if code and name:
                    state_item = {
                        "name": name,
                        'code': code,
                        'url': url,
                    }
                    #name = "."+url[0].replace("/wiki/","/wiki/"+response.meta.get("alpha_2")+"-",1)+".html"
                    result = self.get_wiki_page_id_and_language_names(url, response.meta.get("alpha_2"), format_state_wiki_filename, "./page/")
                    state_item["wiki_page_id"] = result["wiki_page_id"]
                    state_item["language_names"] = result["language_names"]
                    divisions.append(state_item)
                    #break
            item.update({
                'subdivisions': divisions,
                'subdivisions_url': response.url,
            })
        except IndexError:
            print('Did not find any tables for subdivisions for {}'.format(
                    response.meta.get('country_name')
                )
            )

        item.update({
            'country_name': response.meta.get('country_name'),
            'country_iso2': response.meta.get('alpha_2'),
            'country_iso3': response.meta.get('alpha_3'),
            'url': response.meta.get('url'),
            'wiki_page_id': response.meta.get('wiki_page_id'),
            'language_names': response.meta.get('language_names'),
        })
        yield item

