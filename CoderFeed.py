#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import urllib2
import re
import datetime
import time
import math

from lxml import etree

CODER_LIST_FILENAME = 'coder_list.xml'

def download_coder_list_datafeed_and_save():
    opener = urllib2.build_opener()
    url = 'http://www.topcoder.com/tc?module=BasicData&c=dd_coder_list'
    print 'downloading latest coder feed from ' + url;
    datafeed = opener.open(url).read()
    f = open(CODER_LIST_FILENAME , 'w')
    f.write(datafeed)
    f.close()

def coder_list_file_is_exists():
    return os.path.isfile(CODER_LIST_FILENAME)

def get_coder_hash() :
    if not coder_list_file_is_exists():
        download_coder_list_datafeed_and_save()

    tree = etree.parse(CODER_LIST_FILENAME, etree.XMLParser(ns_clean=True))
    coder_hash = {}
    for t in tree.xpath('//dd_coder_list/row') :
        coder_hash[t.find('coder_id').text] = t
    return coder_hash
