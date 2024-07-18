import json
import re
import urllib.parse

import requests

from .project import Project


class Server:
  def __init__(self, url: str = "http://localhost:3333"):
    self.url = url
    self.token = None

  @property
  def is_connected(self):
    return self.token is not None

  def get_csrf_token(self) -> str:
    response = requests.get(f'{self.url}/command/core/get-csrf-token')
    j = response.json()
    if 'token' not in j:
      raise Exception("Invalid response")

    return j['token']

  def connect(self):
    self.token = self.get_csrf_token()
    return self

  def disconnect(self):
    self.token = None
    return self

  def get(self, path, query=None, headers=None, *args, **kwargs):
    self.connect()

    if query is None:
      query = {}
    q = urllib.parse.urlencode({**query, 'csrf_token': self.token})

    if headers is None:
      headers = {}

    headers = {
      # 'Accept': 'application/xml,*/*;0.8',
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      **headers
    }

    r = requests.get(f"{self.url}/{path}?{q}", *args, headers=headers, **kwargs)

    if r.status_code >= 400 and r.status_code < 500:
      raise Exception(f"Invalid Request: Status Code {r.status_code}")
    if r.status_code >= 500 and r.status_code < 600:
      raise Exception(f"Internal Server Error: Status Code {r.status_code}")

    return r

  def post(self, path, query=None, headers=None, *args, **kwargs):
    self.connect()

    if query is None:
      query = {}
    q = urllib.parse.urlencode({**query, 'csrf_token': self.token})

    if headers is None:
      headers = {}

    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      **headers
    }

    req = requests.Request('POST', f"{self.url}/{path}?{q}", *args, headers=headers, **kwargs)
    prepared_req = req.prepare()
    # print(f"URL: {prepared_req.url}")
    # print(f"Headers: {prepared_req.headers}")
    # print(f"Body: {prepared_req.body}")

    with requests.Session() as session:
      r = session.send(prepared_req)
      # print(r.text)

    if r.status_code >= 400 and r.status_code < 500:
      print(r.text)
      raise Exception(f"Invalid Request: Status Code {r.status_code}")
    if r.status_code >= 500 and r.status_code < 600:
      print(r.text)
      raise Exception(f"Internal Server Error: Status Code {r.status_code}")

    return r

  def create_project_from_file(self, file_path: str, name: str = 'New Project') -> Project:
    path = f'command/core/create-project-from-upload'
    files = {'project-file': open(file_path, 'rb')}
    data = {
      'project-name': 'New Project',
      'format': 'test/line-based/*sv',
      'options': {
        # "encoding":"UTF-8",
        # "separator":",",
        # "ignoreLines":-1,
        # "headerLines":1,
        # "skipDataLines":0,
        # "limit":-1,
        # "storeBlankRows": True,
        # "guessCellValueTypes": True,
        # "processQuotes": True,
        # "quoteCharacter": "\"",
        # "storeBlankCellsAsNulls": True,
        # "includeFileSources": False,
        # "includeArchiveFileName": False,
        # "trimStrings": False,
        # "disableAutoPreview": False,
        # "projectName": name,
        # "projectTags":[]
      }
    }
    headers = {
      'Accept': 'application/xml,*/*;0.8',
    }
    r = self.post(path, data=data, files=files, headers=headers)

    if not 'project=' in r.url:
      print(r.text)
      raise Exception('Project Creation Failure')

    v = re.search(r'^.+project=(\d+).*$', r.url, re.I | re.S)

    return Project(int(v.group(1)), server=self)

  def get_metadata(self):
    return self.get(
      'command/core/get-all-project-metadata',
    ).json()

  def get_project(self, id: int):
    return Project(int(id), server=self)

  def get_all_projects(self):
    metadata = self.get_metadata();
    r = set()
    for id, proj in metadata['projects'].items():
      r.add(Project(int(id), server=self))
    return r

  def delete_project(self, project_id):
    data = {'project': project_id};
    return self.post(
      'command/core/delete-project',
      data=json.dumps(data),
      query=data,
    ).json()

  def __repr__(self):
    return f"Server(url={self.url}; token={self.token})"
