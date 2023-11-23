#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json

import requests


class RunTask:
    def __init__(self, config: dict) -> None:
        self.token = config['token']
        self.allowUser = config['allow_user']
        print("RunTask start...")

    def do_run(self, question: str, wix: str) -> str:
        if 'prod1' in question:
            if wix not in self.allowUser:
                return "该执行任务您没有执行权限哦"
            return self.runOvlerlcDeploy(1)
        if 'prod2' in question:
            if wix not in self.allowUser:
                return "该执行任务您没有执行权限哦"
            return self.runOvlerlcDeploy(2)
        return '该执行任务无法找到'

    def runOvlerlcDeploy(self, num: int) -> str:
        url = f"https://api.github.com/repos/oreoft/overlc-backend/actions/workflows/ci-prod-publish{num}.yml/dispatches"
        payload = json.dumps({
            "ref": "master"
        })
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}',
            'Content-Type': 'application/json'
        }
        requests.request("POST", url, headers=headers, data=payload)
        return "命令发送成功, 请等待部署平台结果"


if __name__ == "__main__":
    from configuration import Config

    c = Config()
    runTask = RunTask(c.GITHUB)
    rsp = runTask.do_run("prod1", "wxid_eik8l7osjspt22")
    print(rsp)
