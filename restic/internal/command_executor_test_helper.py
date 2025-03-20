import logging
import time
import random


logging.basicConfig(level=logging.DEBUG, format="%(message)s",)
logger = logging.getLogger("command_executor_testhelper")

for i in range(10):

    if i % 2 == 0:
        print(i)
    else:
        logger.error(i)
    time.sleep(random.randint(5,15)*0.001)
