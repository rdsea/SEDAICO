#!/usr/bin/env python

import yaml
from multiprocessing import Process
import os
from extraNode import sensor_simulator
import time 
import sys


def info(title):
    print(title)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


if __name__ == '__main__':

    with open("config.yml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    print(data)

    info('main line')
    for i in range(0, int(data['deployment']['number'])):
        p = Process(target=sensor_simulator, name=i, args=(data['broker']['topic'], data['broker']['address'], data['broker']['port'], data['deployment']['rate']))
        p.start()
    p.join()
    time.sleep(int(data['deployment']['duration']))
    sys.exit()
