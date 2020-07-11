# 爬取淘宝商品信息至MongoDB数据库
## 说明
现在的淘宝搜索商品时需要登录账号和验证，这里都做了，建议你使用Chrom浏览器，并为Chrome浏览器配置驱动，您自己的淘宝账号和密码在config配置文件里面的账号是username选项，密码是password选项，同时你想要的爬取什么商品也是在congfig里面去修改KEYWORD里面去修改的，因为是将信息保存至数据库，所以需要安装MongoDB数据库，如果你想保存到其他的MongoDB数据库，
## 需要的库
``` python
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pyquery import PyQuery as  pq
from config import *
import pymongo
```
### Chrome版本
推荐使用这个也就是先在config.py里面把信息填好，直接运行：
``` python
python chrome.py
```
即可。这个验证码都是设置好的
### phantomJS版本
这个版本需要注意的是在selenium低版本还是支持的，但是在现在的一些新版本已经不支持了，如果要用就需要调用无头Chrome，很麻烦，这个问题就在于其验证码的问题，不过我写了循环多写跑几遍应该是可以的，我本地测试是可以的
``` python
python phantomJS.py
```


