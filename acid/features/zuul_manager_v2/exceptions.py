# -*- coding: utf-8 -*-
class RemoteServerError(Exception):
    pass


class ZuulManagerError(Exception):
    pass


class ZuulManagerConn(ZuulManagerError):
    pass


class ZuulManagerConfig(ZuulManagerError):
    pass
