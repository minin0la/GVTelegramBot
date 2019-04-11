import requests
import json
import time
import datetime

def checkseats(cinemaId, filmCode, showDate, showTime, hallNumber):
    url = "https://www.gv.com.sg/.gv-api/seatplan"
    payload = "{" + """"cinemaId":"{}","filmCode":"{}","showDate":"{}","showTime":"{}","hallNumber":"{}\"""".format(cinemaId, filmCode, showDate, showTime, hallNumber) + "}"
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
    return haveseatpercent, bookedseat, seatcount

def checkseatsdetail(cinemaId, filmCode, showDate, showTime, hallNumber):
    url = "https://www.gv.com.sg/.gv-api/seatplan"
    theshowDate = datetime.datetime.fromtimestamp(int(showDate) / 1000.0)
    theshowDate = time.strftime("%d-%m-%Y", time.gmtime(int(theshowDate.timestamp())))
    payload = "{" + """"cinemaId":"{}","filmCode":"{}","showDate":"{}","showTime":"{}","hallNumber":"{}\"""".format(cinemaId, filmCode, theshowDate, showTime, hallNumber) + "}"
    headers = {
        'accept': "application/json, text/plain, */*",
        'x_developer': "ENOVAX",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'content-type': "application/json; charset=UTF-8",
        }

    seatcolnum = 0
    seatrownum = 0
    response = requests.request("POST", url, data=payload, headers=headers)
    result = json.loads(response.text.encode('ascii', 'ignore'))
    for seatnumbers in result['data']:
        for seats in seatnumbers:
            if seats['colNumber'] > seatcolnum:
                seatcolnum = int(seats['colNumber'])
            if seats['rowNumber'] > seatrownum:
                seatrownum = int(seats['rowNumber'])
    theseatlist = dict()
    theseatlist['SCREEN'] = ['         Screen']
    for i in range(1, seatrownum):
        if i in theseatlist:
            theseatlist[str(i)].append('')
        else:
            # create a new array in this slot
            theseatlist[str(i)] = []
    for seatnumbers in result['data']:
        for seats in seatnumbers:
            if str(seats['rowNumber']) in theseatlist:
                if (seats['rowId'] is not None) and (seats['status'] == "L"):
                    theseatlist[str(seats['rowNumber'])].append('Y')
                elif (seats['rowId'] is not None) and (seats['status'] == "B"):
                    theseatlist[str(seats['rowNumber'])].append('X')
                elif (seats['rowId'] is not None) and (seats['status'] == "T"):
                    theseatlist[str(seats['rowNumber'])].append('B')
                else:
                    theseatlist[str(seats['rowNumber'])].append(' ')
    theresult = ''
    for k, v in theseatlist.items():
        if k == 'SCREEN':
            theresult = theresult + ''.join(v) + '\n'
        else:
            if int(k) < 10:
                theresult = theresult + k + '   ' + ''.join(v) + '\n'
            else:
                theresult = theresult + k + '  ' + ''.join(v) + '\n'
    return theresult

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

def getsessioninfo(cinemaId, filmCode, showDate):
    sessions = []
    keyboard = []
    thedetails = []
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
    midnightdate = datetime.datetime.fromtimestamp(showDate / 1000.0) - datetime.timedelta(hours=24)
    midnightdate = int((time.mktime(midnightdate.timetuple()))*1000)
    for locations in result['data']['locations']:
        if locations['id'] == cinemaId:
            for dates in locations['dates']:
                if (dates['date'] == midnightdate) or (dates['date'] == showDate):
                    for times in dates['times']:
                        if times['showDate'] == showDate:
                            theshowDate = datetime.datetime.fromtimestamp(times['showDate'] / 1000.0) + datetime.timedelta(hours=8)
                            theshowDate = time.strftime("%d-%m-%Y", time.gmtime(int(theshowDate.timestamp())))
                            seatpercent, bookedseat, seatcount = checkseats(cinemaId=cinemaId, filmCode=filmCode, showDate=theshowDate, showTime=times['time24'], hallNumber=times['hallNumber'])
                            sessions.append("Time: {} \nHall: {} ".format(times['time12'], times['hallNumber']) + "\nBooked: {} ".format(seatpercent) + "({}/{})\n".format(bookedseat, seatcount))
                            keyboard.append("{}".format(times['time12']))
                            thedetails.append({'time12':times['time12'], 'time24':times['time24'], 'hallNumber': times['hallNumber']})
                # elif dates['date'] == showDate:
                #     for times in dates['times']:
                #         if times['showDate'] == showDate:
                #             showDate = datetime.datetime.fromtimestamp(times['showDate'] / 1000.0) + datetime.timedelta(hours=8)
                #             showDate = time.strftime("%d-%m-%Y", time.gmtime(int(showDate.timestamp())))
                #             seatpercent, bookedseat, seatcount = checkseats(cinemaId=cinemaId, filmCode=filmCode, showDate=showDate, showTime=times['time24'], hallNumber=times['hallNumber'])
                #             sessions.append("Time: {} \nHall: {} ".format(times['time12'], times['hallNumber']) + "\nBooked: {} ".format(seatpercent) + "({}/{})\n".format(bookedseat, seatcount))
                #             keyboard.append("Time: {} ".format(times['time24']))
                #             thedetails.append({'time24':times['time24'], 'hallNumber': times['hallNumber']})
    return sessions, keyboard, thedetails