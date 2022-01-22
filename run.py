import requests
import json
import gspread
import pandas

# --Read Config JSON--
with open('config.json') as json_file:
    data = json.load(json_file)
    # --Notion Keys Set Up--
    SECRET = data['Notion']["SECRET"]
    DB_ID = data['Notion']["DB_ID"]
    URL = "https://api.notion.com/v1/databases/"+DB_ID+"/query"
    # --Notion Keys Set Up--
    
    
    # --GoogleSheet set up
    SHEET_OPEN_KEY=data['GSheet']["SHEET_OPEN_KEY"]
    gc = gspread.service_account(filename='credentials.json')
    config_sh = gc.open_by_key(SHEET_OPEN_KEY)
    worksheet = config_sh.get_worksheet(1)
    # --GoogleSheet set up
# --Read Config JSON--  


# --Subject class--
class Subject():
    def __init__(self, name, semester, it_block, category, credit, required, status, grade, number_of_try):
        self.name = name
        self.semester = semester
        self.it_block = it_block
        self.category = category
        self.credit = credit
        self.required = required
        self.status = status
        self.grade = grade
        self.number_of_try = number_of_try
        
    def to_dict(self):
        return {
        'name': self.name,
        'semester': self.semester,
        'it_block': self.it_block,
        'category': self.category,
        'credit': self.credit,
        'required': self.required,
        'status': self.status,
        'grade': self.grade,
        'number_of_try': self.number_of_try
        }
# --Subject class--
 
    
# --Query Notion Database--    
headers = {
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13",
    "Authorization": "Bearer " + SECRET,
    }

response = requests.request("POST", URL, headers=headers)

with open('uni.json', 'w') as f:
    f.write(response.text)
# --Query Notion Database--


# --JSON to Subject list method--
response_json = json.loads(response.text) 
subject_list = []
for s in response_json['results']:
    try:
        name = s['properties']['Name']['title'][0]['plain_text']
    except:
        name = ''
        
    try:
        semester = s['properties']['Ajánlott félév']['select']['name']
    except:
        semester = ''
    
    try:
        it_block = s['properties']['Informatikai blokk']['select']['name']
    except:
        it_block = ''
    try:
        category = s['properties']['Kategória']['select']['name']
    except:
        category = ''
    
    try:
        credit = s['properties']['Kredit']['number']
    except:
        credit = ''
        
    try:
        required = s['properties']['Kötelező?']['select']['name']
    except:
        required = ''
    
    try:
        status = s['properties']['Status']['select']['name']
    except:
        status = ''
    
    try:
        grade = s['properties']['Érdemjegy']['number']
    except:
        grade = ''
        
    try:
        number_of_try = s['properties']['Felvételek száma']['number']
    except:
        number_of_try = ''
        
    subject = Subject(name, semester, it_block, category, credit, required, status, grade, number_of_try)
    subject_list.append(subject)
# --JSON to Subject list method--


# --Final: subject list to dataframe and then to googlesheet-- 
subject_dataframe = pandas.DataFrame.from_records([s.to_dict() for s in subject_list])   
worksheet.clear()
worksheet.update([subject_dataframe.columns.values.tolist()] + subject_dataframe.values.tolist(), value_input_option='USER_ENTERED')
# --Final: subject list to dataframe and then to googlesheet--



        
