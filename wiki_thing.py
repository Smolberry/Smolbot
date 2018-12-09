#!/usr/bin/python3
import re
from urllib.request import urlopen
from urllib.request import unquote
import requests
def search(terms="Dumbass"):
        baseurl = "http://en.wikipedia.org/w/api.php?action=opensearch&search="
        endurl = "&namespace=0&format=xml"
        newterms = terms.replace(" ", "+")
        url = baseurl + newterms + endurl
        search = "<Description.*?>(.*?)</D"
        termurl_end = "&namespace=0&format=json"
        termurl = baseurl + newterms + termurl_end
        page = urlopen(url)
        contents = page.read()
        search_descript = re.search(search, contents.decode())
        terms_page = requests.get(termurl)
        terms_json = terms_page.json()
        try:
                description = search_descript.group(1)
        except:
                try:
                      description = "%s: " % (terms_json[0])
                      for item in terms_json[1]:
                              description += item + " "
                except:
                        description = "None"
        return terms+": "+description
