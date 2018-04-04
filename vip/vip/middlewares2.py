#! -*- encoding:utf-8 -*-
from vip.fetch_proxy import FetchProxy
import logging


class ProxyMiddleware(object):
    f = FetchProxy()
    f.main()
    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        proxy = self.f.fetch_proxy()
        request.meta["proxy"] = "%s" % proxy
        self.logger.info("%s" % request.meta)


