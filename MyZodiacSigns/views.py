from django.http import HttpResponse
from django.shortcuts import render, redirect
from .HoroscopeDetailExtraction import *
from datetime import timedelta, datetime
from .forms import *

today = date.today()
yesterday_date=datetime.now() - timedelta(days=1)
today_date=today.strftime("%d %b, %Y")
tomorrow_date = datetime.now() + timedelta(days=1)
year=today.strftime("%Y")
def HomePageView(request):
    return render(request,"MyZodiacSigns/HomePage.html",{})

def AboutPageView(request):
    return render(request,'MyZodiacSigns/About.html',{})

def DailyHoroscopeDetailView(request):
    for zodiac_det in Zodiac_carousel_Images:
        i=zodiac_det["Zodiac_Sign"]
        zodiac_det["description"]=DailyHoroscope(i).split('-')[-1] 
    return render(request, 'MyZodiacSigns/Zodiac_Horoscope_Types/DailyHoroscopes.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def TomorrowHoroscopeDetailView(request):
    for zodiac_det in Zodiac_carousel_Images:
        zodiac_det["present_date"]=tomorrow_date.strftime("%d %b, %Y")
        i=zodiac_det["Zodiac_Sign"]
        zodiac_det["description"]=TommorrowHoroscope(i).split('-')[-1] 
    return render(request, 'MyZodiacSigns/Zodiac_Horoscope_Types/TomorrowHoroscopes.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def WeeklyHoroscopeDetailView(request):
    for zodiac_det in Zodiac_carousel_Images:
        zodiac_det["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
        zodiac_det["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
        i=zodiac_det["Zodiac_Sign"]
        zodiac_det["description"]=". ".join(WeeklyHoroscope(i).split('-')[2:])
    return render(request, 'MyZodiacSigns/Zodiac_Horoscope_Types/WeeklyHoroscopes.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def MonthlyHoroscopeDetailView(request):
    for zodiac_det in Zodiac_carousel_Images:
        zodiac_det["present_month"]=tomorrow_date.strftime("%b, %Y")
        i=zodiac_det["Zodiac_Sign"]
        zodiac_det["description"]=MonthlyHoroscope(i).split('-')[-1] 
    return render(request, 'MyZodiacSigns/Zodiac_Horoscope_Types/MonthlyHoroscopes.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def YearlyHoroscopeDetailView(request):
    for zodiac_det in Zodiac_carousel_Images:
        zodiac_det["present_year"]=tomorrow_date.strftime("%Y")
        i=zodiac_det["Zodiac_Sign"]
        zodiac_det["description"]=MonthlyHoroscope(i).split('-')[-1] 
    return render(request, 'MyZodiacSigns/Zodiac_Horoscope_Types/YearlyHoroscope.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def FindZodiacDetailView(request):
    ZodiacFindingDetails={}
    submitbutton= request.POST.get("submit")
    form = ZodiacFindingDetailForm(request.POST or None)
    if form.is_valid():
        ZodiacFindingDetails['Person_Name'] = form.cleaned_data.get("person_name")
        ZodiacFindingDetails['Person_Age'] = form.cleaned_data.get("Age")
        ZodiacFindingDetails['Birth_Date'] = form.cleaned_data.get("birth_date")
        ZodiacFindingDetails['Birth_Year'] = str(ZodiacFindingDetails['Birth_Date']).split('-')[0]
        ZodiacFindingDetails['Birth_Month_No'] = GetMonth(int(str(ZodiacFindingDetails['Birth_Date']).split('-')[1]))
        ZodiacFindingDetails['Birth_Day'] = str(ZodiacFindingDetails['Birth_Date']).split('-')[2]
        ZodiacFindingDetails['Zodiac_Sign'] =  str(GetZodiacHoroscopeSign(int(ZodiacFindingDetails['Birth_Day']),ZodiacFindingDetails['Birth_Month_No'].lower()))
    context={'form':form,'submitbutton':submitbutton,'ZodiacFindingDetails':ZodiacFindingDetails}
    return render(request, 'MyZodiacSigns/Zodiac_Sign_Detail/Zodiac_Sign_Finding.html', context)

def ZodiacLoveCompatibilityDetailView(request):
    submitbutton= request.POST.get("submit")
    zodiac1=""
    zodiac2=""
    context={}
    LoveCompatibity={}
    if request.method == "POST":
        form = ZodiacLoveCompatibilityForm(request.POST)
        if form.is_valid():
            zodiac1= form.cleaned_data.get("First_Zodiac_Sign")
            zodiac2= form.cleaned_data.get("Second_Zodiac_Sign")
            LoveCompatibity['Zodiac_Sign1']=FindZodiacSign(zodiac1)
            LoveCompatibity['Zodiac_Sign2']=FindZodiacSign(zodiac2)
            LoveCompatibity['Zodiac_rating']=int(GetLoveCompatibilityRatingDetail(LoveCompatibity['Zodiac_Sign1'],LoveCompatibity['Zodiac_Sign2']).split('/')[0])
            LoveCompatibity['Zodiac_rating_Range']=range(LoveCompatibity['Zodiac_rating'])
            LoveCompatibity['Zodiac_Remaining_Rating_Range']=range(LoveCompatibity['Zodiac_rating'],10)
            LoveCompatibity['Zodiac_Desc'] =GetLoveCompatibilityDescDetail(LoveCompatibity['Zodiac_Sign1'],LoveCompatibity['Zodiac_Sign2'])
            LoveCompatibity['zodiac_img1']=GetZodiacImg(zodiac1)
            LoveCompatibity['zodiac_img2']=GetZodiacImg(zodiac2)
            context={"zodiac1":zodiac1,"zodiac2":zodiac2,'submitbutton':submitbutton,'form':form,'LoveCompatibity':LoveCompatibity}
    else:
        form = ZodiacLoveCompatibilityForm()
        context['form']=form
    return render(request, 'MyZodiacSigns/LoveCompatibility/ZodiacLoveCompatibility.html',context)

def TodayBirthdateGeneralHoroscopeDetailView(request):
    TodayBirthdate={}
    today_month=today.strftime("%B").lower() 
    today_day = int(today.strftime("%d"))
    TodayBirthdate['Today_Day'] = today_day
    TodayBirthdate['Today_Month'] = today_month 
    TodayBirthdate['ZodiacSign'] = GetZodiacHoroscopeSign(today_day,today_month)
    TodayBirthdate['Birthday_Desc'] = str(TodayBirthGeneralDetail())
    return render(request, 'MyZodiacSigns/Birthday_Horoscopes/Today_Birthdate_Horoscopes/BirthdayGeneral/GeneralDetails.html',{'TodayBirthdate':TodayBirthdate})

def TodayBirthdateGiftDetailView(request):
    TodayBirthdate={}
    today_month=today.strftime("%B").lower() 
    today_day = int(today.strftime("%d"))
    TodayBirthdate['Today_Day'] = today_day
    TodayBirthdate['Today_Month'] = today_month 
    TodayBirthdate['ZodiacSign'] = GetZodiacHoroscopeSign(today_day,today_month)
    TodayBirthdate['Birthday_Desc'] = TodayBirthGiftIdeaDetail(TodayBirthdate['ZodiacSign'])
    return render(request, 'MyZodiacSigns/Birthday_Horoscopes/Today_Birthdate_Horoscopes/BirthdayGifts/GiftIdeaDetails.html',{'TodayBirthdate':TodayBirthdate})

def TodayBirthdateDestinationsDetailView(request):
    TodayBirthdate={}
    today_month=today.strftime("%B").lower() 
    today_day = int(today.strftime("%d"))
    TodayBirthdate['Today_Day'] = today_day
    TodayBirthdate['Today_Month'] = today_month 
    TodayBirthdate['ZodiacSign'] = GetZodiacHoroscopeSign(today_day,today_month)
    TodayBirthdate['Birthday_Desc'] = TodayBirthDestinationIdeaDetail(TodayBirthdate['ZodiacSign'])
    return render(request, 'MyZodiacSigns/Birthday_Horoscopes/Today_Birthdate_Horoscopes/BirthdayDestinations/DestinationDetails.html',{'TodayBirthdate':TodayBirthdate})

def TodayBirthdatePartyDetailView(request):
    TodayBirthdate={}
    today_month=today.strftime("%B").lower() 
    today_day = int(today.strftime("%d"))
    TodayBirthdate['Today_Day'] = today_day
    TodayBirthdate['Today_Month'] = today_month 
    TodayBirthdate['ZodiacSign'] = GetZodiacHoroscopeSign(today_day,today_month)
    TodayBirthdate['Birthday_Desc'] = TodayBirthPartyIdeaDetail(TodayBirthdate['ZodiacSign'])
    return render(request, 'MyZodiacSigns/Birthday_Horoscopes/Today_Birthdate_Horoscopes/BirthdayParty/PartyIdeaDetails.html',{'TodayBirthdate':TodayBirthdate})

def TodayBirthdatePamperingDetailView(request):
    TodayBirthdate={}
    today_month=today.strftime("%B").lower() 
    today_day = int(today.strftime("%d"))
    TodayBirthdate['Today_Day'] = today_day
    TodayBirthdate['Today_Month'] = today_month 
    TodayBirthdate['ZodiacSign'] = GetZodiacHoroscopeSign(today_day,today_month)
    TodayBirthdate['Birthday_Desc'] = TodayBirthPamperingIdeaDetail(TodayBirthdate['ZodiacSign'])
    return render(request, 'MyZodiacSigns/Birthday_Horoscopes/Today_Birthdate_Horoscopes/BirthdayPamperings/PamperingIdeaDetails.html',{'TodayBirthdate':TodayBirthdate})

def DateWiseBirthDateGeneralOverallDetailView(request):
    DateWiseBirthDate={}
    submitbutton= request.POST.get("submit")
    form = BirthDateDetailForm(request.POST)
    if form.is_valid():
        DateWiseBirthDate['Person_Name'] = form.cleaned_data.get("person_name")
        DateWiseBirthDate['Birth_Date'] = form.cleaned_data.get("Birth_Date")
        DateWiseBirthDate['Birth_Month'] = form.cleaned_data.get("Birth_Month")
        DateWiseBirthDate['Birth_Year'] = year
        DateWiseBirthDate['General_Desc'] = str(GetZodiacGeneralDatewiseOverallDetail(str(DateWiseBirthDate['Birth_Year'])+str(DateWiseBirthDate['Birth_Month'])+str(DateWiseBirthDate['Birth_Date'])))
        DateWiseBirthDate['ZodiacSign'] = GetZodiacHoroscopeSign(int(DateWiseBirthDate['Birth_Date']),DateWiseBirthDate['Birth_Month'].lower())
        DateWiseBirthDate['Bday_Party_Desc'] = TodayBirthPartyIdeaDetail(DateWiseBirthDate['ZodiacSign'])
        DateWiseBirthDate['Bday_Destination_Desc'] = TodayBirthDestinationIdeaDetail(DateWiseBirthDate['ZodiacSign'])
        DateWiseBirthDate['Bday_Pampering_Desc'] = TodayBirthPamperingIdeaDetail(DateWiseBirthDate['ZodiacSign'])
        DateWiseBirthDate['Bday_Gifts_Desc'] = TodayBirthGiftIdeaDetail(DateWiseBirthDate['ZodiacSign'])
    return render(request, 'MyZodiacSigns/Birthday_Horoscopes/Datewise_Birthday_Horoscope/BirthdayGeneral/GeneralOverallDetails.html',{'DateWiseBirthDate':DateWiseBirthDate,'submitbutton':submitbutton,'form':form})

#### Overall View Details ####
def OverallZodiacOverviewDetailView(request):
    ZodiacOverallViewDetails={}
    ZodiacOverallViewDetails["Description"] = GetTotalZodiacOverviewDetails(year)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/ZodiacOverviewDetails.html',{'ZodiacOverallViewDetails':ZodiacOverallViewDetails,'Zodiac_carousel_Images':Zodiac_carousel_Images})

#Horoscope Details
def OverallZodiacHoroscopesDetailView(request):
    return render(request, 'MyZodiacSigns/Zodiac_Signs/ZodiacHoroscopeDetail.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def AriesHoroscopeDetailView(request):
    AriesHoroscopeDetails={}
    AriesHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AriesHoroscopeDetails['Present_Date']=str(today_date)
    AriesHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AriesHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AriesHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AriesHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    AriesHoroscopeDetails['Year']=year
    AriesHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(1).split("-")[1:])
    AriesHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(1).split("-")[1:])
    AriesHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(1).split("-")[1:])
    AriesHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(1).split("-")[2:])
    AriesHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(1).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/Horoscope/HoroscopeDetails.html',{'AriesHoroscopeDetails':AriesHoroscopeDetails})

def TaurusHoroscopeDetailView(request):
    TaurusHoroscopeDetails={}
    TaurusHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    TaurusHoroscopeDetails['Present_Date']=str(today_date)
    TaurusHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    TaurusHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    TaurusHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    TaurusHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    TaurusHoroscopeDetails['Year']=year
    TaurusHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(2).split("-")[1:])
    TaurusHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(2).split("-")[1:])
    TaurusHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(2).split("-")[1:])
    TaurusHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(2).split("-")[2:])
    TaurusHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(2).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/Horoscope/HoroscopeDetails.html',{'TaurusHoroscopeDetails':TaurusHoroscopeDetails})

