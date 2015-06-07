#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

class CoderState :
    def __init__(self):
        self.rank = 0
        self.coder_handle_name = ''
        self.coder_id  = ''
        self.provisional_score = 0.0
        self.provisional_rank = 0
        self.rank_rated_only = ''
        self.language = ''
        self.current_rating = None
        self.current_volatility = None
        self.new_rating = None
        self.new_volatility = None
        self.country = ''
        self.has_profile = False
        self.is_newbie = False
        self.time_played = 0
        self.perf_as = None
        self.e_rank = None
        self.temp_rank = 0
        self.last_submission_time = ''
        self.rating_plot = []



