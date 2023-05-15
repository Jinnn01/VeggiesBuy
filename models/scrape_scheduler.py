import threading
import schedule
import logging

from models import c_webscraper as CS
from models import w_webscraper as WS


# coles webscraping
def c_job():
    try:
        output = CS.c_scrape()

        # delete this
        logging.log(output, output)
    except Exception as e:
        logging.exception(e)
    else:
        print(output)


# woolworths web scraping
def w_job():
    try:
        output = WS.w_scrape()

        # delete this
        logging.log(output, output)
    except Exception as e:
        logging.exception(e)
    else:
        print(output)


# scheduling jobd
def all_scheduled_job():
    #actual jobs
    schedule.every().day.at("00:05").do(c_job)
    schedule.every().day.at("00:35").do(w_job)

    # # dummy test jobs
    # schedule.every().hour.at(":08").do(c_job)
    # schedule.every().hour.at(":05").do(w_job)

    while True:
        schedule.run_pending()
        if not schedule.jobs:
            break


# Create a new thread for running the scheduled job
def scrape_thread():
    thread1 = threading.Thread(target=all_scheduled_job)
    # Start the thread
    thread1.start()