def GeminiHoroscopeDetailView(request):
    GeminiHoroscopeDetails={}
    GeminiHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    GeminiHoroscopeDetails['Present_Date']=str(today_date)
    GeminiHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    GeminiHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    GeminiHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    GeminiHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    GeminiHoroscopeDetails['Year']=year
    GeminiHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(3).split("-")[1:])
    GeminiHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(3).split("-")[1:])
    GeminiHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(3).split("-")[1:])
    GeminiHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(3).split("-")[2:])
    GeminiHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(3).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/Horoscope/HoroscopeDetails.html',{'GeminiHoroscopeDetails':GeminiHoroscopeDetails})

def CancerHoroscopeDetailView(request):
    CancerHoroscopeDetails={}
    CancerHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CancerHoroscopeDetails['Present_Date']=str(today_date)
    CancerHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CancerHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CancerHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CancerHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    CancerHoroscopeDetails['Year']=year
    CancerHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(4).split("-")[1:])
    CancerHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(4).split("-")[1:])
    CancerHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(4).split("-")[1:])
    CancerHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(4).split("-")[2:])
    CancerHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(4).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/Horoscope/HoroscopeDetails.html',{'CancerHoroscopeDetails':CancerHoroscopeDetails})

def LeoHoroscopeDetailView(request):
    LeoHoroscopeDetails={}
    LeoHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LeoHoroscopeDetails['Present_Date']=str(today_date)
    LeoHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LeoHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LeoHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LeoHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    LeoHoroscopeDetails['Year']=year
    LeoHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(5).split("-")[1:])
    LeoHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(5).split("-")[1:])
    LeoHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(5).split("-")[1:])
    LeoHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(5).split("-")[2:])
    LeoHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(5).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/Horoscope/HoroscopeDetails.html',{'LeoHoroscopeDetails':LeoHoroscopeDetails})

