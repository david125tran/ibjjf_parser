#-------------------------------------- Terminal installs --------------------------------------
# python -m ensurepip
# python -m pip install BeautifulSoup4
# python -m pip install requests
# python -m pip install pandas
# python -m pip install openpyxl
# python -m pip install pipreqs
#-------------------------------------- Libraries --------------------------------------
from bs4 import BeautifulSoup
import requests
import pandas as pd
from openpyxl import Workbook, load_workbook, styles
from openpyxl.styles import Font, PatternFill, Alignment

#-------------------------------------- HTML Color Code Constants --------------------------------------
# https://htmlcolorcodes.com/
BLUE = "58bae8"
PURPLE = "FF00FF"
BROWN = "873600"
BLACK = "000000"
RED = "FF0000"

GREEN_HEADER = "09c97d"
#-------------------------------------- User Inputs --------------------------------------
team = "G13 BJJ USA"
url = "https://www.ibjjfdb.com/ChampionshipResults/2411/PublicAcademyRegistration?lang=en-US"
filename = "IBJJF Atlanta 2024"
filename = filename + ".xlsx"

#-------------------------------------- Parse IBJJF'S Athlete Registration List --------------------------------------
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Get team's athletes
athletes = soup.find_all("script")[4].get_text()
athletes = athletes.split(f'{team}",', 1)
athletes.remove(athletes[0])
x = ']},{"'
athletes = athletes[0].split(x, 1)
athletes = athletes[0]
athletes = athletes.replace('"AthleteCategory":[', '')
athletes = athletes.replace('{"FriendlyCategoryName":"', '')
athletes = athletes.replace('","AthleteName":"', ',')
athletes = athletes.replace('"},', ',')
athletes = athletes.replace('"}', '')
athletes = athletes.split(",")

csv_dictionary = {
    'Time': [],
    'Mat': [],
    'Division': [],
    'Weight Class': [],
    'Name': []
}

rank_list = []

for i in range(0, len(athletes)):
    # Store the rank, age_group, gender, and weight_class
    if i % 2 == 0:
        athlete_info = athletes[i].split("/")
        rank = athlete_info[0]
        age_group = athlete_info[1]
        weight_class = athlete_info[3]

        # Remove unwanted spaces
        rank = rank[0:-1]
        age_group = age_group[1:-1]
        weight_class = weight_class[1:]

        # Get divsion info, ex. "Master 1" --> "M1"
        if (age_group[0] == "A") or (age_group[0] == "J"):          # "Adult" class and "Juvenile class"
            division = age_group[0]
        else:                                                       # "Master" class
            division = age_group[0] + age_group[-1] 

        # Append to rank_list
        rank_list.append(rank)
        # Append  to csv_dictionary
        csv_dictionary['Time'].append("TBD")
        csv_dictionary['Mat'].append("TBD")
        csv_dictionary['Division'].append(division)
        csv_dictionary['Weight Class'].append(weight_class)

    # Store the athlete's name
    else:
        name = athletes[i]
        # Append to team_dictionary 
        csv_dictionary['Name'].append(name)

#-------------------------------------- Push 'csv_dictionary' to MS Excel (.xlsx) with Pandas  --------------------------------------
# dictionary to data frame
df = pd.DataFrame.from_dict(csv_dictionary)

# dataframe to csv
df.to_excel(filename, index=False, header=True)

#-------------------------------------- Format Excel File with OpenPyXL --------------------------------------
# Load the already created Excel file
wb = load_workbook(filename)

# Get the active sheet
ws = wb.active

# Adjust column widths
ws.column_dimensions["D"].width = 25
ws.column_dimensions["E"].width = 35

# Change cell colors of different divisions
for i in range(0, len(rank_list)):
    cell = "C" + str(i + 2) # Start at cell "C2"
    if rank_list[i] == "WHITE":
        pass
    elif rank_list[i] == "BLUE":
        ws[cell].fill = PatternFill(start_color=BLUE, end_color=BLUE, fill_type="solid")
    elif rank_list[i] == "PURPLE":
        ws[cell].fill = PatternFill(start_color=PURPLE, end_color=PURPLE, fill_type="solid")
    elif rank_list[i] == "BROWN":
        ws[cell].fill = PatternFill(start_color=BROWN, end_color=BROWN, fill_type="solid")
    elif rank_list[i] == "BLACK":
        ws[cell].font = Font(color=RED) 
        ws[cell].fill = PatternFill(start_color=BLACK, end_color=BLACK, fill_type="solid")

# Change cell colors of column names
ws["A1"].fill = PatternFill(start_color=GREEN_HEADER, end_color=GREEN_HEADER, fill_type="solid")
ws["B1"].fill = PatternFill(start_color=GREEN_HEADER, end_color=GREEN_HEADER, fill_type="solid")
ws["C1"].fill = PatternFill(start_color=GREEN_HEADER, end_color=GREEN_HEADER, fill_type="solid")
ws["D1"].fill = PatternFill(start_color=GREEN_HEADER, end_color=GREEN_HEADER, fill_type="solid")
ws["E1"].fill = PatternFill(start_color=GREEN_HEADER, end_color=GREEN_HEADER, fill_type="solid")

# Center align rows 1 to 100 for columns A to E
for row in range(1, 100):
    ws["A" + str(row)].alignment = Alignment(horizontal='center', vertical='center')
    ws["B" + str(row)].alignment = Alignment(horizontal='center', vertical='center')
    ws["C" + str(row)].alignment = Alignment(horizontal='center', vertical='center')
    ws["D" + str(row)].alignment = Alignment(horizontal='center', vertical='center')
    ws["E" + str(row)].alignment = Alignment(horizontal='center', vertical='center')

# Save the file
wb.save(filename)

#-------------------------------------- Generate requirements.txt file --------------------------------------
# pipreqs C:\Users\Laptop\Desktop\IBJJF_Parser