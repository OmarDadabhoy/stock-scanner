import os.path
import os
from dateutil import parser
from datetime import datetime
from ftplib import FTP


def listToMap(stockslist):
    allStocks = {}
    for i in stockslist:
        allStocks.update({i: 1})
    return allStocks


def retTickers(file_name):
    """
        THIS IS A HELPER FUNCTION DON'T CALL IT!

        This goes and pull the most recent update to the nasdaq ticker
        symbol directory. ftp://ftp.nasdaqtrader.com/symboldirectory/
    """
    ftp = FTP('ftp.nasdaqtrader.com')
    ftp.login()
    ftp.cwd('symboldirectory')

    with open(f'{file_name}X.txt', 'wb') as fp:
        ftp.retrbinary(f'RETR {file_name}.txt', fp.write)

    timestamp = ftp.voidcmd(
        f"MDTM /symboldirectory/{file_name}.txt")[4:]
    mod_time = parser.parse(timestamp)

    ftp.quit()

    unprocessed = open(f'{file_name}X.txt', 'r')
    unprocessed.readline()
    processed = open(f'{file_name}.txt', 'w')

    # YYYY/mm/dd H:M:S
    dt_string = mod_time.strftime("%Y/%m/%d %H:%M:%S")
    processed.write(dt_string + '\n')

    for line in unprocessed.readlines()[:-1]:
        ticker = line.split('|')[0]
        processed.write(ticker + '\n')

    unprocessed.close()
    processed.close()
    os.remove(f"{file_name}X.txt")


def checkFileExists(file_name):
    if os.path.isfile(file_name):
        # Read the header of the processed ticker file to get mod time of last retrieval
        processed = open(f"{file_name}.txt", 'r')
        stored_time = processed.readline().rstrip()

        # Check ftp server for mod time
        ftp = FTP('ftp.nasdaqtrader.com')
        ftp.login()
        ftp.cwd('symboldirectory')
        timestamp = ftp.voidcmd(
            f"MDTM /symboldirectory/{file_name}.txt")[4:]
        ftp.quit()
        mod_time = parser.parse(timestamp)
        mod_time = mod_time.strftime("%Y/%m/%d %H:%M:%S")

        # Checks to see if the tickers are up to date
        if stored_time != mod_time:
            print(f"Most up to date {file_name} already pulled")
        else:
            print(f"Getting most up to date {file_name}")
            retTickers(file_name)
    else:
        print(f"Getting most up to date {file_name}")
        retTickers(file_name)


def getNasdaqTickers():
    """
        Main funcntion
        @return: {dictionary where all keys = tickers}
    """
    tickers = []
    files = ["nasdaqlisted", "otherlisted"]

    for file_name in files:
        checkFileExists(file_name)
        processed = open(f"{file_name}.txt", 'r')
        processed.readline()
        for line in processed:
            tickers.append(line.rstrip())
        processed.close()

    return listToMap(tickers)