def VirgoHoroscopeDetailView(request):
    VirgoHoroscopeDetails={}
    VirgoHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    VirgoHoroscopeDetails['Present_Date']=str(today_date)
    VirgoHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    VirgoHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    VirgoHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    VirgoHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    VirgoHoroscopeDetails['Year']=year
    VirgoHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(6).split("-")[1:])
    VirgoHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(6).split("-")[1:])
    VirgoHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(6).split("-")[1:])
    VirgoHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(6).split("-")[2:])
    VirgoHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(6).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/Horoscope/HoroscopeDetails.html',{'VirgoHoroscopeDetails':VirgoHoroscopeDetails})

def LibraHoroscopeDetailView(request):
    LibraHoroscopeDetails={}
    LibraHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LibraHoroscopeDetails['Present_Date']=str(today_date)
    LibraHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LibraHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LibraHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LibraHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    LibraHoroscopeDetails['Year']=year
    LibraHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(7).split("-")[1:])
    LibraHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(7).split("-")[1:])
    LibraHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(7).split("-")[1:])
    LibraHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(7).split("-")[2:])
    LibraHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(7).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/Horoscope/HoroscopeDetails.html',{'LibraHoroscopeDetails':LibraHoroscopeDetails})

def ScorpioHoroscopeDetailView(request):
    ScorpioHoroscopeDetails={}
    ScorpioHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    ScorpioHoroscopeDetails['Present_Date']=str(today_date)
    ScorpioHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    ScorpioHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    ScorpioHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    ScorpioHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    ScorpioHoroscopeDetails['Year']=year
    ScorpioHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(8).split("-")[1:])
    ScorpioHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(8).split("-")[1:])
    ScorpioHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(8).split("-")[1:])
    ScorpioHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(8).split("-")[2:])
    ScorpioHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(8).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/Horoscope/HoroscopeDetails.html',{'ScorpioHoroscopeDetails':ScorpioHoroscopeDetails})

def SagittariusHoroscopeDetailView(request):
    SagittariusHoroscopeDetails={}
    SagittariusHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    SagittariusHoroscopeDetails['Present_Date']=str(today_date)
    SagittariusHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    SagittariusHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    SagittariusHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    SagittariusHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    SagittariusHoroscopeDetails['Year']=year
    SagittariusHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(9).split("-")[1:])
    SagittariusHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(9).split("-")[1:])
    SagittariusHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(9).split("-")[1:])
    SagittariusHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(9).split("-")[2:])
    SagittariusHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(9).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/Horoscope/HoroscopeDetails.html',{'SagittariusHoroscopeDetails':SagittariusHoroscopeDetails})

def CapricornHoroscopeDetailView(request):
    CapricornHoroscopeDetails={}
    CapricornHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CapricornHoroscopeDetails['Present_Date']=str(today_date)
    CapricornHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CapricornHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CapricornHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CapricornHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    CapricornHoroscopeDetails['Year']=year
    CapricornHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(10).split("-")[1:])
    CapricornHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(10).split("-")[1:])
    CapricornHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(10).split("-")[1:])
    CapricornHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(10).split("-")[2:])
    CapricornHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(10).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/Horoscope/HoroscopeDetails.html',{'CapricornHoroscopeDetails':CapricornHoroscopeDetails})

def AquariusHoroscopeDetailView(request):
    AquariusHoroscopeDetails={}
    AquariusHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AquariusHoroscopeDetails['Present_Date']=str(today_date)
    AquariusHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AquariusHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AquariusHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AquariusHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    AquariusHoroscopeDetails['Year']=year
    AquariusHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(11).split("-")[1:])
    AquariusHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(11).split("-")[1:])
    AquariusHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(11).split("-")[1:])
    AquariusHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(11).split("-")[2:])
    AquariusHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(11).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/Horoscope/HoroscopeDetails.html',{'AquariusHoroscopeDetails':AquariusHoroscopeDetails})

def PiscesHoroscopeDetailView(request):
    PiscesHoroscopeDetails={}
    PiscesHoroscopeDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    PiscesHoroscopeDetails['Present_Date']=str(today_date)
    PiscesHoroscopeDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    PiscesHoroscopeDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    PiscesHoroscopeDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    PiscesHoroscopeDetails["Month_Details"]=str(today.strftime("%b, %Y"))
    PiscesHoroscopeDetails['Year']=year
    PiscesHoroscopeDetails['Yesterday_Description']=". ".join(YesterdayHoroscope(12).split("-")[1:])
    PiscesHoroscopeDetails['Today_Description']=". ".join(DailyHoroscope(12).split("-")[1:])
    PiscesHoroscopeDetails['Tomorrow_Description']=". ".join(TommorrowHoroscope(12).split("-")[1:])
    PiscesHoroscopeDetails['Weekly_Description']=". ".join(WeeklyHoroscope(12).split("-")[2:])
    PiscesHoroscopeDetails['Monthly_Description']=". ".join(MonthlyHoroscope(12).split("-")[1:])
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/Horoscope/HoroscopeDetails.html',{'PiscesHoroscopeDetails':PiscesHoroscopeDetails})

#Overview Details
def AriesZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[0]["Sign"].lower()
    AriesOverallDetails={}
    AriesOverallDetails['Year']=year
    AriesOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    AriesOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    AriesOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    AriesOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    AriesOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/AriesOverviewDetails.html',{'AriesOverallDetails':AriesOverallDetails})

def TaurusZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[1]["Sign"].lower()
    TaurusOverallDetails={}
    TaurusOverallDetails['Year']=year
    TaurusOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    TaurusOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    TaurusOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    TaurusOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    TaurusOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/TaurusOverviewDetails.html',{'TaurusOverallDetails':TaurusOverallDetails})

def GeminiZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[2]["Sign"].lower()
    GeminiOverallDetails={}
    GeminiOverallDetails['Year']=year
    GeminiOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    GeminiOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    GeminiOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    GeminiOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    GeminiOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/GeminiOverviewDetails.html',{'GeminiOverallDetails':GeminiOverallDetails})

def CancerZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[3]["Sign"].lower()
    CancerOverallDetails={}
    CancerOverallDetails['Year']=year
    CancerOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    CancerOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    CancerOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    CancerOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    CancerOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/CancerOverviewDetails.html',{'CancerOverallDetails':CancerOverallDetails})

def LeoZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[4]["Sign"].lower()
    LeoOverallDetails={}
    LeoOverallDetails['Year']=year
    LeoOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    LeoOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    LeoOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    LeoOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    LeoOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/LeoOverviewDetails.html',{'LeoOverallDetails':LeoOverallDetails})

def VirgoZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[5]["Sign"].lower()
    VirgoOverallDetails={}
    VirgoOverallDetails['Year']=year
    VirgoOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    VirgoOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    VirgoOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    VirgoOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    VirgoOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/VirgoOverviewDetails.html',{'VirgoOverallDetails':VirgoOverallDetails})

def LibraZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[6]["Sign"].lower()
    LibraOverallDetails={}
    LibraOverallDetails['Year']=year
    LibraOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    LibraOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    LibraOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    LibraOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    LibraOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/LibraOverviewDetails.html',{'LibraOverallDetails':LibraOverallDetails})

def ScorpioZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[7]["Sign"].lower()
    ScorpioOverallDetails={}
    ScorpioOverallDetails['Year']=year
    ScorpioOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    ScorpioOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    ScorpioOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    ScorpioOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    ScorpioOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/ScorpioOverviewDetails.html',{'ScorpioOverallDetails':ScorpioOverallDetails})

def SagittariusZodiacOverviewDetailView(request):
    Zodiac_Name='sagittarius'
    SagittariusOverallDetails={}
    SagittariusOverallDetails['Year']=year
    SagittariusOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    SagittariusOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    SagittariusOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    SagittariusOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    SagittariusOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/SagittariusOverviewDetails.html',{'SagittariusOverallDetails':SagittariusOverallDetails})

def CapricornZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[9]["Sign"].lower()
    CapricornOverallDetails={}
    CapricornOverallDetails['Year']=year
    CapricornOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    CapricornOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    CapricornOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    CapricornOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    CapricornOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/CapricornOverviewDetails.html',{'CapricornOverallDetails':CapricornOverallDetails})

def AquariusZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[10]["Sign"].lower()
    AquariusOverallDetails={}
    AquariusOverallDetails['Year']=year
    AquariusOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    AquariusOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    AquariusOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    AquariusOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    AquariusOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/AquariusOverviewDetails.html',{'AquariusOverallDetails':AquariusOverallDetails})

def PiscesZodiacOverviewDetailView(request):
    Zodiac_Name=Zodiac_carousel_Images[11]["Sign"].lower()
    PiscesOverallDetails={}
    PiscesOverallDetails['Year']=year
    PiscesOverallDetails['Zodiac_Sign_Name']=Zodiac_Name
    PiscesOverallDetails['Overview_Description'] = GetZodiacOverviewDetails(year, Zodiac_Name)
    PiscesOverallDetails['LoveCouples_Description'] = GetZodiacLoveCouplesOverallViewDetails(year,Zodiac_Name)
    PiscesOverallDetails['SingleLove_Description'] = GetZodiacLoveSinglesOverallViewDetails(year, Zodiac_Name)
    PiscesOverallDetails['CareerMoney_Description'] = GetZodiacCareerMoneyOverallViewDetails(year, Zodiac_Name)
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/PiscesOverviewDetails.html',{'PiscesOverallDetails':PiscesOverallDetails})

def AriesBasicZodiacDetailView(request):
    Aries_Details=Zodiac_carousel_Images[1]
    Aries_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/AriesZodiacBasicDetails.html',{'Aries_Details':Aries_Details})

def TaurusBasicZodiacDetailView(request):
    Taurus_Details=Zodiac_carousel_Images[1]
    Taurus_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/TaurusZodiacBasicDetails.html',{'Taurus_Details':Taurus_Details})

def GeminiBasicZodiacDetailView(request):
    Gemini_Details=Zodiac_carousel_Images[1]
    Gemini_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/GeminiZodiacBasicDetails.html',{'Gemini_Details':Gemini_Details})

def CancerBasicZodiacDetailView(request):
    Cancer_Details=Zodiac_carousel_Images[1]
    Cancer_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/CancerZodiacBasicDetails.html',{'Cancer_Details':Cancer_Details})

def LeoBasicZodiacDetailView(request):
    Leo_Details=Zodiac_carousel_Images[1]
    Leo_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/LeoZodiacBasicDetails.html',{'Leo_Details':Leo_Details})

def VirgoBasicZodiacDetailView(request):
    Virgo_Details=Zodiac_carousel_Images[1]
    Virgo_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/VirgoZodiacBasicDetails.html',{'Virgo_Details':Virgo_Details})

def LibraBasicZodiacDetailView(request):
    Libra_Details=Zodiac_carousel_Images[1]
    Libra_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/LibraZodiacBasicDetails.html',{'Libra_Details':Libra_Details})

def ScorpioBasicZodiacDetailView(request):
    Scorpio_Details=Zodiac_carousel_Images[1]
    Scorpio_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/ScorpioZodiacBasicDetails.html',{'Scorpio_Details':Scorpio_Details})

def SagittariusBasicZodiacDetailView(request):
    Sagittarius_Details=Zodiac_carousel_Images[1]
    Sagittarius_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/SagittariusZodiacBasicDetails.html',{'Sagittarius_Details':Sagittarius_Details})

def CapricornBasicZodiacDetailView(request):
    Capricorn_Details=Zodiac_carousel_Images[1]
    Capricorn_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/CapricornZodiacBasicDetails.html',{'Capricorn_Details':Capricorn_Details})

def AquariusBasicZodiacDetailView(request):
    Aquarius_Details=Zodiac_carousel_Images[1]
    Aquarius_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/AquariusZodiacBasicDetails.html',{'Aquarius_Details':Aquarius_Details})

def PiscesBasicZodiacDetailView(request):
    Pisces_Details=Zodiac_carousel_Images[1]
    Pisces_Details['Year']=year
    return render(request,'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/PiscesZodiacBasicDetails.html',{'Pisces_Details':Pisces_Details})

#CAREER DETAILS

def ZodiacCareerDetailView(request):
    return render(request,'MyZodiacSigns/Zodiac_Signs/ZodiacCareerDetail.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def AriesZodiacCareerDetailView(request):
    AriesCareerDetails={}
    AriesCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(1).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(1).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(1).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(1).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(1).split("-")[1:])
    AriesCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AriesCareerDetails['Present_Date']=str(today_date)
    AriesCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AriesCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AriesCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AriesCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    AriesCareerDetails['Yesterday_Description']=Yesterday_Desc
    AriesCareerDetails['Today_Description']=Today_Desc
    AriesCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    AriesCareerDetails['Weekly_Description']=Weekly_Desc
    AriesCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/Career/CareerDetails.html',{'AriesCareerDetails':AriesCareerDetails})

def TaurusZodiacCareerDetailView(request):
    TaurusCareerDetails={}
    TaurusCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(2).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(2).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(2).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(2).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(2).split("-")[1:])
    TaurusCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    TaurusCareerDetails['Present_Date']=str(today_date)
    TaurusCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    TaurusCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    TaurusCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    TaurusCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    TaurusCareerDetails['Yesterday_Description']=Yesterday_Desc
    TaurusCareerDetails['Today_Description']=Today_Desc
    TaurusCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    TaurusCareerDetails['Weekly_Description']=Weekly_Desc
    TaurusCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/Career/CareerDetails.html',{'TaurusCareerDetails':TaurusCareerDetails})

def GeminiZodiacCareerDetailView(request):
    GeminiCareerDetails={}
    GeminiCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(3).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(3).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(3).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(3).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(3).split("-")[1:])
    GeminiCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    GeminiCareerDetails['Present_Date']=str(today_date)
    GeminiCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    GeminiCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    GeminiCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    GeminiCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    GeminiCareerDetails['Yesterday_Description']=Yesterday_Desc
    GeminiCareerDetails['Today_Description']=Today_Desc
    GeminiCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    GeminiCareerDetails['Weekly_Description']=Weekly_Desc
    GeminiCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/Career/CareerDetails.html',{'GeminiCareerDetails':GeminiCareerDetails})

def CancerZodiacCareerDetailView(request):
    CancerCareerDetails={}
    CancerCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(4).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(4).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(4).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(4).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(4).split("-")[1:])
    CancerCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CancerCareerDetails['Present_Date']=str(today_date)
    CancerCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CancerCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CancerCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CancerCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    CancerCareerDetails['Yesterday_Description']=Yesterday_Desc
    CancerCareerDetails['Today_Description']=Today_Desc
    CancerCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    CancerCareerDetails['Weekly_Description']=Weekly_Desc
    CancerCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/Career/CareerDetails.html',{'CancerCareerDetails':CancerCareerDetails})

def LeoZodiacCareerDetailView(request):
    LeoCareerDetails={}
    LeoCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(5).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(5).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(5).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(5).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(5).split("-")[1:])
    LeoCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LeoCareerDetails['Present_Date']=str(today_date)
    LeoCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LeoCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LeoCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LeoCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    LeoCareerDetails['Yesterday_Description']=Yesterday_Desc
    LeoCareerDetails['Today_Description']=Today_Desc
    LeoCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    LeoCareerDetails['Weekly_Description']=Weekly_Desc
    LeoCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/Career/CareerDetails.html',{'LeoCareerDetails':LeoCareerDetails})

