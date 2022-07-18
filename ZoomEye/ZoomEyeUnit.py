#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,yaml
import logging
import requests

class ZoomEyeUnit():

    def __init__(self):
        self.config = self._config()
        self.headers = self._create_header()

    def _config(self):
        if os.path.exists('config.yml'):
            with open('config.yml', 'r', encoding='utf-8') as rad_yaml:
                config = yaml.load(rad_yaml, Loader=yaml.FullLoader)
                return config

    def _create_header(self):
        if self.config['Auth']['APIkey'] != None:
            header = {"API-KEY": self.config['Auth']['APIkey']}
            return header
        elif self.config['Auth']['user'] != None and self.config['Auth']['pass'] != None:
            if self._login != None:
                header = self._login()
            return header
        else:
            logging.log(logging.ERROR, "[-][Config Error]:Not Found API-Key or username,password.")
            exit(0)

    def _login(self):
        url = self.config['API']['login']
        data = {"username": self.config['Auth']['user'], "password": self.config['Auth']['pass']}
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                header = {"Authorization": "JWT %s" % (response["access_token"])}
                return header
            else:
                logging.log(logging.ERROR, "[-][Statu Error]:URL:{} Status:{}".format(url, str(response.status_code)))
                return
        except Exception as e:
            logging.log("[-][Requests Error]:URL:{} Error:{}".format(url, e))
            return

    # 用户信息接口：无需参数传入
    def info(self):
        url = self.config['API']['info']
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.log(logging.ERROR, "[-][Statu Error]:URL:{} Status:{}".format(url, str(response.status_code)))
                return
        except Exception as e:
            logging.log("[-][Requests Error]:URL:{} Error:{}".format(url, e))
            return

    #查询：type类型对应查询接口  host和web
    def search(self,type,query,page=1,facets=1):
        params = {"query": query, "page": page, "facets": facets}
        url = self.config['API'][type]
        try:
            response = requests.get(url, headers=self.headers,params=params)
            if response.status_code == 200:
                return response.json()
            else:
                logging.log(logging.ERROR, "[-][Statu Error]:URL:{} Status:{}".format(url, str(response.status_code)))
                return
        except Exception as e:
            logging.log("[-][Requests Error]:URL:{} Error:{}".format(url, e))
            return
