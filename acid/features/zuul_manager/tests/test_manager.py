# -*- coding: utf-8 -*-
import pytest

from ..manager import ZuulManager
from ..exceptions import ZuulManagerConfig


@pytest.mark.unit
class TestZuulConnector():
    def test_raise_when_no_user_key_file(self, path_to_test_file):
        with pytest.raises(ZuulManagerConfig):
            ZuulManager(host="host",
                        username="user",
                        user_key_file="there/is/no/file",
                        host_key_file=path_to_test_file("host_key.pub"),
                        tenant="tenant",
                        trigger="trigger",
                        project="project",
                        policy="AutoAddPolicy",
                        gearman_conf="/path/to/file/.conf")

    def test_raise_when_no_host_keys_file(self, path_to_test_file):
        with pytest.raises(ZuulManagerConfig):
            ZuulManager(host="host",
                        username="user",
                        user_key_file=path_to_test_file("insecure_user_key"),
                        host_key_file="there/is/no/file",
                        tenant="tenant",
                        trigger="trigger",
                        project="project",
                        policy="AutoAddPolicy",
                        gearman_conf="/path/to/file/.conf")

    def test_can_set_autoadd_policy(self, path_to_test_file):
        ZuulManager(host="host",
                    username="user",
                    user_key_file=path_to_test_file("insecure_user_key"),
                    host_key_file=path_to_test_file("host_key.pub"),
                    tenant="tenant",
                    trigger="trigger",
                    project="project",
                    policy="AutoAddPolicy",
                    gearman_conf="/path/to/file/.conf")

    def test_can_set_reject_policy(self, path_to_test_file):
        ZuulManager(host="host",
                    username="user",
                    user_key_file=path_to_test_file("insecure_user_key"),
                    host_key_file=path_to_test_file("host_key.pub"),
                    tenant="tenant",
                    trigger="trigger",
                    project="project",
                    policy="RejectPolicy",
                    gearman_conf="/path/to/file/.conf")

    def test_raise_when_try_to_set_not_exists_policy(self, path_to_test_file):
        with pytest.raises(ZuulManagerConfig):
            ZuulManager(host="host",
                        username="user",
                        user_key_file=path_to_test_file("insecure_user_key"),
                        host_key_file=path_to_test_file("host_key.pub"),
                        tenant="tenant",
                        trigger="trigger",
                        project="project",
                        policy="no-policy",
                        gearman_conf="/path/to/file/.conf")

    def test_enqueue_generate_correct_command(self, path_to_test_file, mocker):
        run_command = mocker.patch.object(ZuulManager, '_run_command')
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="tenant",
                           trigger="trigger",
                           project="project",
                           policy="AutoAddPolicy",
                           gearman_conf="/path/to/file/.conf")
        zuul.enqueue(pipeline="periodic-nightly", branch="master")

        run_command.assert_called_with(
            'zuul -c /path/to/file/.conf enqueue-ref --tenant tenant --trigger '
            'trigger --pipeline periodic-nightly --project project '
            '--ref refs/heads/master > /dev/null 2>&1 &')

    def test_dequeue_generate_correct_command(self, path_to_test_file, mocker):
        run_command = mocker.patch.object(ZuulManager, '_run_command')
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="tenant",
                           trigger="trigger",
                           project="project",
                           policy="AutoAddPolicy",
                           gearman_conf="/path/to/file/.conf")
        zuul.dequeue(pipeline="periodic-nightly", branch="master")

        run_command.assert_called_with(
            'zuul -c /path/to/file/.conf dequeue --tenant tenant '
            '--pipeline periodic-nightly --project project '
            '--ref refs/heads/master > /dev/null 2>&1 &')

    def test_enqueue_correct_escape_insecure_args(self, path_to_test_file,
                                                  mocker):
        run_command = mocker.patch.object(ZuulManager, '_run_command')
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="TENANT",
                           trigger="TRIGGER",
                           project="PROJECT",
                           policy="AutoAddPolicy",
                           gearman_conf="/path/to/file/.conf")
        zuul.enqueue(pipeline="periodic`who`", branch="master???*")

        run_command.assert_called_with(
            'zuul -c /path/to/file/.conf enqueue-ref --tenant TENANT '
            '--trigger TRIGGER --pipeline \'periodic`who`\' --project PROJECT '
            '--ref \'refs/heads/master???*\' > /dev/null 2>&1 &')

    def test_dequeue_correct_escape_insecure_args(self, path_to_test_file,
                                                  mocker):
        run_command = mocker.patch.object(ZuulManager, '_run_command')
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="TENANT",
                           trigger="TRIGGER",
                           project="PROJECT",
                           policy="AutoAddPolicy",
                           gearman_conf="/path/to/file/.conf")
        zuul.dequeue(pipeline="rm -r /", branch="master*/~")

        run_command.assert_called_with(
            'zuul -c /path/to/file/.conf dequeue --tenant TENANT '
            '--pipeline \'rm -r /\' --project PROJECT '
            '--ref \'refs/heads/master*/~\' > /dev/null 2>&1 &')

    def test_enqueue_incorect_gearman_conf(self, path_to_test_file,
                                           mocker):
        run_command = mocker.patch.object(ZuulManager, '_run_command')
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="tenant",
                           trigger="trigger",
                           project="project",
                           policy="AutoAddPolicy",
                           gearman_conf="incorrect/path/to/file/.con")
        zuul.enqueue(pipeline="periodic-nightly", branch="master")

        run_command.assert_called_with(
            'zuul  enqueue-ref --tenant tenant --trigger trigger --pipeline '
            'periodic-nightly --project project --ref refs/heads/master '
            '> /dev/null 2>&1 &')

    def test_dequeue_incorect_gearman_conf(self, path_to_test_file,
                                           mocker):
        run_command = mocker.patch.object(ZuulManager, '_run_command')
        zuul = ZuulManager(host="host",
                           username="user",
                           user_key_file=path_to_test_file("insecure_user_key"),
                           host_key_file=path_to_test_file("host_key.pub"),
                           tenant="tenant",
                           trigger="trigger",
                           project="project",
                           policy="AutoAddPolicy",
                           gearman_conf="incorrect/path/to/file/.con")
        zuul.dequeue(pipeline="periodic-nightly", branch="master")

        run_command.assert_called_with(
            'zuul  dequeue --tenant tenant --pipeline periodic-nightly '
            '--project project --ref refs/heads/master > /dev/null 2>&1 &')
