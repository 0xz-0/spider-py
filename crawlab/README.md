# 爬虫们

## CLC - 中国图书分类(Chinese Library Classification)
  
* 主站地址: [www.clcindex.com](http://www.clcindex.com)

* 获取分类条目名和上下级条目关系，存入postgres数据库

* 启动
  * ```scrapy crawl clc```或```scrapy runspider ./crawlab/spiders/clc.py```

## QHDM - 统计用区划代码和城乡划分代码

* 主站地址：[www.stats.gov.cn/sj/tjbz/qhdm/](https://www.stats.gov.cn/sj/tjbz/qhdm/)
  
  * 实际为某一具体年份数据即：[www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html](https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html)
  
* 获取省市区县街道的名称和编码，及上下层级结构

* 启动
  * ```scrapy crawl qhdm```或```scrapy runspider ./crawlab/spiders/qhdm.py```
  