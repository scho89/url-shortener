#views.py
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
import os
from Redirect.graph import *
import datetime

project_root = os.path.dirname(os.path.realpath(__file__))
os.chdir(project_root)
os.chdir("..")

try:
    csv_path = 'bk_alias.txt'

    csv = open(csv_path,'r')
    aliases_csv = {}
    context={}

    for line in csv.readlines():
        if not line.startswith('#'):
            try:
                raw = line.strip().split(',')
                if "https://" in raw[1].lower() or "http://" in raw[1].lower():
                    aliases_csv[raw[0]]={'url':raw[1],'des':raw[2]}

            except:
                pass

    csv.close()

    context['aliases']=aliases_csv

except:
    context['aliases']={}



def set_context_get_aliases():
    try:
        token = get_token(token_url,token_data)
        headers = get_headers(token)
        spo_list = get_spo_list(graph_url,headers)
        aliases = get_aliases(spo_list,col_alias,col_url,col_des)

        bk_csv = open(csv_path,'w',encoding='utf8')
        print('alias,url,description',file=bk_csv)
        for key,value in aliases.items():
            print('{0},{1},{2}'.format(key,value['url'],value['des']),file=bk_csv)
        bk_csv.close()

        context['aliases']=aliases
        context['lastModifiedDateTime']=get_lastModifiedDateTime(spo_list)
        return aliases

    except Exception as ex:
        print(ex)
        context['aliases']=aliases_csv
        context['lastModifiedDateTime']= str(datetime.datetime.fromtimestamp(os.path.getmtime(csv_path)))+" from local cache."
        return aliases_csv

def home(request,alias):
    aliases = set_context_get_aliases()
    if alias in aliases.keys():
        return HttpResponseRedirect(aliases[alias]['url'])

    else:
        if not alias == 'favicon.ico': 
            context['alias']=alias
        else:
            context['alias']=False
            
        return HttpResponseRedirect('https://www.zenithn.com')

def list_aliases(request):
    return render(request,'Redirect/aliases.html',context=context)


def redirect_home(request):
    return HttpResponseRedirect('https://zenithn.sharepoint.com/sites/URL-Shortener/Lists/Aliases/AllItems.aspx')

aliases = set_context_get_aliases()
