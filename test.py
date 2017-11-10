import Getmovie

print(Getmovie.checkseatsdetail(cinemaId="04",filmCode="3456",showDate="11-11-2017",showTime="1040",hallNumber="4"))
sessions, keyboard, thedetails = Getmovie.getsessioninfo(cinemaId="04",filmCode="3456",showDate=1510243200000)
print(thedetails)