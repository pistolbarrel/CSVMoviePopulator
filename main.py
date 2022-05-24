# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import os

import requests
import json


def prepareTitle(title):
    title = title.replace(" (FC)", "")
    if title.find(" (1") != -1:
        title = title[:title.find(" (1")]
    if title.find(" (2") != -1:
        title = title[:title.find(" (2")]
    return title


def prepareDescription(description):
    description = description.replace("<LF>", os.linesep)
    return description


def prepareYear(year):
    if year == "0":
        return ""
    return year


def extractYearFromTitle(year):
    fnd = year.find(" (1")
    if fnd != -1:
        return year[fnd + 2: fnd + 6]
    fnd = year.find(" (2")
    if fnd != -1:
        return year[fnd + 2: fnd + 6]


def populateMovieDB():
    put_uri = "http://localhost:8080/rest/movie"
    # put_uri = "http://localhost:8080/rest/viewdate"

    with open('FromMediaMonkey.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if row[0].find("(FC)") != -1:
                    # continue
                    year = extractYearFromTitle(row[0])
                    movie_dto = {"title": prepareTitle(row[0]),
                                 "year": year,
                                 "description": "",
                                 "directors": "",
                                 "collections": row[4],
                                 "duration": "",
                                 "actors": ""}
                else:
                    # movie_dto = {"title": prepareTitle(row[0]),
                    #              "year": prepareYear(row[1]),
                    #              "description": "",
                    #              "directors": "",
                    #              "collections": "",
                    #              "duration": "",
                    #              "actors":"",
                    #              "viewDate": "1964-12-15"}
                    movie_dto = {"title": prepareTitle(row[0]),
                                 "year": prepareYear(row[1]),
                                 "description": prepareDescription(row[2]),
                                 "directors": row[3],
                                 "collections": row[4],
                                 "duration": row[5],
                                 "actors": row[6],
                                 "viewDate": "1964-12-15"}

                response = requests.put(put_uri, json=movie_dto)
                if response.status_code != 200:
                    print("Error processing " + prepareTitle(row[0]) + ":" + prepareYear(row[1]))
                    exit(-1)
                line_count += 1
                if line_count % 50 == 0:
                    print(f'Processed {line_count} lines.')
        print(f'Processed {line_count} lines.')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    populateMovieDB()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
