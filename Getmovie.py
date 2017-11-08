import requests
import json
import time
import datetime

def checkseats(cinemaId, filmCode, showDate, showTime, hallNumber):
    url = "https://www.gv.com.sg/.gv-api/seatplan"
    payload = "{" + """"cinemaId":"{}","filmCode":"{}","showDate":"{}","showTime":"{}","hallNumber":"{}\"""".format(cinemaId, filmCode, showDate, showTime, hallNumber) + "}"
    # payload = "{\"cinemaId\":\"04\",\"filmCode\":\"6111\",\"showDate\":\"06-11-2017\",\"showTime\":\"1915\",\"hallNumber\":\"5\"}"
    # print(payload)
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        }

    seatcount = 0
    haveseat = 0
    bookedseat = 0
    blockedseat = 0
    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for seatnumbers in result['data']:
        for seats in seatnumbers:
            if seats["status"] is not None:
                seatcount = seatcount + 1
            if seats["status"] == "L":
                haveseat = haveseat + 1
            if seats["status"] == "B":
                bookedseat = bookedseat + 1
            if seats["status"] == "T":
                blockedseat = blockedseat + 1
    haveseatpercent = float(bookedseat/seatcount)*(100.0)
    haveseatpercent = "{0:.2f}%".format(haveseatpercent)
    return haveseatpercent

