#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib2
import re

from StringIO import StringIO
from lxml import etree
from CoderState import *

def safe_int(x) :
    if x is None :
        return None
    return int(x)

def get_active_standings_url(round_id, page_idx = 0) :
    return 'http://www.topcoder.com/longcontest/?&module=ViewStandings&rd={0}&sr={1}&nr={2}'.format(round_id , page_idx * 100 + 1 , 100)

def download_active_contest_standing(round_id, page_idx):
    url = get_active_standings_url(round_id , page_idx)
    print 'loading ' + url
    opener = urllib2.build_opener()
    html = opener.open(url).read()
    return html    

def get_active_contest_standing(coder_hash , round_id) :
    stat_list = []
    page_idx = 0
    memo_coder_id = {}
    last_rank = None
    pattern = re.compile('cr=([0-9]+)')
    while True :
        html = download_active_contest_standing(round_id, page_idx)
        tree = etree.parse(StringIO(html), etree.HTMLParser())

        index = 0

        for t in tree.xpath("//table[@class='statTable']/tr")[2:] :
            index = index + 1
            stat = CoderState()
            stat.coder_handle_name = t[0][0].text.strip()
            stat.coder_id = pattern.search(t[0][0].get('href')).group(1)
            if memo_coder_id.get(stat.coder_id) is not None :
                return None
            memo_coder_id [stat.coder_id] = True
            if t[2].text.strip() == '' :
                stat.provisional_score = 0.00
                stat.provisional_rank = last_rank
            else :
                stat.provisional_score = float(t[1].text.strip())
                stat.provisional_rank = safe_int(t[2].text.strip())
                stat.last_submission_time = t[3].text.strip()
            stat.language = t[4].text.strip()
            last_rank = stat.provisional_rank
            coder_info = coder_hash.get(stat.coder_id)
            if coder_info is not None :
                stat.current_rating = safe_int(coder_info.find('mar_rating').text)
                stat.current_volatility = safe_int(coder_info.find('mar_vol').text)
                stat.time_played = safe_int(coder_info.find('mar_num_ratings').text)
                stat.country = coder_info.find('country_name').text
                stat.is_newbie = False
                if stat.current_rating is None :
                    stat.is_newbie = True
                if stat.time_played is None :
                    stat.time_played = 0
            else :
                stat.is_newbie = True
            stat_list.append(stat)
        if index < 100 :
            break
        page_idx = page_idx + 1
    return stat_list