def VirgoZodiacCareerDetailView(request):
    VirgoCareerDetails={}
    VirgoCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(6).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(6).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(6).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(6).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(6).split("-")[1:])
    VirgoCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    VirgoCareerDetails['Present_Date']=str(today_date)
    VirgoCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    VirgoCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    VirgoCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    VirgoCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    VirgoCareerDetails['Yesterday_Description']=Yesterday_Desc
    VirgoCareerDetails['Today_Description']=Today_Desc
    VirgoCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    VirgoCareerDetails['Weekly_Description']=Weekly_Desc
    VirgoCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/Career/CareerDetails.html',{'VirgoCareerDetails':VirgoCareerDetails})

def LibraZodiacCareerDetailView(request):
    LibraCareerDetails={}
    LibraCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(7).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(7).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(7).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(7).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(7).split("-")[1:])
    LibraCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LibraCareerDetails['Present_Date']=str(today_date)
    LibraCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LibraCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LibraCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LibraCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    LibraCareerDetails['Yesterday_Description']=Yesterday_Desc
    LibraCareerDetails['Today_Description']=Today_Desc
    LibraCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    LibraCareerDetails['Weekly_Description']=Weekly_Desc
    LibraCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/Career/CareerDetails.html',{'LibraCareerDetails':LibraCareerDetails})

def ScorpioZodiacCareerDetailView(request):
    ScorpioCareerDetails={}
    ScorpioCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(8).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(8).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(8).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(8).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(8).split("-")[1:])
    ScorpioCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    ScorpioCareerDetails['Present_Date']=str(today_date)
    ScorpioCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    ScorpioCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    ScorpioCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    ScorpioCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    ScorpioCareerDetails['Yesterday_Description']=Yesterday_Desc
    ScorpioCareerDetails['Today_Description']=Today_Desc
    ScorpioCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    ScorpioCareerDetails['Weekly_Description']=Weekly_Desc
    ScorpioCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/Career/CareerDetails.html',{'ScorpioCareerDetails':ScorpioCareerDetails})

def SagittariusZodiacCareerDetailView(request):
    SagittariusCareerDetails={}
    SagittariusCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(9).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(9).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(9).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(9).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(9).split("-")[1:])
    SagittariusCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    SagittariusCareerDetails['Present_Date']=str(today_date)
    SagittariusCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    SagittariusCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    SagittariusCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    SagittariusCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    SagittariusCareerDetails['Yesterday_Description']=Yesterday_Desc
    SagittariusCareerDetails['Today_Description']=Today_Desc
    SagittariusCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    SagittariusCareerDetails['Weekly_Description']=Weekly_Desc
    SagittariusCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/Career/CareerDetails.html',{'SagittariusCareerDetails':SagittariusCareerDetails})

def CapricornZodiacCareerDetailView(request):
    CapricornCareerDetails={}
    CapricornCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(10).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(10).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(10).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(10).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(10).split("-")[1:])
    CapricornCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CapricornCareerDetails['Present_Date']=str(today_date)
    CapricornCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CapricornCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CapricornCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CapricornCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    CapricornCareerDetails['Yesterday_Description']=Yesterday_Desc
    CapricornCareerDetails['Today_Description']=Today_Desc
    CapricornCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    CapricornCareerDetails['Weekly_Description']=Weekly_Desc
    CapricornCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/Career/CareerDetails.html',{'CapricornCareerDetails':CapricornCareerDetails})

def AquariusZodiacCareerDetailView(request):
    AquariusCareerDetails={}
    AquariusCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(11).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(11).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(11).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(11).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(11).split("-")[1:])
    AquariusCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AquariusCareerDetails['Present_Date']=str(today_date)
    AquariusCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AquariusCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AquariusCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AquariusCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    AquariusCareerDetails['Yesterday_Description']=Yesterday_Desc
    AquariusCareerDetails['Today_Description']=Today_Desc
    AquariusCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    AquariusCareerDetails['Weekly_Description']=Weekly_Desc
    AquariusCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/Career/CareerDetails.html',{'AquariusCareerDetails':AquariusCareerDetails})

def PiscesZodiacCareerDetailView(request):
    PiscesCareerDetails={}
    PiscesCareerDetails["Year"]=year
    Yesterday_Desc=", ".join(GetYesterdayCareerHoroscopeDetails(12).split('-')[1:])
    Today_Desc=", ".join(GetTodayCareerHoroscopeDetails(12).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowCareerHoroscopeDetails(12).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyCareerHoroscopeDetails(12).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyCareerHoroscopeDetails(12).split("-")[1:])
    PiscesCareerDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    PiscesCareerDetails['Present_Date']=str(today_date)
    PiscesCareerDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    PiscesCareerDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    PiscesCareerDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    PiscesCareerDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    PiscesCareerDetails['Yesterday_Description']=Yesterday_Desc
    PiscesCareerDetails['Today_Description']=Today_Desc
    PiscesCareerDetails['Tomorrow_Description']=Tomorrow_Desc
    PiscesCareerDetails['Weekly_Description']=Weekly_Desc
    PiscesCareerDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/Career/CareerDetails.html',{'PiscesCareerDetails':PiscesCareerDetails})

def ZodiacHealthDetailView(request):
    return render(request,'MyZodiacSigns/Zodiac_Signs/ZodiacHealthDetails.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

# Health Details
def AriesZodiacHealthDetailView(request):
    AriesHealthDetails={}
    AriesHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(1).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(1).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(1).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(1).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(1).split("-")[1:])
    AriesHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AriesHealthDetails['Present_Date']=str(today_date)
    AriesHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AriesHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AriesHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AriesHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    AriesHealthDetails['Yesterday_Description']=Yesterday_Desc
    AriesHealthDetails['Today_Description']=Today_Desc
    AriesHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    AriesHealthDetails['Weekly_Description']=Weekly_Desc
    AriesHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/Health/HealthDetails.html',{'AriesHealthDetails':AriesHealthDetails})

def TaurusZodiacHealthDetailView(request):
    TaurusHealthDetails={}
    TaurusHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(2).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(2).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(2).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(2).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(2).split("-")[1:])
    TaurusHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    TaurusHealthDetails['Present_Date']=str(today_date)
    TaurusHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    TaurusHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    TaurusHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    TaurusHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    TaurusHealthDetails['Yesterday_Description']=Yesterday_Desc
    TaurusHealthDetails['Today_Description']=Today_Desc
    TaurusHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    TaurusHealthDetails['Weekly_Description']=Weekly_Desc
    TaurusHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/Health/HealthDetails.html',{'TaurusHealthDetails':TaurusHealthDetails})

def GeminiZodiacHealthDetailView(request):
    GeminiHealthDetails={}
    GeminiHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(3).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(3).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(3).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(3).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(3).split("-")[1:])
    GeminiHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    GeminiHealthDetails['Present_Date']=str(today_date)
    GeminiHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    GeminiHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    GeminiHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    GeminiHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    GeminiHealthDetails['Yesterday_Description']=Yesterday_Desc
    GeminiHealthDetails['Today_Description']=Today_Desc
    GeminiHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    GeminiHealthDetails['Weekly_Description']=Weekly_Desc
    GeminiHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/Health/HealthDetails.html',{'GeminiHealthDetails':GeminiHealthDetails})

def CancerZodiacHealthDetailView(request):
    CancerHealthDetails={}
    CancerHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(4).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(4).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(4).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(4).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(4).split("-")[1:])
    CancerHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CancerHealthDetails['Present_Date']=str(today_date)
    CancerHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CancerHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CancerHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CancerHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    CancerHealthDetails['Yesterday_Description']=Yesterday_Desc
    CancerHealthDetails['Today_Description']=Today_Desc
    CancerHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    CancerHealthDetails['Weekly_Description']=Weekly_Desc
    CancerHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/Health/HealthDetails.html',{'CancerHealthDetails':CancerHealthDetails})

