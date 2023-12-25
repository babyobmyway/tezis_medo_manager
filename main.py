from functions import analize_medo, file_manager
import schedule
import time

def job():
    catalogs_list = analize_medo()
    file_manager(catalogs_list)

schedule.every(2).minutes.do(job)

# нужно иметь свой цикл для запуска планировщика с периодом в 1 секунду:
while True:
    schedule.run_pending()
    time.sleep(1)