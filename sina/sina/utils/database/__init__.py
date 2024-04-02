from . import rank_models

# 定时任务
DBRequestTask = rank_models.RequestTask

# 榜单们
DBRankHotSearchRealTimeItems = rank_models.HotSearchRealTimeItems
DBRankHotSearchHotGovItems = rank_models.HotSearchHotGovItems
DBRankEntertainmentItems = rank_models.EntertainmentItems
DBRankNewsItems = rank_models.RankNewsItems
