# 新浪

## 微博

* 主站地址: [weibo.com](https://weibo.com/)
  
### 榜单

* 热搜榜：[hotSearch](https://weibo.com/ajax/side/hotSearch)
  
  * 启动：`scrapy crawl RankHotSearch`
  
* 文娱榜：[entertainment](https://weibo.com/ajax/statuses/entertainment)

  * 启动：`scrapy crawl RankEntertainment`
  
* 新闻榜：[news](https://weibo.com/ajax/statuses/news)

  * 启动：`scrapy crawl RankNews`

* *其中，文娱榜、新闻榜，有用到selenium的chrome driver*

### 榜单V1

* 主地址：[m.weibo.cn/api](https://m.weibo.cn/api/container/getIndex)
  
* 热搜榜：[https://m.weibo.cn/api/container/getIndex?containerid=106003type=25&extparam=seat=1%26region_relas_conf=0%26cate=10103%26dgr=0%26filter_type=realtimehot%26lcate=1001]
  * 注：extparam参数为`seat=1&region_relas_conf=0&cate=10103&dgr=0&filter_type=realtimehot&lcate=1001`，实际请求时不要转义！
  * 启动：`scrapy crawl RankV1HotSearch`
