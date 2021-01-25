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


def retNasdaqTickers():
    """
        THIS IS A HELPER FUNCTION DON'T CALL IT!

        This goes and pull the most recent update to the nasdaq ticker
        symbol directory.
    """
    ftp = FTP('ftp.nasdaqtrader.com')
    ftp.login()
    ftp.cwd('symboldirectory')

    with open('nasdaqlistedX.txt', 'wb') as fp:
        ftp.retrbinary('RETR nasdaqlisted.txt', fp.write)

    timestamp = ftp.voidcmd(
        "MDTM /symboldirectory/nasdaqlisted.txt")[4:]
    mod_time = parser.parse(timestamp)

    ftp.quit()

    unprocessed = open('nasdaqlistedX.txt', 'r')
    unprocessed.readline()
    processed = open('nasdaqlisted.txt', 'w')

    # YYYY/mm/dd H:M:S
    dt_string = mod_time.strftime("%Y/%m/%d %H:%M:%S")
    processed.write(dt_string + '\n')

    for line in unprocessed.readlines()[:-1]:
        ticker = line.split('|')[0]
        processed.write(ticker + '\n')

    unprocessed.close()
    processed.close()
    os.remove("nasdaqlistedX.txt")


def getNasdaqTickers():
    """
        Main funcntion
        @return: {dictionary where all keys = tickers}
    """
    tickers = []
    if os.path.isfile("nasdaqlisted.txt"):
        # Read the header of the processed ticker file to get mod time of last retrieval
        processed = open('nasdaqlisted.txt', 'r')
        stored_time = processed.readline().rstrip()

        # Check ftp server for mod time
        ftp = FTP('ftp.nasdaqtrader.com')
        ftp.login()
        ftp.cwd('symboldirectory')
        timestamp = ftp.voidcmd(
            "MDTM /symboldirectory/nasdaqlisted.txt")[4:]
        ftp.quit()
        mod_time = parser.parse(timestamp)
        mod_time = mod_time.strftime("%Y/%m/%d %H:%M:%S")

        # Checks to see if the tickers are up to date
        if stored_time != mod_time:
            print("Most up to date tickers already pulled")
        else:
            print("Getting most up to date tickers")
            retNasdaqTickers()

    else:
        print("Getting most up to date tickers")
        retNasdaqTickers()

    processed = open('nasdaqlisted.txt', 'r')
    processed.readline()

    for line in processed:
        tickers.append(line.rstrip())
    processed.close()

    return listToMap(tickers)
