ZoomEyeTools Release
===========================
***
# 环境依赖
> 
* Python3
* yaml
* requests
***
# 运行方式
> 
* import ZoomEyeUnit
* ze = ZoomEyeUnit.ZoomEyeUnit()
* print(ze.info())
***
# 配置文件介绍
>
* API:
  - login: https://api.zoomeye.org/user/login        #登录页面
  - info: https://api.zoomeye.org/resources-info     #用户信息页面
  - host: https://api.zoomeye.org/host/search        #主机搜素
  - web: https://api.zoomeye.org/web/search          #Web搜素
* Auth:  #APIKEY和用户密码均可查询
  - APIkey:                                          #APIKEY
  - user:                                            #用户名
  - pass:                                            #密码
***