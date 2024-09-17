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

     cf_file_id = None
     cf_client_file = None
     cf_server_file = None
     cf_change_log_data = None
     cf_change_log = None
     cf_project_data = None
     cf_download_count = None

     def get_client_file(self) -> str:
          """Returns a link to the CF page of the most recent file"""
          if(Curseforge.cf_project_data == None):
               Curseforge.cf_project_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID, headers = Curseforge.headers).json()
          Curseforge.cf_file_id = str(Curseforge.cf_project_data['data']['mainFileId'])
          Curseforge.cf_client_file ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + Curseforge.cf_file_id
          return Curseforge.cf_client_file

     def get_server_file(self) -> str:
          """Returns a link to the CF page of the most recent file"""
          if(Curseforge.cf_project_data == None):
               Curseforge.cf_project_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID, headers = Curseforge.headers).json()
          Curseforge.cf_file_id = str(Curseforge.cf_project_data['data']['mainFileId'])
          Curseforge.cf_server_file ='https://www.curseforge.com/minecraft/modpacks/mc-chocolate-edition/files/' + Curseforge.cf_file_id + '/additional-files'
          return Curseforge.cf_server_file

     def get_change_log(self) -> str:
          """Returns the change log of the most recent update"""
          if(Curseforge.cf_change_log == None):
               if(Curseforge.cf_project_data == None):
                    Curseforge.cf_project_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID, headers = Curseforge.headers).json()
               Curseforge.cf_file_id = str(Curseforge.cf_project_data['data']['mainFileId'])
               Curseforge.cf_change_log_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID +'/files/' + Curseforge.cf_file_id + '/changelog', headers = Curseforge.headers).json()
               Curseforge.cf_change_log = html2text.html2text(str(Curseforge.cf_change_log_data['data']))
          return Curseforge.cf_change_log

     def get_downloads(self) -> str:
          """Returns the how many downloads the pack has"""
          Curseforge.cf_project_data = requests.get('https://api.curseforge.com/v1/mods/'+ Curseforge.CF_PROJECT_ID, headers = Curseforge.headers).json()
          Curseforge.cf_download_count = str(Curseforge.cf_project_data['data']['downloadCount'])
          return Curseforge.cf_download_count


     def update_cf(self) -> None:
          """Updates the CF links/log"""
          Curseforge.cf_file_id = None
          Curseforge.cf_client_file = None
          Curseforge.cf_server_file = None
          Curseforge.cf_change_log_data = None
          Curseforge.cf_change_log = None
          Curseforge.cf_project_data = None

