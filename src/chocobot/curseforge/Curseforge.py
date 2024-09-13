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

     def get_link(self) -> str:
          """Returns a link to the CF page of the most recent file"""
          cf_file_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files', headers = Curseforge.headers).json()
          file_id = str(cf_file_data['data'][0]['id'])
          cf_link ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + file_id
          return cf_link

     def get_change_log(self) -> str:
          """Rerturns the change log of the most recent update"""
          cf_file_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files', headers = Curseforge.headers).json()
          file_id = str(cf_file_data['data'][0]['id'])
          cf_change_log = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files/' + file_id + '/changelog', headers = Curseforge.headers).json()
          change_log = html2text.html2text(str(cf_change_log['data']))
          return change_log