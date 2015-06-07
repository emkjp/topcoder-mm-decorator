#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

from CoderState import *
import WebScraping

APP_ROOT = os.path.dirname( os.path.abspath( __file__ ) )

TEMPLATE_DIR = os.path.join(APP_ROOT,'template')

TEMPLATE_LOOKUP = TemplateLookup(directories=TEMPLATE_DIR,
                        output_encoding='utf-8',
                        input_encoding='utf-8',
                        default_filters=['decode.utf8'])

TEMPLATE_FILE = 'standing.tmpl'

def save_graph_html(stat, path) :
    print 'making {0} chart'.format(stat.coder_handle_name)
    html = ''
    try:
        template = TEMPLATE_LOOKUP.get_template('graph.tmpl')
        html = template.render(plot_data = stat.rating_plot , stat = stat, current_rank = stat.temp_rank)
    except Exception , e:
        print exceptions.text_error_template().render()
        raise e
    graph_path = os.path.join(path , 'graph');
    if not os.path.isdir(graph_path) :
        os.makedirs(graph_path);
    f = open(os.path.join(graph_path , stat.coder_handle_name + '.html' ) , 'wb')
    f.write(html)
    f.close()


def save_standing_html(round_id , stat_list , title, path) :

    html = ''
    try:
        template = TEMPLATE_LOOKUP.get_template(TEMPLATE_FILE)
        html = template.render(rows = stat_list ,
                                 url = WebScraping.get_active_standings_url(round_id) ,
                                 title = title, 
                                 last_updated = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    except Exception , e:
        print exceptions.text_error_template().render()
        raise e

    if not os.path.isdir(path) :
        os.makedirs(path);
    print os.path.join(path , 'index.html')
    f = open(os.path.join(path , 'index.html') , 'wb')
    f.write(html)
    f.close()
    print U'updated index.html '  + datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), '\n'
