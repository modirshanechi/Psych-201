import numpy as np
import pandas as pd
import math


def randomized_choice_options(num_choices):
    choice_options = list(map(chr, range(65, 91)))
    return np.random.choice(choice_options, num_choices, replace=False)

def standardize_degree(degree):
    mapping = {
        "high school": "High School",
        "high school graduate": "High School",
        "less than high school": "Less than High School",
        "less than high school degree": "Less than High School",
        "primary ed.": "Less than High School",
        "primary": "Less than High School",
        "secondary ed.": "High School",
        "secondary": "High School",
        "some college": "College",
        "some college but no degree": "College",
        "some-college": "College",
        "associate degree": "Associate Degree",
        "associate degree in college (2-year)": "Associate Degree",
        "bachelor": "Bachelor's Degree",
        "bachelor degree": "Bachelor's Degree",
        "bachelor's degree in college (4-year)": "Bachelor's Degree",
        "college-completed": "Bachelor's Degree",
        "university degree": "Bachelor's Degree",
        "grad": "Master's Degree or Higher",
        "graduate": "Master's Degree or Higher",
        "master degree or higher": "Master's Degree or Higher",
        "master's degree": "Master's Degree or Higher",
        "master": "Master's Degree or Higher",
        "mba": "Master's Degree or Higher",
        "advanced degree (ma, phd, etc)": "Master's Degree or Higher",
        "doctoral degree": "Master's Degree or Higher",
        "phd": "Master's Degree or Higher",
        "professional degree (jd, md)": "Professional Degree",
        "technical ed.": "Technical Education",
        "school (a-levels, vocational, or similar)": "Technical Education",
        "school (gcse or similar)": "High School",
        "no formal ed.": "No Formal Education",
        "none": "No Formal Education",
        "rather not say": "N/A"
    }
    
    return mapping.get(degree.lower(), "N/A")

