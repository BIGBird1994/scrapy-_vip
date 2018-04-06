# encoding=utf-8
from redis import Redis
from time import sleep
import requests



class FetchProxy(object):

    def __init__(self):
        self.r = Redis(host='localhost')

    def get_proxy(self):
        print("获取proxy")
        url = 'http://webapi.http.zhimacangku.com/?num=20&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        try:
            resp = requests.get(url)
            proxy = resp.text
            proxy_list = proxy.split('\r\n')[:-1]
            print(proxy_list)
            if not proxy_list == []:
               return proxy_list
            else:
                sleep(20)
                self.get_proxy()
        except Exception as e:
            print(e)


    def test_proxy(self,proxy_list):
        for p in proxy_list:
            try:
                print("测试proxy")
                url = 'https://www.baidu.com'
                proxie = {
                    'https': 'https://{}'.format(p)
                }
                header = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
                }
                resp = requests.get(url, proxies=proxie, headers=header, timeout=2)
                print(resp.status_code)
                if resp.status_code == 200:
                   proxy = "https://{}".format(p)
                   self.r.lpush("xt_proxy",proxy)
                   print('save to redis!!!')
            except Exception:
                continue

    def count_proxy(self):
        return self.r.llen("xt_proxy")

    def fetch_proxy(self):
        proxy = self.r.lpop("xt_proxy")
        count = self.r.llen("xt_proxy")
        if proxy and count >= 30:
           return proxy.decode(encoding="utf-8")
        else:
            print('need to fetch proxy!!')
            while True:
                proxy_list = self.get_proxy()
                self.test_proxy(proxy_list)
                if self.count_proxy() >= 30:
                    print("enough proxy %s" % self.count_proxy())
                    break

    def save_proxy(self,proxy):
        self.r.rpush("xt_proxy",proxy)

    def drop_proxy(self,proxy):
        self.r.lrem("xt_proxy",proxy,-1)

    def delete_keys(self):
        self.r.delete("xt_proxy")

    def main(self):
        f = FetchProxy()
        while f.count_proxy() == None or f.count_proxy() <= 30:
                proxy_list = f.get_proxy()
                f.test_proxy(proxy_list)
                print("already fetch %s" % f.count_proxy())
        print(f.count_proxy())