def LeoZodiacHealthDetailView(request):
    LeoHealthDetails={}
    LeoHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(5).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(5).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(5).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(5).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(5).split("-")[1:])
    LeoHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LeoHealthDetails['Present_Date']=str(today_date)
    LeoHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LeoHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LeoHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LeoHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    LeoHealthDetails['Yesterday_Description']=Yesterday_Desc
    LeoHealthDetails['Today_Description']=Today_Desc
    LeoHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    LeoHealthDetails['Weekly_Description']=Weekly_Desc
    LeoHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/Health/HealthDetails.html',{'LeoHealthDetails':LeoHealthDetails})

def VirgoZodiacHealthDetailView(request):
    VirgoHealthDetails={}
    VirgoHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(6).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(6).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(6).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(6).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(6).split("-")[1:])
    VirgoHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    VirgoHealthDetails['Present_Date']=str(today_date)
    VirgoHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    VirgoHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    VirgoHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    VirgoHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    VirgoHealthDetails['Yesterday_Description']=Yesterday_Desc
    VirgoHealthDetails['Today_Description']=Today_Desc
    VirgoHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    VirgoHealthDetails['Weekly_Description']=Weekly_Desc
    VirgoHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/Health/HealthDetails.html',{'VirgoHealthDetails':VirgoHealthDetails})

def LibraZodiacHealthDetailView(request):
    LibraHealthDetails={}
    LibraHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(7).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(7).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(7).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(7).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(7).split("-")[1:])
    LibraHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LibraHealthDetails['Present_Date']=str(today_date)
    LibraHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LibraHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LibraHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LibraHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    LibraHealthDetails['Yesterday_Description']=Yesterday_Desc
    LibraHealthDetails['Today_Description']=Today_Desc
    LibraHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    LibraHealthDetails['Weekly_Description']=Weekly_Desc
    LibraHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/Health/HealthDetails.html',{'LibraHealthDetails':LibraHealthDetails})

def ScorpioZodiacHealthDetailView(request):
    ScorpioHealthDetails={}
    ScorpioHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(8).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(8).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(8).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(8).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(8).split("-")[1:])
    ScorpioHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    ScorpioHealthDetails['Present_Date']=str(today_date)
    ScorpioHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    ScorpioHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    ScorpioHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    ScorpioHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    ScorpioHealthDetails['Yesterday_Description']=Yesterday_Desc
    ScorpioHealthDetails['Today_Description']=Today_Desc
    ScorpioHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    ScorpioHealthDetails['Weekly_Description']=Weekly_Desc
    ScorpioHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/Health/HealthDetails.html',{'ScorpioHealthDetails':ScorpioHealthDetails})

def SagittariusZodiacHealthDetailView(request):
    SagittariusHealthDetails={}
    SagittariusHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(9).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(9).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(9).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(9).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(9).split("-")[1:])
    SagittariusHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    SagittariusHealthDetails['Present_Date']=str(today_date)
    SagittariusHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    SagittariusHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    SagittariusHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    SagittariusHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    SagittariusHealthDetails['Yesterday_Description']=Yesterday_Desc
    SagittariusHealthDetails['Today_Description']=Today_Desc
    SagittariusHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    SagittariusHealthDetails['Weekly_Description']=Weekly_Desc
    SagittariusHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/Health/HealthDetails.html',{'SagittariusHealthDetails':SagittariusHealthDetails})

def CapricornZodiacHealthDetailView(request):
    CapricornHealthDetails={}
    CapricornHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(10).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(10).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(10).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(10).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(10).split("-")[1:])
    CapricornHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CapricornHealthDetails['Present_Date']=str(today_date)
    CapricornHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CapricornHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CapricornHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CapricornHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    CapricornHealthDetails['Yesterday_Description']=Yesterday_Desc
    CapricornHealthDetails['Today_Description']=Today_Desc
    CapricornHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    CapricornHealthDetails['Weekly_Description']=Weekly_Desc
    CapricornHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/Health/HealthDetails.html',{'CapricornHealthDetails':CapricornHealthDetails})

def AquariusZodiacHealthDetailView(request):
    AquariusHealthDetails={}
    AquariusHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(11).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(11).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(11).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(11).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(11).split("-")[1:])
    AquariusHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AquariusHealthDetails['Present_Date']=str(today_date)
    AquariusHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AquariusHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AquariusHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AquariusHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    AquariusHealthDetails['Yesterday_Description']=Yesterday_Desc
    AquariusHealthDetails['Today_Description']=Today_Desc
    AquariusHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    AquariusHealthDetails['Weekly_Description']=Weekly_Desc
    AquariusHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/Health/HealthDetails.html',{'AquariusHealthDetails':AquariusHealthDetails})

def PiscesZodiacHealthDetailView(request):
    PiscesHealthDetails={}
    PiscesHealthDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayHealthHoroscopeDetails(12).split('-')[1:])
    Today_Desc=", ".join(GetTodayHealthHoroscopeDetails(12).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowHealthHoroscopeDetails(12).split("-")[1:])
    Weekly_Desc=", ".join(GetWeeklyHealthHoroscopeDetails(12).split("-")[2:])
    Monthly_Desc=", ".join(GetMonthlyHealthHoroscopeDetails(12).split("-")[1:])
    PiscesHealthDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    PiscesHealthDetails['Present_Date']=str(today_date)
    PiscesHealthDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    PiscesHealthDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    PiscesHealthDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    PiscesHealthDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    PiscesHealthDetails['Yesterday_Description']=Yesterday_Desc
    PiscesHealthDetails['Today_Description']=Today_Desc
    PiscesHealthDetails['Tomorrow_Description']=Tomorrow_Desc
    PiscesHealthDetails['Weekly_Description']=Weekly_Desc
    PiscesHealthDetails['Monthly_Description']=Monthly_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/Health/HealthDetails.html',{'PiscesHealthDetails':PiscesHealthDetails})

# Love Details
def ZodiacLoveDetailView(request):
    return render(request,'MyZodiacSigns/Zodiac_Signs/ZodiacLoveDetails.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def AriesZodiacLoveDetailView(request):
    AriesLoveDetails={}
    AriesLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(1).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(1).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(1).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(1).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(1).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(1).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(1).split('-')[1:])
    AriesLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AriesLoveDetails['Present_Date']=str(today_date)
    AriesLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AriesLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AriesLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AriesLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    AriesLoveDetails['Yesterday_Description']=Yesterday_Desc
    AriesLoveDetails['Today_Description']=Today_Desc
    AriesLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    AriesLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    AriesLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    AriesLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    AriesLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/Love/LoveDetails.html',{'AriesLoveDetails':AriesLoveDetails})

def TaurusZodiacLoveDetailView(request):
    TaurusLoveDetails={}
    TaurusLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(2).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(2).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(2).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(2).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(2).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(2).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(2).split('-')[1:])
    TaurusLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    TaurusLoveDetails['Present_Date']=str(today_date)
    TaurusLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    TaurusLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    TaurusLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    TaurusLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    TaurusLoveDetails['Yesterday_Description']=Yesterday_Desc
    TaurusLoveDetails['Today_Description']=Today_Desc
    TaurusLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    TaurusLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    TaurusLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    TaurusLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    TaurusLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/Love/LoveDetails.html',{'TaurusLoveDetails':TaurusLoveDetails})

def GeminiZodiacLoveDetailView(request):
    GeminiLoveDetails={}
    GeminiLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(3).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(3).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(3).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(3).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(3).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(3).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(3).split('-')[1:])
    GeminiLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    GeminiLoveDetails['Present_Date']=str(today_date)
    GeminiLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    GeminiLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    GeminiLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    GeminiLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    GeminiLoveDetails['Yesterday_Description']=Yesterday_Desc
    GeminiLoveDetails['Today_Description']=Today_Desc
    GeminiLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    GeminiLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    GeminiLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    GeminiLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    GeminiLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/Love/LoveDetails.html',{'GeminiLoveDetails':GeminiLoveDetails})

