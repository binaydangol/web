from django.shortcuts import render
from . import views
from bs4 import BeautifulSoup
import json
import requests
import time
# import urllib.request
import urllib.request
from webscrap.models import Coronacases



# Create your views here.
def home(request):
    API_KEY = "jlBPGH4VHh1kMxWmn3IL1LRoOCW5o3yJ"
    if request.method == 'POST':
        CountryCode = request.POST['countryid']
        c = request.POST['cityname']
        city = c.replace(" ", "")
        loc = get_location(CountryCode, city, API_KEY)
        forecast = get_forecast(loc, API_KEY)
        daily_detail = {}
        k = 0
        apilink = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + loc + "?apikey=" + API_KEY + "&details=true"
        for key1 in forecast['DailyForecasts']:
            k = k + 1
            temp = {}
            temp_min = key1['Temperature']['Minimum']['Value']
            temp_max = key1['Temperature']['Maximum']['Value']
            daytype = key1['Day']['IconPhrase']
            daylong = key1['Day']['LongPhrase']

            dt = key1['Date']
            temp['max'] = temp_max
            temp['min'] = temp_min
            temp['daytype'] = daytype
            temp['daylong'] = daylong
            date = dt[0:10]
            temp['date'] = date
            key_gen = "day " + str(k)
            daily_detail[key_gen] = temp

        daily_report = daily_detail['day 1']
        context = {
            'MaxTemp': daily_detail['day 1']['max'],
            'MinTemp': daily_detail['day 1']['min'],
            'daytype': daily_detail['day 1']['daytype'],
            'daylong': daily_detail['day 1']['daylong'],
            'date': daily_detail['day 1']['date'],
            'place_name': "Temperature Detail For :  " + c

        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', {'place_name': ""})


def get_location(CountryCode, city, API_KEY):
    if CountryCode == "":
        search_address = "http://dataservice.accuweather.com/locations/v1/cities/search?apikey=" + API_KEY + "&q=" + city + "&details=true"
    else:
        search_address = "http://dataservice.accuweather.com/locations/v1/cities/" + CountryCode + "/search?apikey=" + API_KEY + "&q=" + city + "&details=true"

    with urllib.request.urlopen(search_address) as search_address:
        data = json.loads(search_address.read().decode())
    location_key = data[0]['Key']

    return location_key


def get_forecast(location_key, API_KEY):
    forecast_key = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + location_key + "?apikey=" + API_KEY + "&details=true"
    with urllib.request.urlopen(forecast_key) as forecast_key:
        data = json.loads(forecast_key.read().decode())
    return data


def corona_info(request):
    url = BeautifulSoup('https://www.worldometers.info/coronavirus/', "html.parser")
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, "html")
    wrf_dict = world_record(soup)
    wrf_detail_dict = world_detail(soup)
    country_detail = country_details(soup)
    temp_dict1 = {}
    delIns = Coronacases.objects.all()
    delIns.delete()

    for b in range(1, len(country_detail)):
        # for a in range(1):
        uC = Coronacases.objects.create(
            Index=country_detail[b]['Index'],
            Country_Name=country_detail[b]['Country Name'],
            Total_Cases=country_detail[b]['Total Cases'],
            New_Cases=country_detail[b]['New Cases'],
            Deaths_Per_Country=country_detail[b]['Total Deaths'],
            New_Death=country_detail[b]['New Deaths'],
            Total_Recovered=country_detail[b]['Total Recovered'],
            Active_Cases=country_detail[b]['Active Cases'],
            Serious_and_Critical=country_detail[b]['Serious Critical'],
            Cases_Per_Million=country_detail[b]['Total Cases Per Million'],
            Death_Per_Millions=country_detail[b]['Deaths Per Million'],
            Total_Tests=country_detail[b]['Total Tests'],
            Tests_Per_Millions=country_detail[b]['Tests Per Million'],
            Total_Population=country_detail[b]['Population'],
        )
        uC.save()

        # mer = {**country, **cases}
        # print(mer)
        # temp_dict1[b] = country

    summary = {
        'case': wrf_dict['Coronavirus Cases'],
        'death': wrf_dict['Deaths'],
        'recover': wrf_dict['Recovered'],
        'wd': wrf_detail_dict,
        'cip': wrf_detail_dict['Currently Infected Patients'],
        'imc': wrf_detail_dict['in Mild Condition'],
        'soc': wrf_detail_dict['Serious or Critical'],
        'cwhao': wrf_detail_dict['Cases which had an outcome:'],
        'rd': wrf_detail_dict['Recovered / Discharged'],
        'd': wrf_detail_dict['Deaths'],
        'contryDet': Coronacases.objects.all(),
    }

    return render(request, 'corona_info.html', summary)


def world_detail(soup):
    wrd_cnt = soup.findAll("div", {"class": "panel_front"})
    wd = []
    for w in wrd_cnt:
        wd.append(w.get_text())

    world_d = []
    for w_str in wd:
        f = w_str.replace("\n\n", "-")
        final_str1 = f.replace("\n", "=")
        final_str11 = final_str1.replace("Graph", "")
        final_str = final_str11.replace("Show", "")
        world_d.append(final_str)
    li = []
    for x in world_d:
        listss = x.split("-")
        li.append(listss)
    list_f = []

    for d1 in li:
        d1.remove("= =")
        for ax in d1:
            d_temp = ax.split("=")
            list_f.append(d_temp)
    culter_list = []
    for i in list_f:
        for gg in i:
            if gg == '':
                i.remove('')
        culter_list.append(i)

    dict = {}
    for temp in culter_list:
        dict[temp[-1]] = temp[0]

    return dict


def world_record(soup):
    wrd_cnt = soup.findAll("div", {"id": "maincounter-wrap"})

    world = []
    for w in wrd_cnt:
        world.append(w.get_text())

    # removing \n from the scrapped text
    world_record = []
    for w_str in world:
        final_str = w_str.replace("\n", "")
        world_record.append(final_str)
    wrf_final = []

    # converting to dictionary
    for wd in world_record:
        x = wd.split(":")
        wrf_final.append(x)
    wrf_dict = {}
    for a in wrf_final:
        wrf_dict[a[0]] = a[1]

    return wrf_dict


def country_details(soup):
    headings = soup.table.thead.tr
    headings = headings.find_all('th')
    tbody = soup.table.tbody
    bodys = tbody.find_all('tr')
    b = []

    for body in bodys:
        b.append(body.get_text())

    world_record = []
    for w_str in b:
        final_str1 = w_str.split("\n")
        world_record.append(final_str1)

    index_world_record = []
    index_world_record = world_record

    for ind in world_record:
        del ind[0]
        del ind[-1]
        del ind[-1]

    headings = soup.table.thead.tr
    headings = headings.find_all('th')
    head = []
    for h in headings:
        head.append(h.get_text())
    contex_f = {}
    for con in range(8, len(world_record)):
        contex = {
            'Index': world_record[con][0],
            'Country Name': world_record[con][1],
            'Total Cases': world_record[con][2],
            'New Cases': world_record[con][3],
            'Total Deaths': world_record[con][4],
            'New Deaths': world_record[con][5],
            'Total Recovered': world_record[con][6],
            'Active Cases': world_record[con][7],
            'Serious Critical': world_record[con][8],
            'Total Cases Per Million': world_record[con][9],
            'Deaths Per Million': world_record[con][10],
            'Total Tests': world_record[con][11],
            'Tests Per Million': world_record[con][12],
            'Population': world_record[con][13],
            # 'country': world_record[8:],

        }
        contex_f[con - 7] = contex

        # # 'head': l_f,
    # (contex_f)

    return contex_f
