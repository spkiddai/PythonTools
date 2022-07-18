BladeScan Release
===========================
***
# 环境依赖
> 
* Python3
***
# 运行方式
> 
* usage: BladeScan.py [-h] [-u DOMAIN] [-a AUTH] [-b BASEURL] [-c CUSTOM][-p PAGE] [-f FILE] [-o OUT] [-r]
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
*   -r, --read            Read API USER Date