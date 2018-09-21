# -*- coding: utf-8 -*-
import shlex

import paramiko

from .exceptions import ZuulManagerConfig, ZuulManagerConn

from flask import current_app


class ZuulManager:
    def __init__(self, host, username, user_key_file, host_key_file,
                 tenant, trigger, project, policy):
        self.host = host
        self.username = username
        self.host_pub_key = host_key_file
        self.policy = policy

        self.tenant = tenant
        self.trigger = trigger
        self.project = project

        try:
            self.user_key = paramiko.RSAKey.from_private_key_file(user_key_file)
            self._client = self._prepare_client()
        except FileNotFoundError as exc:
            raise ZuulManagerConfig() from exc

    def enqueue(self, pipeline, branch):
        pipeline, ref = self._sanitize_args(pipeline, branch)

        c = self._gearman_conf_arg()

        command = str(f"zuul{c} enqueue-ref --tenant {self.tenant} "
                      f"--trigger {self.trigger} --pipeline {pipeline} "
                      f"--project {self.project} --ref {ref} "
                      "> /dev/null 2>&1 &")
        self._run_command(command)

    def dequeue(self, pipeline, branch):
        pipeline, ref = self._sanitize_args(pipeline, branch)

        c = self._gearman_conf_arg()

        command = str(f"zuul{c} dequeue --tenant {self.tenant} "
                      f"--pipeline {pipeline} --project {self.project} "
                      f"--ref {ref} > /dev/null 2>&1 &")
        self._run_command(command)

    def _sanitize_args(self, pipeline, branch):
        sanitized_pipeline = shlex.quote(pipeline)
        sanitized_ref = shlex.quote(f'refs/heads/{branch}')
        return sanitized_pipeline, sanitized_ref

    def _gearman_conf_arg(self, conf_path=None):
        if conf_path is None:
            config = current_app.config
            conf_path = config['zuul'].get('gearman_conf', None)

        c = ""
        # check if path isn't empty
        if conf_path and len(str(conf_path)) > 0:
            # simple path validation
            # format: /path/to/file.conf
            if conf_path[0] == '/' and conf_path.endswith('.conf'):
                c = f" -c {conf_path}"
            else:
                print(f" * Invalid path to gearman configuration file!\n"
                      f" * Path should be in format: /path/to/file.conf\n"
                      f" * Given path: {conf_path}")
        return c

    def _prepare_client(self):
        client = paramiko.SSHClient()
        client.load_host_keys(self.host_pub_key)

        try:
            policy = getattr(paramiko, self.policy)
        except AttributeError as exc:
            raise ZuulManagerConfig() from exc

        client.set_missing_host_key_policy(policy)
        return client

    def _run_command(self, command):
        try:
            self._client.connect(hostname=self.host, username=self.username,
                                 pkey=self.user_key)
            self._client.exec_command(command)  # noqa S601
        except paramiko.ssh_exception.SSHException as exc:
            raise ZuulManagerConn() from exc
        finally:
            self._client.close()
