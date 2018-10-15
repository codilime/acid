# -*- coding: utf-8 -*-
import datetime

from jwt import encode

import requests

from .exceptions import RemoteServerError

from acid.utils import get_logger


class ZuulManager:
    def __init__(self, host, tenant, project,
                 trigger, jwt_secret, jwt_algorithm):
        self.logger = get_logger()
        self.tenant = tenant
        self.trigger = trigger
        self.project = project

        self.endpoint = \
            f"http://{host}/api/tenant/{self.tenant}/project/{self.project}/"
        token = self.generate_jwt(jwt_secret, jwt_algorithm)
        self.auth_header = {"Authorization": f"Bearer {token}"}

    def generate_jwt(self, jwt_secret, jwt_algorithm):
        tenants_field = {self.tenant: [self.project]}
        message = {
            # Time for the token to expire
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "zuul.tenants": tenants_field
        }
        token = encode(message, jwt_secret, algorithm=jwt_algorithm)
        return token.decode('utf-8')

    def post_request(self, endpoint, body):
        res = requests.post(endpoint, headers=self.auth_header, json=body)

        if res.status_code not in [200, 304]:
            self.logger.error(res.text)
            raise RemoteServerError('Request for zuul operation failed.')

    def enqueue(self, pipeline, branch):
        endpoint = self.endpoint + "enqueue"
        ref = f"refs/heads/{branch}"
        body = {
            "trigger": self.trigger,
            "pipeline": pipeline,
            "ref": ref,
            # oldrev nad newrev set to some arbitrary values temporarily.
            "oldrev": "0000000000000000000000000000000000000001",
            "newrev": "0000000000000000000000000000000000000000"
        }
        self.post_request(endpoint, body)

    def dequeue(self, pipeline, branch):
        endpoint = self.endpoint + "dequeue"
        ref = f"refs/heads/{branch}"
        body = {
            "trigger": self.trigger,
            "pipeline": pipeline,
            "ref": ref
        }
        self.post_request(endpoint, body)
