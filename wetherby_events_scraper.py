import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.wetherby.co.uk/Whats_On_3783.aspx"
page = requests.get(url)
# print(page.status_code)

soup = BeautifulSoup(page.content, "html.parser")
events_raw = soup.find_all("div", class_="col-sm-3")
# events_raw[0:3]

event_name = []
for event in events_raw:
    event_name.append(event.find("h4").text)

# event_name[0:3]

event_details_raw =[]
for event in events_raw:
    event_details_raw.append(event.find_all("p"))

# event_details_raw[0:3]

event_details_df = pd.DataFrame(event_details_raw,dtype="string")
event_details_df = event_details_df.drop(3,axis=1)
event_details_df.rename(columns = {0:"Location", 
                                   1:"Date & Time",
                                   2:"Extra Info"}, inplace=True)

event_details_df.replace({r"<p>":"",r"</p>":"","&amp;": r"&"}, regex=True,inplace=True)
event_details_df["Date & Time"].iloc[14] = "23 Nov 23"


event_details_df["Name"] = event_name
event_details_df = event_details_df[["Name", "Location", "Date & Time", "Extra Info"]]


event_details_df.to_csv("Wetherby Events.csv")