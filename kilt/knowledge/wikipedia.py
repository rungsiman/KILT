# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import requests
import urllib.request
from bs4 import BeautifulSoup
import urllib.parse as urlparse
from urllib.parse import parse_qs

from kilt.knowledge.base import KnowledgeBase


def _get_pageid_from_api(title, client=None):
    pageid = None

    title_html = title.strip().replace(" ", "%20")
    url = (
        "https://en.wikipedia.org/w/api.php?action=query&titles={}&format=json".format(
            title_html
        )
    )

    try:
        # Package the request, send the request and catch the response: r
        r = requests.get(url)

        # Decode the JSON data into a dictionary: json_data
        json_data = r.json()

        if len(json_data["query"]["pages"]) > 1:
            print("WARNING: more than one result returned from wikipedia api")

        for _, v in json_data["query"]["pages"].items():
            pageid = v["pageid"]

    except Exception as e:
        #  print("Exception: {}".format(e))
        pass

    return pageid


def _read_url(url):
    with urllib.request.urlopen(url) as response:
        html = response.read()
        soup = BeautifulSoup(html, features="html.parser")
        title = soup.title.string.replace(" - Wikipedia", "").strip()
    return title


def _get_title_from_wikipedia_url(url, client=None):
    title = None
    try:
        title = _read_url(url)
    except Exception:
        try:
            # try adding https
            title = _read_url("https://" + url)
        except Exception:
            #  print("Exception: {}".format(e))
            pass
    return title


class Wikipedia(KnowledgeBase):
    page_id_attr = 'wikipedia_id'
    page_title_attr = 'wikipedia_title'
    page_description_attr = 'text'

    def __init__(
        self,
        mongo_connection_string=None,
        database="kilt",
        collection="wikipedia",
    ):
        super().__init__(mongo_connection_string, database, collection)

    def get_page_from_url(self, url):
        page = None

        # 1. try to look for title in the url
        parsed = urlparse.urlparse(url)
        record = parse_qs(parsed.query)
        if "title" in record:
            title = record["title"][0].replace("_", " ")
            page = self.get_page_by_title(title)

        # 2. try another way to look for title in the url
        if page == None:
            title = url.split("/")[-1].replace("_", " ")
            page = self.get_page_by_title(title)

        # 3. try to retrieve the current wikipedia_id from the url
        if page == None:
            title = _get_title_from_wikipedia_url(url, client=self.client)
            if title:
                pageid = _get_pageid_from_api(title, client=self.client)
                if pageid:
                    page = self.get_page_by_id(pageid)

        return page
