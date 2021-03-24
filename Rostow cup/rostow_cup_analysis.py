import pandas as pd
import country_data as cod
def get_country_names():
    country_list_file = open("country_list.txt", "r")
    country_list = []
    for country in country_list_file:
        country = country.rstrip("\n")
        #removes empty lines from the list of countries
        if country != '':
            country_list.append(country)
    return(country_list)

def get_header_string(year):
    return(str(year) + " " + "[YR" + str(year) + "]")

def string_is_number(string):
    try:
        float(string)
        return(True)
    except ValueError:
        return(False)

def get_most_recent_year_data_in_dict(dictionary, start_year):
    for i in range(2020, start_year, -1):
        data = dictionary[get_header_string(i)]
        if(string_is_number(data)):
            return float(data)
    return("Data not found.")

def get_country_population_and_economic_data(country_name, start_index, dicts):
    data_names = ["GNI per capita, PPP (constant 2017 international $)", "Life expectancy at birth, total (years)", "Urban population (% of total population)", "Mortality rate, infant (per 1,000 live births)", "Birth rate, crude (per 1,000 people)", "Death rate, crude (per 1,000 people)", "Fertility rate, total (births per woman)"]
    data = []
    i = 0
    for data_name in data_names:
        data.append(get_most_recent_year_data_in_dict(dicts[i + start_index], 2016))
        i += 1
    return(data)

def get_country_education_data(country_name, dictionary):
    return(get_most_recent_year_data_in_dict(dictionary, 2014))

def get_country_dict_list_index_from_name(name, dicts):
    index = 0
    for d in dicts:
        if d["Country Name"] == name:
            return index
        index += 1
    print("name not found: " + name)

def get_country_data_objects(population_and_economic_dicts, education_dicts):
    country_list = get_country_names()
    countries = []
    for country in country_list:
        country_data_params = [country]
        country_population_and_economic_data = get_country_population_and_economic_data(country, get_country_dict_list_index_from_name(country, population_and_economic_dicts), population_and_economic_dicts)
        for data in country_population_and_economic_data:
            country_data_params.append(data)
        country_data_params.append(get_country_education_data(country, education_dicts[get_country_dict_list_index_from_name(country, education_dicts)]))
        country = cod.Country_data(*country_data_params)
        countries.append(country)
    return countries
    
def update_country_data_win_percentages(country_data_objects):
    for data in country_data_objects:
        data.win_percentage = data.wins / (len(country_data_objects) - 1)
    return country_data_objects

def countries_compete(country_data_objects):
    for i in range(len(country_data_objects)):
        for j in range(len(country_data_objects)):
            country_data_objects[i].update_wins(country_data_objects[j])
    country_data_objects = update_country_data_win_percentages(country_data_objects)
    return country_data_objects

def get_country_data_object_text(data):
    return data.name + " " + str(data.win_percentage)

def text_found(file_name, search):
    with open(file_name, 'r') as f:
        for line in f:
            if search in line:
                return True
    return False

def get_country_groups_dict(country_data_objects):
    files = ["africa_countries.txt", "asia_countries.txt", "europe_countries.txt", "flex_countries.txt", "latin_america_countries.txt"]
    groups = []
    group_names = ["Africa", "Asia", "Europe", "Flex", "Latin America"]
    for f in files:
        countries = []
        for d in country_data_objects:
            if(text_found(f, d.name)):
                countries.append(get_country_data_object_text(d))
        groups.append(countries)
    group_dict = {
        "names": group_names,
        "country data": groups
    }
    return group_dict

def write_list_to_file(text_file, country_list, name):
    text_file.write(name + "\n")
    for l in country_list:
        text_file.write(l + "\n")

def create_country_groups_text_document(file_name, dictionary):
    f = open(file_name, "a")
    i = 0
    for country in dictionary["country data"]:
        write_list_to_file(f, country, dictionary["names"][i])
        i += 1



population_and_economic_data = pd.read_csv("population_and_economic_data.csv")
population_and_economic_dicts = population_and_economic_data.to_dict("records")
education_data = pd.read_csv("education_data.csv")
education_dicts = education_data.to_dict("records")
country_data_objects = get_country_data_objects(population_and_economic_dicts, education_dicts)
country_data_objects = countries_compete(country_data_objects)
country_data_objects.sort(key=lambda x: x.win_percentage, reverse=True)
country_groups_dict = get_country_groups_dict(country_data_objects)
create_country_groups_text_document("result.txt", country_groups_dict)