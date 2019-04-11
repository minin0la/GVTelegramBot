import Getmovie

cinemaname = "GV Tiong Bahru"
print(Getmovie.cinemalist())
cinemanid = Getmovie.getcinemaid(cinemaname.lower())
print(Getmovie.showingincinemalist(cinemanid))
moviename = "Marvel Studios' Avengers: Endgame*"
movieid = Getmovie.getshowingincinemaid(cinemaId=cinemanid, filmTitle=moviename.lower())
print(Getmovie.showingincinemadatelist(cinemanid, movieid))
date = Getmovie.getunixdate("Sun 28 Apr 2019")
sessions, keyboard, thedetails = Getmovie.getsessioninfo(cinemaId=50, filmCode=6549, showDate=1556409600000)
print(sessions)