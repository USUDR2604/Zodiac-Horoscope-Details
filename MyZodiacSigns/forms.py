from numbers import Number
from django import forms
Zodiacs=(("Aries","Aries"),("Taurus","Taurus"),("Gemini","Gemini"),("Cancer","Cancer"),("Leo","Leo"),("Virgo","Virgo"),
("Libra","Libra"),("Scorpio","Scorpio"),("Sagittarius","Sagittarius"),("Capricorn","Capricorn"),("Aquarius","Aquarius"),("Pisces","Pisces"))
Months=(("January","January"),("February","February"),("March","March"),("April","April"),("May","May"),("June","June"),
("July","July"),("August","August"),("September","September"),("October","October"),("November","Novemeber"),("December","December"))
# creating a form
class ZodiacFindingDetailForm(forms.Form):
	person_name = forms.CharField(label='What is your name:',max_length=50,help_text="Please enter your full name")
	Age = forms.IntegerField(max_value=100,label="Enter your Age:",help_text="Please check enter your age and check it should be below 100 in general.")
	birth_date = forms.DateField(label='What is your birth date:', help_text="Please enter your correct birthdate",widget=forms.NumberInput(attrs={'type':'date'}))

class ZodiacLoveCompatibilityForm(forms.Form):
	First_Zodiac_Sign = forms.ChoiceField(widget=forms.Select, choices=Zodiacs,label="Enter your zodiac sign")
	Second_Zodiac_Sign = forms.ChoiceField(widget=forms.Select, choices=Zodiacs,label="Enter your Partner zodiac sign")

class BirthDateDetailForm(forms.Form):
	person_name = forms.CharField(label='What is your name?',max_length=50,help_text='Please enter your name')
	Birth_Date = forms.ChoiceField(widget=forms.Select,choices=[(x,x) for x in range(1,32)],help_text="Enter your birthday Date",label="Enter your Birthday Date:")
	Birth_Month = forms.ChoiceField(widget=forms.Select,choices= Months,help_text="Enter your birthday Date",label="Enter your Birthday Month:")