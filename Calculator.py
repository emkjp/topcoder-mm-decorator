#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math

from mpmath import erf,erfinv,mp

mp.dps = 15

cdfinv_cached_hash = {}

# inverse of cumulative distribution function of a normal distribution
def cdfinv( p ) :
    return math.sqrt(2) * erfinv(min(max(-1 , 2 * p - 1), +1))

def cdfinv_cached( p ) :
    if cdfinv_cached_hash.get(p) is None :
        cdfinv_cached_hash[p] = cdfinv(p)
    return cdfinv_cached_hash[p] 

def square(p) : 
    return p * p

def calculate_new_rating(stat_list) :
    # calculate rated member's ratings
    calculate_new_rating_sub(stat_list , rated_only = True)
    for stat in stat_list :
        if stat.current_rating is None :
            stat.current_rating = 1200
            stat.current_volatility = 515
    # calculate new member's ratings
    calculate_new_rating_sub(stat_list , rated_only = False)

def calculate_temp_rank(stat_list, rated_only) :
    last_score = None
    last_rank = None
    rank_histogram = {}
    index = 0
    for stat in stat_list :
        index = index + 1
        if last_score == stat.provisional_score :
            stat.temp_rank = last_rank
        else :
            stat.temp_rank = index
        last_score = stat.provisional_score
        last_rank = stat.temp_rank
        if rated_only :
            stat.rank_rated_only = stat.temp_rank
        if rank_histogram.get(stat.temp_rank) is None :
            rank_histogram[stat.temp_rank] = 1
        else :
            rank_histogram[stat.temp_rank] = rank_histogram[stat.temp_rank] + 1

    for stat in stat_list :
        stat.temp_rank = (stat.temp_rank * 2 + rank_histogram[stat.temp_rank] - 1) / 2.0

def calculate_new_rating_sub(stat_list, rated_only) :
    if rated_only :
        stat_list = filter(lambda x : x.current_rating is not None , stat_list)
    num_coders = len(stat_list)
    
    calculate_temp_rank(stat_list, rated_only)
    
    def calcuate_cf(stat_list) :
        sum_rating = sum(map(lambda stat: int(stat.current_rating), stat_list))
        avg_rating = float(sum_rating) / float(num_coders)
        cf1 = 0
        cf2 = 0
        for stat in stat_list :
            cf1 += square(stat.current_volatility)
            cf2 += square(stat.current_rating - avg_rating)
        return math.sqrt(cf1 / float(num_coders) + cf2 / float(num_coders - 1.0))

    def calculate_cap(stat) :
        return 150 + 1500 / (stat.time_played + 2.0);
    
    def calculate_weight(stat) :
        weight = 1.0 / (1 - (0.42 / (stat.time_played + 1) + 0.18)) - 1.0
        if 2000 <= stat.current_rating and stat.current_rating <= 2500 :
            weight *= 0.9
        elif 2500 < stat.current_rating :
            weight *= 0.8
        return weight;
        
    def calculate_erank(stat_list, target) :
        e_rank = 0.5
        for stat in stat_list :
            wp = 0.5 * (
                erf(
                    (stat.current_rating - target.current_rating) /
                    math.sqrt(
                        2 * (square(target.current_volatility) + square(stat.current_volatility))
                    )
                ) + 1.0
            )
            e_rank = e_rank + wp
        return e_rank;

    cf = calcuate_cf(stat_list)
    
    for stat in stat_list :
        if stat.new_rating is not None :
            continue # already calculated

        weight = calculate_weight(stat);
        cap = calculate_cap(stat);

        e_rank = calculate_erank(stat_list, stat);
        e_perf = -cdfinv_cached( (e_rank - 0.5) / num_coders)
        
        def calculate_new_rating_and_volatility(rank) :
            a_perf = -cdfinv_cached( (rank - 0.5) / num_coders)
            perf_as = stat.current_rating + cf * (a_perf - e_perf)
            new_rating = (stat.current_rating + weight * perf_as) / (1.0 + weight)
            new_volatility = math.sqrt(
                square(new_rating - stat.current_rating) / weight +
                square(stat.current_volatility) / (weight + 1.0)
            )
            if new_rating < stat.current_rating - cap :
                new_rating = stat.current_rating - cap
            if new_rating > stat.current_rating + cap :
                new_rating = stat.current_rating + cap
            return (int(round(new_rating)), int(round(new_volatility)), int(perf_as), round(e_rank,2));
            
        (stat.new_rating, stat.new_volatility, stat.perf_as, stat.e_rank) = calculate_new_rating_and_volatility(stat.temp_rank);
        
        if stat.is_newbie :
            # http://apps.topcoder.com/forums/?module=Thread&threadID=507858&mc=17&view=threaded
            stat.new_volatility = 385

        stat.rating_plot = map((lambda r: calculate_new_rating_and_volatility(r)[0]), range(1, len(stat_list) + 1));
