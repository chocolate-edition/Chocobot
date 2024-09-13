import requests
import html2text
import os

class Curseforge:
     CF_PROJECT_ID = '888414'
     CF_TOKEN: str = os.environ['CURSE_FORGE_TOKEN']
     headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'x-api-key': CF_TOKEN
     }

     def __init__(self):
          self.cf_file_data = None
          self.file_id = None
          self.cf_link = None
          self.cf_change_log = None
          self.change_log = None

     def update_cf(self) -> None:
          self.cf_file_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files', headers = Curseforge.headers).json()
          self.file_id = str(self.cf_file_data['data'][0]['id'])
          self.cf_link ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + self.file_id

          self.cf_change_log = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files/' + self.file_id + '/changelog', headers = Curseforge.headers).json()
          self.change_log = html2text.html2text(str(self.cf_change_log['data']))

