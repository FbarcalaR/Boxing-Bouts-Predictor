import logging
import random
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

class ProxiesGenerator:

    def __init__(self):
        req_proxy = RequestProxy(log_level=logging.ERROR)
        self.proxiesPool = req_proxy.get_proxy_list()
    
    def getRandomProxy(self):
        proxy = random.choice(self.proxiesPool)
        return {
            'http': 'http://' + proxy.ip + ':' + proxy.port,
            'https': 'http://' + proxy.ip + ':' + proxy.port,
        }