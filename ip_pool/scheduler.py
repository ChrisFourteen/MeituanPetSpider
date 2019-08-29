import time

from multiprocessing import Process
from api import app
from get_ip import Getter
from tester import Tester

from settings import TESTER_ENABLED,GETTER_ENABLED,API_ENABLED,TESTER_CYCLE,GETTER_CYCLE


class Scheduler():

    def scheldule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle: 间隔时间
        """
        tester = Tester()
        while True:
            print("测试程序开始测试...")
            tester.run()
            time.sleep(cycle)

    def scheldule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 间隔时间
        """
        getter = Getter()
        while True:
            print("开始抓取代理...")
            getter.run()
            time.sleep(cycle)

    def scheldule_api(self):
        app.run()

    def run(self):
        print("代理池程序开始运行...")

        if TESTER_ENABLED:
            tester_process = Process(target=self.scheldule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.scheldule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.scheldule_api)
            api_process.start()
