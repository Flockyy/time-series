from model import LostItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import requests
import dateparser

engine = create_engine('sqlite:////db.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

def request_lost_item(start_date,end_date):
    if isinstance(start_date,str): 
        start_date = dateparser.parse(start_date)

    if isinstance(end_date,str): 
        end_date = dateparser.parse(end_date)
    
    start_date = str(start_date.date())
    end_date =  str(end_date.date())
    URL = "https://ressources.data.sncf.com/"
    ressource = f"api/records/1.0/search/?dataset=objets-trouves-restitution&q=date:[{start_date}%20TO%20{end_date}]&rows=10000&sort=date&refine.gc_obo_gare_origine_r_name=Lille+Europe"
    
    my_request = requests.get(URL + ressource)

    field_list = [
    ["type_objet", "gc_obo_type_c"],
    ["date_restitution", "gc_obo_date_heure_restitution_c"]
]

    for lost_item in my_request.json()["records"]:   
        lost_item_data= {}
        
        for field in field_list:    
            try: 
                lost_item_data[field[0]] = lost_item["fields"][field[1]]
            except KeyError:
                lost_item_data[field[0]]=None

        session.add(LostItem(date=lost_item["fields"]["date"],**lost_item_data))
    
    session.commit()

    return URL + ressource
    
request_lost_item("last week","yesterday")


# 0 0 * * TUE conda activate time_series ; /usr/local/Caskroom/miniconda/base/envs/time_series/bin/python3 /Users/charles/Documents/pythonProject/time_series_sncf/python_cron_script.py