def standardize_nationalities(nationality):
    # Mapping redundant nationalities to a standard format
    merge_map = {
        "USA": "United States",
        "Basel": "Switzerland",
        "Berlin": "Germany",
        "United States": "United States",
        "Russian Federation": "Russia",
        "Czech Republic": "Czechia",
        "England": "United Kingdom",
        "Scotland": "United Kingdom",
        "Wales": "United Kingdom",
        "Northern Ireland": "United Kingdom",
        "United Kingdom": "United Kingdom",
        "Bangladeshi": "Bangladesh",
        "Pakistani": "Pakistan",
        "Indian": "India",
        "Chinese": "China",
        "South Korea": "Korea",
        "Saint Vincent and the Grenadines": "Saint Vincent",
        "Venezuela, Bolivarian Republic of": "Venezuela",
        # ISO alpha-3 abbreviations
        "AFG": "Afghanistan",
        "AGO": "Angola",
        "ALA": "Åland Islands",
        "ALB": "Albania",
        "ARE": "United Arab Emirates",
        "ARG": "Argentina",
        "ARM": "Armenia",
        "ATG": "Antigua and Barbuda",
        "AUS": "Australia",
        "AUT": "Austria",
        "AZE": "Azerbaijan",
        "BEL": "Belgium",
        "BGD": "Bangladesh",
        "BGR": "Bulgaria",
        "BHR": "Bahrain",
        "BHS": "Bahamas",
        "BIH": "Bosnia and Herzegovina",
        "BLR": "Belarus",
        "BLZ": "Belize",
        "BMU": "Bermuda",
        "BOL": "Bolivia",
        "BRA": "Brazil",
        "BRN": "Brunei",
        "BWA": "Botswana",
        "CAN": "Canada",
        "CHE": "Switzerland",
        "CHL": "Chile",
        "CHN": "China",
        "CIV": "Côte d'Ivoire",
        "COL": "Colombia",
        "CPV": "Cape Verde",
        "CRI": "Costa Rica",
        "CUB": "Cuba",
        "CYP": "Cyprus",
        "CZE": "Czechia",
        "DEU": "Germany",
        "DNK": "Denmark",
        "DOM": "Dominican Republic",
        "DZA": "Algeria",
        "ECU": "Ecuador",
        "EGY": "Egypt",
        "ESP": "Spain",
        "EST": "Estonia",
        "FIN": "Finland",
        "FJI": "Fiji",
        "FRA": "France",
        "GBR": "United Kingdom",
        "GEO": "Georgia",
        "GGY": "Guernsey",
        "GHA": "Ghana",
        "GIB": "Gibraltar",
        "GLP": "Guadeloupe",
        "GRC": "Greece",
        "GTM": "Guatemala",
        "GUF": "French Guiana",
        "HKG": "Hong Kong",
        "HND": "Honduras",
        "HRV": "Croatia",
        "HUN": "Hungary",
        "IDN": "Indonesia",
        "IMN": "Isle of Man",
        "IND": "India",
        "IRL": "Ireland",
        "IRN": "Iran",
        "IRQ": "Iraq",
        "ISL": "Iceland",
        "ISR": "Israel",
        "ITA": "Italy",
        "JAM": "Jamaica",
        "JEY": "Jersey",
        "JOR": "Jordan",
        "JPN": "Japan",
        "KAZ": "Kazakhstan",
        "KEN": "Kenya",
        "KGZ": "Kyrgyzstan",
        "KHM": "Cambodia",
        "KOR": "Korea",
        "KWT": "Kuwait",
        "LAO": "Laos",
        "LBN": "Lebanon",
        "LIE": "Liechtenstein",
        "LKA": "Sri Lanka",
        "LTU": "Lithuania",
        "LUX": "Luxembourg",
        "LVA": "Latvia",
        "MAC": "Macau",
        "MAR": "Morocco",
        "MCO": "Monaco",
        "MDA": "Moldova",
        "MDG": "Madagascar",
        "MDV": "Maldives",
        "MEX": "Mexico",
        "MKD": "North Macedonia",
        "MLT": "Malta",
        "MMR": "Myanmar",
        "MNE": "Montenegro",
        "MNG": "Mongolia",
        "MTQ": "Martinique",
        "MUS": "Mauritius",
        "MYS": "Malaysia",
        "MYT": "Mayotte",
        "NCL": "New Caledonia",
        "NGA": "Nigeria",
        "NIC": "Nicaragua",
        "NLD": "Netherlands",
        "NOR": "Norway",
        "NPL": "Nepal",
        "NZL": "New Zealand",
        "OMN": "Oman",
        "PAK": "Pakistan",
        "PAN": "Panama",
        "PER": "Peru",
        "PHL": "Philippines",
        "PNG": "Papua New Guinea",
        "POL": "Poland",
        "PRI": "Puerto Rico",
        "PRT": "Portugal",
        "PRY": "Paraguay",
        "PSE": "Palestine",
        "PYF": "French Polynesia",
        "QAT": "Qatar",
        "REU": "Réunion",
        "ROU": "Romania",
        "RUS": "Russia",
        "SAU": "Saudi Arabia",
        "SDN": "Sudan",
        "SEN": "Senegal",
        "SGP": "Singapore",
        "SLV": "El Salvador",
        "SRB": "Serbia",
        "SVK": "Slovakia",
        "SVN": "Slovenia",
        "SWE": "Sweden",
        "SXM": "Sint Maarten",
        "SYR": "Syria",
        "THA": "Thailand",
        "TJK": "Tajikistan",
        "TTO": "Trinidad and Tobago",
        "TUN": "Tunisia",
        "TUR": "Turkey",
        "TWN": "Taiwan",
        "TZA": "Tanzania",
        "UKR": "Ukraine",
        "URY": "Uruguay",
        "UZB": "Uzbekistan",
        "VEN": "Venezuela",
        "VNM": "Vietnam",
        "YEM": "Yemen",
        "ZAF": "South Africa",
        "ZWE": "Zimbabwe"
    }

    # List of known nationalities (ISO country names as reference)
    valid_nationalities = {
        "Algeria", "Argentina", "Australia", "Austria", "Bangladesh", "Belgium",
        "Bosnia and Herzegovina", "Brazil", "Bulgaria", "Canada", "Chile", "China",
        "Croatia", "Cyprus", "Czechia", "Denmark", "Egypt", "Estonia", "Ethiopia",
        "France", "Georgia", "Germany", "Ghana", "Greece", "Hungary", "India",
        "Indonesia", "Iran", "Ireland", "Israel", "Italy", "Japan", "Jordan",
        "Kazakhstan", "Kenya", "Korea", "Latvia", "Lebanon", "Libya", "Lithuania",
        "Malaysia", "Mauritius", "Mexico", "Moldova", "Montenegro", "Morocco",
        "Nepal", "Netherlands", "New Zealand", "Nigeria", "North Macedonia",
        "Norway", "Pakistan", "Panama", "Paraguay", "Peru", "Philippines", "Poland",
        "Portugal", "Puerto Rico", "Romania", "Russia", "Serbia", "Singapore",
        "Slovakia", "Slovenia", "South Africa", "Spain", "Sri Lanka", "Sweden",
        "Switzerland", "Turkey", "United States", "Uganda", "Ukraine",
        "United Kingdom", "Uruguay", "Venezuela", "Vietnam", "Yemen", "Zimbabwe"
    }

    # Function to standardize a single nationality
    def standardize(nat):
        if nat in merge_map:
            return merge_map[nat]
        elif nat in valid_nationalities:
            return nat
        else:
            return 'N/A'

    # Apply transformation to the list
    return standardize(nationality)


