import sys

from functions import analize_medo, file_manager
import schedule
import time
import logging


def job():
    try:
        catalogs_list = analize_medo()
        length = file_manager(catalogs_list)
        logging.info(f'Successfully: {length} packages')
    except Exception:
        e = sys.exc_info()[1]
        logging.error(f'{e.args[0]}')
        return


schedule.every(10).seconds.do(job)
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
while True:
    schedule.run_pending()
    time.sleep(1)
