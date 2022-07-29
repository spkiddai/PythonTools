BladeScan Release
===========================
***
# 环境依赖
> 
* Python3
***
# 运行方式
> 
* usage: userscan.py [-h] [-u DOMAIN] [-a AUTH] [-b BASEURL] [-c CUSTOM][-p PAGE] [-f FILE] [-o OUT] [-r]
* 
* optional arguments:
* -h, --help            show this help message and exit
* 
* API:
* URL AND API SET
* 
* -u DOMAIN, --domain DOMAIN Website domain
* -a AUTH, --auth AUTH  API Blade-Auth Example:x.py -u xx -a "bearer XXXXX"
* -b BASEURL, --baseURL BASEURL API BaseURL Default:api
* -c CUSTOM, --custom CUSTOM API Custom URL Default:blade-log
* -p PAGE, --page PAGE  LogAPI Json Max Page Default:1
* 
* Batch:
* URL Batch Test
* 
* -f FILE, --file FILE  URL FileName
* -o OUT, --out OUT     Save FlieName Default:result.txt
* 
* Data:
* Save Data
* 
* -r, --read            Read API USER Date
***
# 漏洞说明
* 由于接口权限限制宽松，导致/api/blade-log/api/list接口存在两种问题。
* 1.未授权问题：无需登录即可访问 
* 例:https://xxx.com/api/blade-log/api/list
* 未登录情况下直接访问接口，获取登录账户信息
* 2.权限限制不严格问题：登录低权限用户即可访问获取管理员账户密码
* 使用低权限人事账户登录官网演示站:https://saber.bladex.vip/#/login
* 访问https://saber.bladex.vip/api/blade-log/api/list接口查看admin用户密码信息或token