def safe_cast_to_age(value):
    try:
        value = float(value)
        if value < 0:
            return 'N/A'
        if value > 100:
            return 'N/A'
        if math.isnan(value):
            return 'N/A'
        return str(value)
    except (ValueError, TypeError):
        return 'N/A'
    
def safe_cast_to_int(value):
    try:
        value = int(value)
        if math.isnan(value):
            return 'N/A'
        return str(value)
    except (ValueError, TypeError):
        return 'N/A'

def safe_cast_to_float_array(value): 
    return pd.to_numeric(value, errors='coerce').astype(float).tolist()

def cast_to_nationality(value):
    value = str(value).replace('Other ', '')
    value = str(value).replace("\"", "").replace(" (please specify)", "")
    if (value == 'nan') or (value == 'Unknown'):
        return 'N/A'
    value = str(value).replace('_', ' ')
    value = standardize_nationalities(value)
    return value

def cast_to_education(value):
    value = standardize_degree(value)
    if value == 'nan':
        return 'N/A'
    return value

def cast_to_gender(value):
    if value == 'nan':
        return 'N/A'
    
    if value == 'Female':
        return 'female'
    if value == 'F':
        return 'female'
    if value == 'Woman':
        return 'female' 

    if value == 'Male':
        return 'male'
    if value == 'M':
        return 'male'
    if value == 'Man':
        return 'male'
    
    if value == 'NB':
        return 'other'
    if value == 'Other':
        return 'other'

    if value == 'no-specify':
        return 'N/A'
    if value == 'no-spe':
        return 'N/A'
    if value == 'Prefer not to answer':
        return 'N/A'
    if value == 'Prefer not to say':
        return 'N/A'
    if value == 'Rather not say':
        return 'N/A'
    
    
    return value

def cast_to_diagnosis(value):
    if value == 'Healthy':
        return 'N/A'
    if value == 'Depression':
        return 'depression'
    if value == 'Bipolar':
        return 'bipolar'
    if value == 'no-lesion-control':
        return 'N/A'
    if value == 'non-PFC-lesion':
        return 'brain-lesion'

    return value
