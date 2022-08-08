from matplotlib.pyplot import text
import requests
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime, timedelta
today = date.today()
today_date=today.strftime("%d %b, %Y")
day_count=today.weekday()
year=today.strftime("%Y")
Zodiac_carousel_Images=[{"Zodiac_Sign":1,"Sign":"Aries","Image_url":"/media/Zodiac_carousels/Aries_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Aries.png',"present_date":today_date},
{"Zodiac_Sign":2,"Sign":"Taurus","Image_url":"/media/Zodiac_carousels/Taurus_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/taurus.png',"present_date":today_date},
{"Zodiac_Sign":3,"Sign":"Gemini","Image_url":"/media/Zodiac_carousels/Gemini_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Gemini.png',"present_date":today_date},
{"Zodiac_Sign":4,"Sign":"Cancer","Image_url":"/media/Zodiac_carousels/Cancer_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Cancer.png',"present_date":today_date},
{"Zodiac_Sign":5,"Sign":"Leo","Image_url":"/media/Zodiac_carousels/Leo_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Leo.png',"present_date":today_date},
{"Zodiac_Sign":6,"Sign":"Virgo","Image_url":"/media/Zodiac_carousels/Virgo_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Virgo.png',"present_date":today_date},
{"Zodiac_Sign":7,"Sign":"Libra","Image_url":"/media/Zodiac_carousels/Libra_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Libra.png',"present_date":today_date},
{"Zodiac_Sign":8,"Sign":"Scorpio","Image_url":"/media/Zodiac_carousels/Scorpio_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Scorpio.png',"present_date":today_date},
{"Zodiac_Sign":9,"Sign":"Sagittarius","Image_url":"/media/Zodiac_carousels/Sagittarius_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Sagittarius.png',"present_date":today_date},
{"Zodiac_Sign":10,"Sign":"Capricorn","Image_url":"/media/Zodiac_carousels/Capricorn_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Capricorn.png',"present_date":today_date},
{"Zodiac_Sign":11,"Sign":"Aquarius","Image_url":"/media/Zodiac_carousels/Aquarius_Zodiac.jpg",'zodiac_image_sign':'/media/Horoscope_Symbols/Aquarius.png',"present_date":today_date},
{"Zodiac_Sign":12,"Sign":"Pisces","Image_url":"/media/Zodiac_carousels/Pisces_Zodiac.png",'zodiac_image_sign':'/media/Horoscope_Symbols/Pisces.png',"present_date":today_date},
]
def YesterdayHoroscope(zodiac_sign :int) -> str:
   url = ("https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-yesterday.aspx?sign={zodiac_sign}" ) 
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text 

def DailyHoroscope(zodiac_sign: int) -> str:
    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-today.aspx?sign={zodiac_sign}" ) 
    soup = BeautifulSoup(requests.get(url).content, "html.parser") 
    return soup.find("div", class_="main-horoscope").p.text 

def TommorrowHoroscope(zodiac_sign: int) -> str:
    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-daily-tomorrow.aspx?sign={zodiac_sign}" )
    soup = BeautifulSoup(requests.get(url).content, "html.parser") 
    return soup.find("div", class_="main-horoscope").p.text 

def WeeklyHoroscope(zodiac_sign: int) -> str:
    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-weekly.aspx?sign={zodiac_sign}" )
    soup = BeautifulSoup(requests.get(url).content, "html.parser") 
    return soup.find("div", class_="main-horoscope").p.text 

def MonthlyHoroscope(zodiac_sign: int) -> str:
    url = (
        "https://www.horoscope.com/us/horoscopes/general/"
        f"horoscope-general-monthly.aspx?sign={zodiac_sign}" )
    soup = BeautifulSoup(requests.get(url).content, "html.parser") 
    return soup.find("div", class_="main-horoscope").p.text 

def start_day_date():
    if day_count>=0:
        return (today-timedelta(days=day_count))
def end_day_date():
    if day_count<7:
        return (today+timedelta(days=7-day_count))

def FindZodiacSign(sign):
   for zodiac in Zodiac_carousel_Images:
      if zodiac['Sign']==sign:
         return str(int(zodiac['Zodiac_Sign']-1))

def GetZodiacImg(sign):
   for zodiac in Zodiac_carousel_Images:
      if zodiac['Sign']==sign:
         return zodiac['zodiac_image_sign']

def GetMonth(sign):
   if sign == 1:
      return 'January'
   if sign == 2:
      return 'February'
   if sign == 3:
      return 'March'
   if sign == 4:
      return 'April'
   if sign == 5:
      return 'May'
   if sign == 6:
      return 'June'
   if sign == 7:
      return 'July'
   if sign == 8:
      return 'August'
   if sign == 9:
      return 'September'
   if sign == 10:
      return 'October'
   if sign == 11:
      return 'November'
   if sign ==12:
      return 'December'

def GetLoveCompatibilityRatingDetail(sign1, sign2):
   url =("https://www.horoscope.com/us/games/compatibility/game-love-compatibility.aspx?"
   f"ZodiacSignSelector_alphastring={sign1}&PartnerZodiacSignSelector_alphastring={sign2}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="game-compatibility-score").text 

def GetLoveCompatibilityDescDetail(zodiac1, zodiac2):
   url =("https://www.horoscope.com/us/games/compatibility/game-love-compatibility.aspx?"
   f"ZodiacSignSelector_alphastring={zodiac1}&PartnerZodiacSignSelector_alphastring={zodiac2}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="module-skin").p.text 

def GetZodiacSignNo(day, month):
   # checks month and date within the valid range
   # of a specified zodiac
   if month == 'december':
      astro_sign_no = '8' if (day < 22) else '9'
   elif month == 'january':
      astro_sign_no = '9' if (day < 20) else '10'
   elif month == 'february':
      astro_sign_no = '10' if (day < 19) else '11'
   elif month == 'march':
      astro_sign_no = '11' if (day < 21) else '0'
   elif month == 'april':
      astro_sign_no = '0' if (day < 20) else '1'
   elif month == 'may':
      astro_sign_no = '1' if (day < 21) else '2'
   elif month == 'june':
      astro_sign_no = '2' if (day < 21) else '3'
   elif month == 'july':
      astro_sign_no = '3' if (day < 23) else '4'
   elif month == 'august':
      astro_sign_no = '4' if (day < 23) else '5'
   elif month == 'september':
      astro_sign_no = '5' if (day < 23) else '6'
   elif month == 'october':
      astro_sign_no = "6" if (day < 23) else '7'
   elif month == 'november':
      astro_sign_no = '7' if (day < 22) else '8'
   return (astro_sign_no)

#### Get Birthday Details ####
def GetZodiacHoroscopeSign(day,month):
   astro_sign=""
   if month == 'december':
      astro_sign = 'Sagittarius' if (day < 22) else 'Capricorn'
   elif month == 'january':
      astro_sign = 'Capricorn' if (day < 20) else 'Aquarius'
   elif month == 'february':
      astro_sign = 'Aquarius' if (day < 19) else 'Pisces'
   elif month == 'march':
      astro_sign = 'Pisces' if (day < 21) else 'Aries'
   elif month == 'april':
      astro_sign = 'Aries' if (day < 20) else 'Taurus'
   elif month == 'may':
      astro_sign = 'Taurus' if (day < 21) else 'Gemini'
   elif month == 'june':
      astro_sign = 'Gemini' if (day < 21) else 'Cancer'
   elif month == 'july':
      astro_sign = 'Cancer' if (day < 23) else 'Leo'
   elif month == 'august':
      astro_sign = 'Leo' if (day < 23) else 'Virgo'
   elif month == 'september':
      astro_sign = 'Virgo' if (day < 23) else 'Libra'
   elif month == 'october':
      astro_sign = 'Libra' if (day < 23) else 'Scorpio'
   elif month == 'november':
      astro_sign = 'Scorpio' if (day < 22) else 'Sagittarius'
   return (astro_sign)

def TodayBirthGeneralDetail():
   url =("https://www.horoscope.com/birthday-horoscope.aspx")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("main", class_="birthday-default").p.text 

def TodayBirthDestinationIdeaDetail(zodiac_sign : str):
   url =(f"https://www.horoscope.com/birthday-horoscope/{zodiac_sign}-destinations")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   bdaydestinations = soup.find("main", class_="birthday-party-ideas")
   Zodiacdet=bdaydestinations.find_all('p')
   return list(map(lambda x: x.getText(), Zodiacdet))

def TodayBirthGiftIdeaDetail(zodiac_sign : str):
   url =(f"https://www.horoscope.com/birthday-horoscope/{zodiac_sign}-gifts")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   bdaygifts = soup.find("main", class_="birthday-party-ideas")
   Zodiacdet=bdaygifts.find_all('p')
   return list(map(lambda x: x.getText(), Zodiacdet))

def TodayBirthPartyIdeaDetail(zodiac_sign : str):
   url =(f"https://www.horoscope.com/birthday-horoscope/{zodiac_sign}-party")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   bdayparty = soup.find("main", class_="birthday-party-ideas")
   Zodiacdet=bdayparty.find_all('p')
   return list(map(lambda x: x.getText(), Zodiacdet))

def TodayBirthPamperingIdeaDetail(zodiac_sign : str):
   url =(f"https://www.horoscope.com/birthday-horoscope/{zodiac_sign}-pampering")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   bdaypampering = soup.find("main", class_="birthday-party-ideas")
   Zodiacdet=bdaypampering.find_all('p')
   return list(map(lambda x: x.getText(), Zodiacdet))

def GetZodiacGeneralDatewiseOverallDetail(zodiac_date : str):
   url=(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-birthday.aspx?laDate={zodiac_date}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("main", class_="birthday-default").p.text 

### Zodiac Sign Findings ###
def GetZodiacSign(bdate):
   birth_date=int(bdate.strftime("%d"))
   birth_month=bdate.strftime("%B").lower() 
   zodiac_no=GetZodiacSignNo(birth_date,birth_month)
   return zodiac_no

# TOTAL ZODIAC OVERVIEW DETAILS
def GetTotalZodiacOverviewDetails(zodiac_year : int):
   Zodiac_Para_Details=[]
   url=(f"https://www.horoscope.com/us/horoscopes/yearly/{zodiac_year}-horoscope-overview.aspx")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   list_details = soup.find_all('p')
   for i in list_details:
      Zodiac_Para_Details.append(i.getText())
   return Zodiac_Para_Details[2:-1]

# Every Zodiac Overview 
def GetZodiacOverviewDetails(zodiac_year : int, zodiac_sign : str):
   url=("https://www.horoscope.com/us/horoscopes/yearly/"
     f"{zodiac_year}-horoscope-{zodiac_sign}.aspx?type=personal")
   soup = BeautifulSoup(requests.get(url).content, 'html.parser')
   ZodiacDetails = soup.find('section', class_='tab-content')
   ZodiacOverviewDetails=ZodiacDetails.find_all('p')
   return list(map(lambda x: x.getText(), ZodiacOverviewDetails))
   
def GetZodiacLoveCouplesOverallViewDetails(zodiac_year : int, zodiac_sign : str) -> str:
   url=(f"https://www.horoscope.com/us/horoscopes/yearly/{zodiac_year}-horoscope-{zodiac_sign}.aspx?type=love_couples")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   ZodiacDetails = soup.find('section', class_='tab-content')
   LoveCoupleDetails = ZodiacDetails.find_all('p')
   return list(map(lambda x: x.getText(), LoveCoupleDetails))

def GetZodiacLoveSinglesOverallViewDetails(zodiac_year : int, zodiac_sign : str) -> str:
   url=(f"https://www.horoscope.com/us/horoscopes/yearly/{zodiac_year}-horoscope-{zodiac_sign}.aspx?type=love_single")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   ZodiacDetails = soup.find('section', class_='tab-content')
   LoveSingleDetails = ZodiacDetails.find_all('p')
   return list(map(lambda x: x.getText(), LoveSingleDetails))
   
def GetZodiacCareerMoneyOverallViewDetails(zodiac_year : int, zodiac_sign : str) -> str:
   url=(f"https://www.horoscope.com/us/horoscopes/yearly/{zodiac_year}-horoscope-{zodiac_sign}.aspx?type=career")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   ZodiacDetails = soup.find('section', class_='tab-content')
   MoneyCareerDetails = ZodiacDetails.find_all('p')
   return list(map(lambda x: x.getText(), MoneyCareerDetails))

# CAREER DETAILS
def GetYesterdayCareerHoroscopeDetails(zodiac_sign : int) -> str:
   url =("https://www.horoscope.com/us/horoscopes/general/"
         f"horoscope-general-daily-yesterday.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetTodayCareerHoroscopeDetails(zodiac_sign : int) -> str:
   url =("https://www.horoscope.com/us/horoscopes/career/"
         f"horoscope-career-daily-today.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text 

def GetTomorrowCareerHoroscopeDetails(zodiac_sign : int) -> str:
   url =("https://www.horoscope.com/us/horoscopes/"
         f"general/horoscope-general-daily-tomorrow.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text    

def GetWeeklyCareerHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/general/"
         f"horoscope-general-weekly.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetMonthlyCareerHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/general/"
      f"horoscope-general-monthly.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

# HEALTH DETAILS
def GetYesterdayHealthHoroscopeDetails(zodiac_sign : int) -> str:
   url =("https://www.horoscope.com/us/horoscopes/wellness/"
      f"horoscope-wellness-daily-yesterday.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetTodayHealthHoroscopeDetails(zodiac_sign : int) -> str:
   url = ("https://www.horoscope.com/us/horoscopes/wellness/"
      f"horoscope-wellness-daily-today.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text 

def GetTomorrowHealthHoroscopeDetails(zodiac_sign : int) -> str:
   url = ("https://www.horoscope.com/us/horoscopes/wellness/"
      f"horoscope-wellness-daily-tomorrow.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text    

def GetWeeklyHealthHoroscopeDetails(zodiac_sign : int) -> str:
   url = ("https://www.horoscope.com/us/horoscopes/wellness/"
      f"horoscope-wellness-weekly.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetMonthlyHealthHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/wellness/"
      f"horoscope-wellness-monthly.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

# LOVE INFORMATION
def GetYesterdayLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-daily-yesterday.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetTodayLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-daily-today.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text 

def GetTomorrowLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-daily-tomorrow.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text   

def GetWeeklySingleLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-weekly-single.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetWeeklyCoupleLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-weekly-couple.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetMonthlySingleLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-monthly-single.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

def GetMonthlyCoupleLoveHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/love/"
      f"horoscope-love-monthly-couple.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

# MONEY DETAILS
def GetWeeklyMoneyHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/money/"
         f"horoscope-money-weekly.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text

# RETAIL DETAILS
def GetWeeklyRetailHoroscopeDetails(zodiac_sign : int) -> str:
   url=("https://www.horoscope.com/us/horoscopes/general/"
      f"retail-therapy-horoscope.aspx?sign={zodiac_sign}")
   soup = BeautifulSoup(requests.get(url).content, "html.parser") 
   return soup.find("div", class_="main-horoscope").p.text