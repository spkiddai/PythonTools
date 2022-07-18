import os,re,sys,yaml,queue,argparse,joblib,threading,subprocess
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer

#PHP执行路径  需配置PHP+VLD扩展 用于生成PHP文件的Opcode
PHP_BIN = "php"
Text_Feature = 'feature.pkl'
RF_Model = 'RFModel.pkl'

#结果集
code_list = {}

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d webshell")
    parser.add_argument("-d", "--dir", help="Directory Name")
    parser.add_argument("-f", "--file", help="FileName")
    parser.add_argument("-p", "--thread", default=10 , type=int ,help="Thread")
    return parser.parse_args()

def get_opcde(queue):
    php_bin = PHP_BIN
    while not queue.empty():
        file = queue.get()
        code = []
        cmd = php_bin + " -dvld.active=1 -dvld.execute=0 " + file
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8")
            for line in p.stdout.readlines()[8:-3]:
                match = re.search(r'([A-Z_]{2,})\s+', line)
                if match:
                    code.append(match.group(1))
            code_list.update({file:' '.join(code)})
        except:
            pass
        p.terminate()

def thread_run(t,queue):
    threads = []
    for t in range(t):
        thread = threading.Thread(target=get_opcde,args=(queue,))
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()

def phpscan(dict):
    CVfeatures = joblib.load(Text_Feature)
    CV = CountVectorizer(ngram_range=(2, 4), decode_error="ignore", token_pattern=r'\b\w+\b', min_df=0.15, max_df=0.85,
                         vocabulary=CVfeatures)
    rfc = joblib.load(RF_Model)
    for key,value in dict.items():
        list = [value]
        x=CV.transform(list).toarray()
        result = rfc.predict(x).tolist()
        if 1 in result:
            print(key)

if __name__ == "__main__":
    args = parse_args()
    list = []
    if args.file != None:
        scan_path = Path(args.file)
        if os.path.exists(args.file):
            if args.file.endswith(".php") or args.file.endswith(".php3"):
                list.append(scan_path)
    elif args.dir != None:
        scan_path = Path(args.dir)
        if scan_path.exists():
            list = sorted(scan_path.rglob('*.php')) + sorted(scan_path.rglob('*.php3'))
    if len(list) > 0:
        q = queue.Queue()
        for i in list:
            q.put(str(i))
        thread_run(args.thread,q)
        phpscan(code_list)