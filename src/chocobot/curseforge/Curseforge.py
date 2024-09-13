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
     cf_file_data = None
     file_id = None
     cf_client_file = None
     cf_server_file = None
     cf_change_log = None
     change_log = None

     def get_client_file(self) -> str:
          """Returns a link to the CF page of the most recent file"""
          return Curseforge.cf_client_file

     def get_server_file(self) -> str:
          """Returns a link to the CF page of the most recent file"""
          return Curseforge.cf_server_file

     def get_change_log(self) -> str:
          """Returns the change log of the most recent update"""
          return Curseforge.change_log

     def update_cf(self) -> None:
          Curseforge.cf_file_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files', headers = Curseforge.headers).json()
          Curseforge.file_id = str(Curseforge.cf_file_data['data'][0]['id'])
          Curseforge.cf_client_file ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + Curseforge.file_id
          Curseforge.cf_server_file ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + Curseforge.file_id + '/additional-files'

          Curseforge.cf_change_log = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files/' + Curseforge.file_id + '/changelog', headers = Curseforge.headers).json()
          Curseforge.change_log = html2text.html2text(str(Curseforge.cf_change_log['data']))