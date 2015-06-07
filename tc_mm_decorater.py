#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import time

from argparse import ArgumentParser

from CoderState import *
import Calculator
import WebScraping
import CoderFeed
import Html

def main():
    parser = ArgumentParser()
    parser.add_argument("-u", "--update_coder_data" , action="store_true" , dest="update_coder_data",
                      help="update coders information and exit")
    parser.add_argument("-t", "--refresh_time" , action="store" , default=30*60 , dest="refresh_time",
                      help="reflesh time (sec)")
    parser.add_argument("-r", "--round_id" , action="store" , dest="round_id",
                      help="round_id")
    parser.add_argument("-T", "--title" , action="store" , dest="title",
                      help="title")
    parser.add_argument("-d", "--directory" , action="store" , dest="dir",
                      help="dir")    
    options = parser.parse_args()
        
    if options.update_coder_data :
        CoderFeed.download_coder_list_datafeed_and_save()
        exit(0)
    
    if options.round_id is None :
        parser.print_help()
        exit(0)
    
    if options.dir is not None : 
        save_path = options.dir 
    else :
        save_path = "./" + options.round_id
        
    coder_hash = CoderFeed.get_coder_hash()
    while True :
        stat_list = WebScraping.get_active_contest_standing(coder_hash, options.round_id)
        Calculator.calculate_new_rating(stat_list)
        for stat in stat_list :
            Html.save_graph_html(stat, save_path)
        Html.save_standing_html(options.round_id , stat_list, options.title, save_path)
        time.sleep(options.refresh_time)

if __name__ == "__main__":
    main()