def cinemalist():
    cinemalist = []
    url = "https://www.gv.com.sg/.gv-api/cinemas"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
    response = requests.request("POST", url, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for cinemaname in result['data']:
        cinemalist.append(cinemaname['name'])
    return cinemalist

def getcinemaid(cinematitle):
    url = "https://www.gv.com.sg/.gv-api/cinemas"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
    response = requests.request("POST", url, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for cinemaname in result['data']:
        if cinematitle.lower() == cinemaname['name'].lower():
            cinemaid = cinemaname['id']
    return cinemaid

def getcinemaname(cinemaid):
    url = "https://www.gv.com.sg/.gv-api/cinemas"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }
    response = requests.request("POST", url, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for cinemaname in result['data']:
        if cinemaname['id'] == cinemaid:
            name = cinemaname['name']
    return name

def nowshowinglist():
    movielist = []
    url = "https://www.gv.com.sg/.gv-api/nowshowing"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }

    response = requests.request("POST", url, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for moviename in result['data']:
        movielist.append(moviename['filmTitle'])
    return movielist

def getnowshowingname(filmid):
    url = "https://www.gv.com.sg/.gv-api/nowshowing"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }

    response = requests.request("POST", url, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for moviename in result['data']:
        if moviename['filmCd'] == filmid:
            name = moviename['filmTitle']
    return name

def getnowshowingid(filmTitle):
    url = "https://www.gv.com.sg/.gv-api/nowshowing"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        }

    response = requests.request("POST", url, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for moviename in result['data']:
        if filmTitle.lower() == moviename['filmTitle'].lower():
            movieid = moviename['filmCd']
    return movieid

def showingincinemalist(cinemaId):
    movielist = []
    url = "https://www.gv.com.sg/.gv-api/v2quickbuyfilms"
    payload = "{" + """"cinemaId":"{}\"""".format(cinemaId) + "}"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for moviename in result['data']:
        movielist.append(moviename['filmTitle'])
    return movielist

def getshowingincinemaid(cinemaId, filmTitle):
    url = "https://www.gv.com.sg/.gv-api/v2quickbuyfilms"
    payload = "{" + """"cinemaId":"{}\"""".format(cinemaId) + "}" 
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for moviename in result['data']:
        if filmTitle.lower() == moviename['filmTitle'].lower():
            movieid = moviename['filmCd']
    return movieid

def showingincinemadatelist(cinemaId, filmCode):
    datelist = []
    url = "https://www.gv.com.sg/.gv-api/v2quickbuydates"
    payload = "{" + """"cinemaId":"{}","filmCode":"{}\"""".format(cinemaId, filmCode) + "}"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for thedate in result['data']:
        date = datetime.datetime.fromtimestamp(thedate['date'] / 1000.0) + datetime.timedelta(hours=8)
        datelist.append(time.strftime("%a %d %b %Y", time.gmtime(int(date.timestamp()))))
    return datelist

def getunixdate(date):
    date = datetime.datetime.strptime(date, "%a %d %b %Y")
    date = (time.mktime(date.timetuple()))*1000
    return int(date)

def getsessioninfo(cinemaID, filmCode, date):
    sessions = []
    url = "https://www.gv.com.sg/.gv-api/sessionforfilm"
    payload = "{" + """"filmCode":"{}\"""".format(filmCode) + "}"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for locations in result['data']['locations']:
        if locations['id'] == cinemaID:
            for dates in locations['dates']:
                if dates['date'] == date:
                    for times in dates['times']:
                        showDate = datetime.datetime.fromtimestamp(times['showDate'] / 1000.0) + datetime.timedelta(hours=8)
                        showDate = time.strftime("%d-%m-%Y", time.gmtime(int(showDate.timestamp())))
                        seatpercent = checkseats(cinemaId=cinemaID, filmCode=filmCode, showDate=showDate, showTime=times['time24'], hallNumber=times['hallNumber'])
                        sessions.append("Time: {} \nHall: {} ".format(times['time12'], times['hallNumber']) + "Boooked: {}".format(seatpercent))
    return sessions

# movielist()
# cinemalist()
# cinemaid = input("Which cinema (ID): ")
# filmid = input("Which movie (ID): ")
# date = input("Which day? (DD-MM-YYYY): ")
# date = datetime.datetime.strptime(date, "%d-%m-%Y") + datetime.timedelta(hours=16)
# date = (time.mktime(date.timetuple()))*1000
# timing = checktiming(cinemaId=cinemaid, filmCode=filmid, date=int(date))
# print("Show details for {} at {}".format(showmoviename(filmid), showcinemaname(cinemaid)))
# result = ''
# for time in timing:
#     result = result + time['showDate'] + "\n"
#     result = result + time['time12'] + "\n"
#     seatpercent = checkseats(cinemaId=cinemaid, filmCode=filmid, showDate=time['showDate'], showTime=time['time24'], hallNumber=time['hall'])
#     result = result + "Booked: {}".format(seatpercent) + "\n"
# print(result)
# url = "https://www.gv.com.sg/.gv-api/nowshowing"

# headers = {
#     'accept': "application/json, text/plain, */*",
#     'x_developer': "ENOVAX",
#     'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
#     }

# print("Getting now showing movie in Golden Village")
# response = requests.request("POST", url, headers=headers)
# result = json.loads(response.text.encode('ascii', 'ignore'))
# for moviename in result['data']:
#     print(moviename['filmTitle'] + " " + moviename['filmCd'])

# FlimID = input("Which flim?: ")
# url = 'https://www.gv.com.sg/.gv-api/sessionforfilm'
# payload = "{" + """"filmCode": """ + "{}".format(FlimID) + "}"

# headers = {
#     'accept': "application/json, text/plain, */*",
#     'x_developer': "ENOVAX",
#     'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
#     'content-type': "application/json; charset=UTF-8",
#     }
# response = requests.request("POST", url, data=payload, headers=headers)
# result = json.loads(response.text.encode('ascii', 'ignore'))
# filmcode = result['data']['filmCd']
# for location_name in result['data']['locations']:
#     if location_name['name'] == "GV Jurong Point":
#         print("Showing Result for {}".format(location_name['name']))
#         print("Movie Name: {}".format(result['data']['filmTitle']))
#         cinemaId = location_name['id']
#         for the_date in location_name['dates']:
#             print(time.strftime("\nDate: %a %d %b %Y", time.gmtime(int(the_date['date']) / 1000.0)))
#             showDate = time.strftime("%d-%m-%Y", time.gmtime(int(the_date['date']) / 1000.0))
#             for the_time in the_date['times']:
#                 try:
#                     seatpercent = checkseats(cinemaId=cinemaId, filmCode=filmcode, showDate=showDate, showTime=the_time['time24'], hallNumber=the_time['hallNumber'])
#                     print("Time: {} ".format(the_time['time12']) + "Sold: {} ".format(seatpercent) + "Hall Number: {}".format(the_time['hallNumber']))
#                 except:
#                     pass
#         print(location_name['dates'])