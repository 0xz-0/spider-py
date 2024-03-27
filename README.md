# spider-py

base from scrapy. To crawl sth simply

## Getting started

### Create a new project

1. 安装 python 环境，安装 scrapy 包
   ```pip install scrapy -i https://pypi.tuna.tsinghua.edu.cn/simple--trusted-host pypi.tuna.tsinghua.edu.cn```

2. 根据默认模版创建一个项目
   ```scrapy startproject {{project_name}}```

3. 进行爬虫开发

## scrapy project

### crawlab

* 通用爬虫，一般为一次性/手动触发的非周期任务
  
* 包含以下爬虫，详见[crawlab.README](./crawlab/README.md)

| 爬虫名 | 内容名   | 来源                                        | 说明 |
| :----: | :------: | :-----------------------------------------: | :--- |
| clc    | 中图分类 | [www.clcindex.com](http://www.clcindex.com) |      |
  
* 启动爬虫
  ```cd crawlab && scrapy crawl {{spider_name}}```
  