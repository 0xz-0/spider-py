# 爬虫们

## 爬虫目录

### clc - 中国图书分类(Chinese Library Classification)
  
* 主站地址: [www.clcindex.com](http://www.clcindex.com)

* 获取分类条目名和上下级条目关系，存入postgres数据库

* 启动
  * ```scrapy crawl clc```或```scrapy runspider ./crawlab/spiders/clc.py```

### QHDM - 统计用区划代码和城乡划分代码

* 主站地址：[www.stats.gov.cn/sj/tjbz/qhdm/](https://www.stats.gov.cn/sj/tjbz/qhdm/)
  
  * 实际为某一具体年份数据即：[www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html](https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html)
  
* 获取省市区县街道的名称和编码，及上下层级结构

* 启动
  * ```scrapy crawl qhdm```或```scrapy runspider ./crawlab/spiders/qhdm.py```
  
### intel_cpu_rank - 英特尔处理器性能排名

* 主站地址：[CPU-Compare](https://cpu-compare.com/zh-CN)
  * 榜单地址：[英特尔处理器性能排名](https://cpu-compare.com/zh-CN/benchmark/intel?page=1)
  
* 启动
  * 当前目录下：```scrapy crawl intel_cpu_rank```

## 开发SOP

* 临时爬虫的开发流程
  
1. 创建一个爬虫在spiders文件夹中，包含数据的获取和转换
   * 基于模版创建：````scrapy genspider {{spider_name}} {{domain}}```
   * 可能会用到中间件

2. 创建数据对象在[items.py](./crawlab/items.py)中
   * 定义爬虫结果的数据格式

3. 创建数据对象序列化在[pipelines.py](./crawlab/pipelines.py)中
   * 定义爬虫结果的存储形式
  
4. 执行爬虫命令
   * 本地执行：```scrapy crawl {{spider_name}}```
