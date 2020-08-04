#import libraries
import requests
import json

with open('oauth.json','r') as json_file:
    settings = json.load(json_file)

token_url = 'https://login.microsoftonline.com/{0}/oauth2/token'.format(settings['tenant_id'])
query = '?select=id,name,lastModifiedDateTime&expand=items(expand=fields(select=title,url,createdby,description))'

graph_url = 'https://graph.microsoft.com/v1.0/sites/{0}/lists/{1}{2}'.format(settings['site_id'],settings['list_id'],query)

token_data = {
    'grant_type' : 'client_credentials',
    'client_id' : settings['app_id'],
    'client_secret' : settings['app_secret'],
    'resource' : settings['resource_url']
}

col_alias = 'Title'
col_url = 'url'
col_des = 'Description'

#get token
def get_token(token_url,token_data):
    token_r = requests.post(token_url,data=token_data)
    token = token_r.json().get('access_token')
    return token

#create header for GET request
def get_headers(token):
    headers = {
        'Authorization':'Bearer {0}'.format(token)
    }
    return headers

#get sharepoint list
def get_spo_list(graph_url,headers):
    spo_list_r =requests.get(graph_url,headers=headers)
    return json.loads(spo_list_r.text)

#get lastModifiedDateTime
def get_lastModifiedDateTime(spo_list):
    return spo_list['lastModifiedDateTime']

#create data
def get_aliases(spo_list,col_alias,col_url,col_des):
    aliases = {}
    for i in range(len(spo_list['items'])):
        data_alias = spo_list['items'][i]['fields'][col_alias]
        data_url = spo_list['items'][i]['fields'][col_url]
        data_description = spo_list['items'][i]['fields'][col_des]
        aliases[data_alias]={'url':data_url,'des':data_description}

    return aliases