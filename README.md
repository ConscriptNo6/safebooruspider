~~小孩子不懂事儿，写着玩的~~

现在看来写的真烂，挖个坑准备重构

### 2023.04.20 重构
- 使用类封进行封装，移除了所有在终端里的交互。
- 拟加入本地代理功能，预防网站哪天突然被墙。
#### 实例：
```python
spider = sbSpider(r'D:\users\Conscripter\Desktop\BA', tag = 'blue_archive', page = 1)
spider.crawl()
```