def CancerZodiacLoveDetailView(request):
    CancerLoveDetails={}
    CancerLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(4).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(4).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(4).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(4).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(4).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(4).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(4).split('-')[1:])
    CancerLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CancerLoveDetails['Present_Date']=str(today_date)
    CancerLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CancerLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CancerLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CancerLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    CancerLoveDetails['Yesterday_Description']=Yesterday_Desc
    CancerLoveDetails['Today_Description']=Today_Desc
    CancerLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    CancerLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    CancerLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    CancerLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    CancerLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/Love/LoveDetails.html',{'CancerLoveDetails':CancerLoveDetails})

def LeoZodiacLoveDetailView(request):
    LeoLoveDetails={}
    LeoLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(5).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(5).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(5).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(5).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(5).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(5).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(5).split('-')[1:])
    LeoLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LeoLoveDetails['Present_Date']=str(today_date)
    LeoLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LeoLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LeoLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LeoLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    LeoLoveDetails['Yesterday_Description']=Yesterday_Desc
    LeoLoveDetails['Today_Description']=Today_Desc
    LeoLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    LeoLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    LeoLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    LeoLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    LeoLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/Love/LoveDetails.html',{'LeoLoveDetails':LeoLoveDetails})

def VirgoZodiacLoveDetailView(request):
    VirgoLoveDetails={}
    VirgoLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(6).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(6).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(6).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(6).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(6).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(6).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(6).split('-')[1:])
    VirgoLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    VirgoLoveDetails['Present_Date']=str(today_date)
    VirgoLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    VirgoLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    VirgoLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    VirgoLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    VirgoLoveDetails['Yesterday_Description']=Yesterday_Desc
    VirgoLoveDetails['Today_Description']=Today_Desc
    VirgoLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    VirgoLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    VirgoLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    VirgoLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    VirgoLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/Love/LoveDetails.html',{'VirgoLoveDetails':VirgoLoveDetails})

def LibraZodiacLoveDetailView(request):
    LibraLoveDetails={}
    LibraLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(7).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(7).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(7).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(7).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(7).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(7).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(7).split('-')[1:])
    LibraLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    LibraLoveDetails['Present_Date']=str(today_date)
    LibraLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    LibraLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LibraLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LibraLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    LibraLoveDetails['Yesterday_Description']=Yesterday_Desc
    LibraLoveDetails['Today_Description']=Today_Desc
    LibraLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    LibraLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    LibraLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    LibraLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    LibraLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/Love/LoveDetails.html',{'LibraLoveDetails':LibraLoveDetails})

def ScorpioZodiacLoveDetailView(request):
    ScorpioLoveDetails={}
    ScorpioLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(8).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(8).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(8).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(8).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(8).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(8).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(8).split('-')[1:])
    ScorpioLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    ScorpioLoveDetails['Present_Date']=str(today_date)
    ScorpioLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    ScorpioLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    ScorpioLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    ScorpioLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    ScorpioLoveDetails['Yesterday_Description']=Yesterday_Desc
    ScorpioLoveDetails['Today_Description']=Today_Desc
    ScorpioLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    ScorpioLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    ScorpioLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    ScorpioLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    ScorpioLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/Love/LoveDetails.html',{'ScorpioLoveDetails':ScorpioLoveDetails})

def SagittariusZodiacLoveDetailView(request):
    SagittariusLoveDetails={}
    SagittariusLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(9).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(9).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(9).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(9).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(9).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(9).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(9).split('-')[1:])
    SagittariusLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    SagittariusLoveDetails['Present_Date']=str(today_date)
    SagittariusLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    SagittariusLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    SagittariusLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    SagittariusLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    SagittariusLoveDetails['Yesterday_Description']=Yesterday_Desc
    SagittariusLoveDetails['Today_Description']=Today_Desc
    SagittariusLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    SagittariusLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    SagittariusLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    SagittariusLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    SagittariusLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/Love/LoveDetails.html',{'SagittariusLoveDetails':SagittariusLoveDetails})

def CapricornZodiacLoveDetailView(request):
    CapricornLoveDetails={}
    CapricornLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(10).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(10).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(10).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(10).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(10).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(10).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(10).split('-')[1:])
    CapricornLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    CapricornLoveDetails['Present_Date']=str(today_date)
    CapricornLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    CapricornLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CapricornLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CapricornLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    CapricornLoveDetails['Yesterday_Description']=Yesterday_Desc
    CapricornLoveDetails['Today_Description']=Today_Desc
    CapricornLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    CapricornLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    CapricornLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    CapricornLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    CapricornLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/Love/LoveDetails.html',{'CapricornLoveDetails':CapricornLoveDetails})

def AquariusZodiacLoveDetailView(request):
    AquariusLoveDetails={}
    AquariusLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(11).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(11).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(11).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(11).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(11).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(11).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(11).split('-')[1:])
    AquariusLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    AquariusLoveDetails['Present_Date']=str(today_date)
    AquariusLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    AquariusLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AquariusLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AquariusLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    AquariusLoveDetails['Yesterday_Description']=Yesterday_Desc
    AquariusLoveDetails['Today_Description']=Today_Desc
    AquariusLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    AquariusLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    AquariusLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    AquariusLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    AquariusLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/Love/LoveDetails.html',{'AquariusLoveDetails':AquariusLoveDetails})

def PiscesZodiacLoveDetailView(request):
    PiscesLoveDetails={}
    PiscesLoveDetails['Year']=year
    Yesterday_Desc=", ".join(GetYesterdayLoveHoroscopeDetails(12).split('-')[1:])
    Today_Desc=", ".join(GetTodayLoveHoroscopeDetails(12).split("-")[1:])
    Tomorrow_Desc=", ".join(GetTomorrowLoveHoroscopeDetails(12).split("-")[1:])
    Weekly_Single_Desc=", ".join(GetWeeklySingleLoveHoroscopeDetails(12).split("-")[2:])
    Weekly_Couple_Desc=", ".join(GetWeeklyCoupleLoveHoroscopeDetails(12).split('-')[2:])
    Monthly_Single_Desc=", ".join(GetMonthlySingleLoveHoroscopeDetails(12).split('-')[1:])
    Monthly_Couple_Desc=", ".join(GetMonthlyCoupleLoveHoroscopeDetails(12).split('-')[1:])
    PiscesLoveDetails['Yesterday_Date']=str(yesterday_date.strftime("%d %b, %Y"))
    PiscesLoveDetails['Present_Date']=str(today_date)
    PiscesLoveDetails['Tomorrow_Date']=str(tomorrow_date.strftime("%d %b, %Y"))
    PiscesLoveDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    PiscesLoveDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    PiscesLoveDetails["Month_Details"]=str(tomorrow_date.strftime("%b, %Y"))
    PiscesLoveDetails['Yesterday_Description']=Yesterday_Desc
    PiscesLoveDetails['Today_Description']=Today_Desc
    PiscesLoveDetails['Tomorrow_Description']=Tomorrow_Desc
    PiscesLoveDetails['Weekly_Single_Description']=Weekly_Single_Desc
    PiscesLoveDetails['Weekly_Couple_Description']=Weekly_Couple_Desc
    PiscesLoveDetails['Monthly_Single_Description']=Monthly_Single_Desc
    PiscesLoveDetails['Monthly_Couple_Description']=Monthly_Couple_Desc
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/Love/LoveDetails.html',{'PiscesLoveDetails':PiscesLoveDetails})

