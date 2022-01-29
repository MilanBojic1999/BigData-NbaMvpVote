from exp_standing_scarper import call as standing_call
from awards_voting import call as award_call
from players_stats_scraper import call as stat_call


start = 1990
end = 2000


award_call(start,end)
standing_call(start,end)
stat_call()