def ZodiacMoneyDetailView(request):
    return render(request,'MyZodiacSigns/Zodiac_Signs/ZodiacMoneyDetails.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def AriesZodiacMoneyDetailView(request):
    AriesMoneyDetails={}
    AriesMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AriesMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AriesMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(1).split('-')[2:])
    AriesMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/Money/MoneyDetails.html', {'AriesMoneyDetails':AriesMoneyDetails})

def TaurusZodiacMoneyDetailView(request):
    TaurusMoneyDetails={}
    TaurusMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    TaurusMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    TaurusMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(2).split('-')[2:])
    TaurusMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/Money/MoneyDetails.html', {'TaurusMoneyDetails':TaurusMoneyDetails})

def GeminiZodiacMoneyDetailView(request):
    GeminiMoneyDetails={}
    GeminiMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    GeminiMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    GeminiMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(3).split('-')[2:])
    GeminiMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/Money/MoneyDetails.html', {'GeminiMoneyDetails':GeminiMoneyDetails})

def CancerZodiacMoneyDetailView(request):
    CancerMoneyDetails={}
    CancerMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CancerMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CancerMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(4).split('-')[2:])
    CancerMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/Money/MoneyDetails.html', {'CancerMoneyDetails':CancerMoneyDetails})

def LeoZodiacMoneyDetailView(request):
    LeoMoneyDetails={}
    LeoMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LeoMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LeoMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(5).split('-')[2:])
    LeoMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/Money/MoneyDetails.html', {'LeoMoneyDetails':LeoMoneyDetails})

def VirgoZodiacMoneyDetailView(request):
    VirgoMoneyDetails={}
    VirgoMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    VirgoMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    VirgoMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(6).split('-')[2:])
    VirgoMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/Money/MoneyDetails.html', {'VirgoMoneyDetails':VirgoMoneyDetails})

def LibraZodiacMoneyDetailView(request):
    LibraMoneyDetails={}
    LibraMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LibraMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LibraMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(7).split('-')[2:])
    LibraMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/Money/MoneyDetails.html', {'LibraMoneyDetails':LibraMoneyDetails})

def ScorpioZodiacMoneyDetailView(request):
    ScorpioMoneyDetails={}
    ScorpioMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    ScorpioMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    ScorpioMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(8).split('-')[2:])
    ScorpioMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/Money/MoneyDetails.html', {'ScorpioMoneyDetails':ScorpioMoneyDetails})

def SagittariusZodiacMoneyDetailView(request):
    SagittariusMoneyDetails={}
    SagittariusMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    SagittariusMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    SagittariusMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(9).split('-')[2:])
    SagittariusMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/Money/MoneyDetails.html', {'SagittariusMoneyDetails':SagittariusMoneyDetails})

def CapricornZodiacMoneyDetailView(request):
    CapricornMoneyDetails={}
    CapricornMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CapricornMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CapricornMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(10).split('-')[2:])
    CapricornMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/Money/MoneyDetails.html', {'CapricornMoneyDetails':CapricornMoneyDetails})

def AquariusZodiacMoneyDetailView(request):
    AquariusMoneyDetails={}
    AquariusMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AquariusMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AquariusMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(11).split('-')[2:])
    AquariusMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/Money/MoneyDetails.html', {'AquariusMoneyDetails':AquariusMoneyDetails})

def PiscesZodiacMoneyDetailView(request):
    PiscesMoneyDetails={}
    PiscesMoneyDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    PiscesMoneyDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    PiscesMoneyDetails['Weekly_Description']=", ".join(GetWeeklyMoneyHoroscopeDetails(12).split('-')[2:])
    PiscesMoneyDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/Money/MoneyDetails.html', {'PiscesMoneyDetails':PiscesMoneyDetails})

def ZodiacRetailDetailView(request):
    return render(request,'MyZodiacSigns/Zodiac_Signs/ZodiacRetailDetails.html',{'Zodiac_carousel_Images':Zodiac_carousel_Images})

def AriesZodiacRetailDetailView(request):
    AriesRetailDetails={}
    AriesRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AriesRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AriesRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(1).split('-')[2:])
    AriesRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aries_Zodiac/Retail/RetailDetails.html', {'AriesRetailDetails':AriesRetailDetails})

def TaurusZodiacRetailDetailView(request):
    TaurusRetailDetails={}
    TaurusRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    TaurusRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    TaurusRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(2).split('-')[2:])
    TaurusRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Taurus_Zodiac/Retail/RetailDetails.html', {'TaurusRetailDetails':TaurusRetailDetails})

def GeminiZodiacRetailDetailView(request):
    GeminiRetailDetails={}
    GeminiRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    GeminiRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    GeminiRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(3).split('-')[2:])
    GeminiRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Gemini_Zodiac/Retail/RetailDetails.html', {'GeminiRetailDetails':GeminiRetailDetails})

def CancerZodiacRetailDetailView(request):
    CancerRetailDetails={}
    CancerRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CancerRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CancerRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(4).split('-')[2:])
    CancerRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Cancer_Zodiac/Retail/RetailDetails.html', {'CancerRetailDetails':CancerRetailDetails})

def LeoZodiacRetailDetailView(request):
    LeoRetailDetails={}
    LeoRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LeoRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LeoRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(5).split('-')[2:])
    LeoRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Leo_Zodiac/Retail/RetailDetails.html', {'LeoRetailDetails':LeoRetailDetails})

def VirgoZodiacRetailDetailView(request):
    VirgoRetailDetails={}
    VirgoRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    VirgoRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    VirgoRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(6).split('-')[2:])
    VirgoRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Virgo_Zodiac/Retail/RetailDetails.html', {'VirgoRetailDetails':VirgoRetailDetails})

def LibraZodiacRetailDetailView(request):
    LibraRetailDetails={}
    LibraRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    LibraRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    LibraRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(7).split('-')[2:])
    LibraRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Libra_Zodiac/Retail/RetailDetails.html', {'LibraRetailDetails':LibraRetailDetails})

def ScorpioZodiacRetailDetailView(request):
    ScorpioRetailDetails={}
    ScorpioRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    ScorpioRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    ScorpioRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(8).split('-')[2:])
    ScorpioRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Scorpio_Zodiac/Retail/RetailDetails.html', {'ScorpioRetailDetails':ScorpioRetailDetails})

def SagittariusZodiacRetailDetailView(request):
    SagittariusRetailDetails={}
    SagittariusRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    SagittariusRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    SagittariusRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(9).split('-')[2:])
    SagittariusRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Sagittarius_Zodiac/Retail/RetailDetails.html', {'SagittariusRetailDetails':SagittariusRetailDetails})

def CapricornZodiacRetailDetailView(request):
    CapricornRetailDetails={}
    CapricornRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    CapricornRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    CapricornRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(10).split('-')[2:])
    CapricornRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Capricorn_Zodiac/Retail/RetailDetails.html', {'CapricornRetailDetails':CapricornRetailDetails})

def AquariusZodiacRetailDetailView(request):
    AquariusRetailDetails={}
    AquariusRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    AquariusRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    AquariusRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(11).split('-')[2:])
    AquariusRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Aquarius_Zodiac/Retail/RetailDetails.html', {'AquariusRetailDetails':AquariusRetailDetails})

def PiscesZodiacRetailDetailView(request):
    PiscesRetailDetails={}
    PiscesRetailDetails["start_week_date"]=str(start_day_date().strftime("%d %b, %Y"))
    PiscesRetailDetails["end_week_date"]=str(end_day_date().strftime("%d %b, %Y"))
    PiscesRetailDetails['Weekly_Description']=", ".join(GetWeeklyRetailHoroscopeDetails(12).split('-')[2:])
    PiscesRetailDetails['Year']=str(today.strftime("%Y"))
    return render(request, 'MyZodiacSigns/Zodiac_Signs/Pisces_Zodiac/Retail/RetailDetails.html', {'PiscesRetailDetails':PiscesRetailDetails})
