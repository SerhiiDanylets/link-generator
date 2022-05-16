import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from grab import Grab
g = Grab()
from os.path import exists


def save_to_file(content):
    file_exists = exists("GeneratedLinks.json")
    if(file_exists):
        f = open("GeneratedLinks.json", "a")
        f.write(content)
        f.close()
    else:
        f = open("GeneratedLinks.json", "x")
        f.write(content)
        f.close()

    #open and read the file after the appending:
    #f = open("GeneratedLinks", "r")
    #print(f.read())

# Replace the existing home function with the one below
def home(request):
    context = {
		"title":"Trigger python logic"
    }
    return render(request, "hello/home.html",context)

def simple_function(request):
    resp = g.go('https://nekretninecrikvenica.net/')
# Create a pattern to match names
    name_pattern = re.compile(r'parent_location\":\"(\w+)\"', flags = re.M)
# Find all occurrences of the pattern
    transaction_id =1 #1 or 2
    locations=name_pattern.findall(str(resp.body))
    locations = list(dict.fromkeys(locations))
    domain = ''
    i = 0
    sale_type ='sale_strict'
    link = ''
    final = []
    save_to_file('[')
    while(i<len(locations)):
        link = '\n{\n'+'\t"url":"'+'https://nekretninecrikvenica.net/listings/results?id_transaction='+str(transaction_id)+'&location='+str(locations[i])+'&page=[INDEX]",\n'+'\t"meta":'+ "{\n"+'\t\t"type":'+'"'+sale_type+'"'+',\n'+'\t\t"location_ids":'+ '[\n'+'\t\t\t"CONSTANT."\n'+'\t\t]\n'+'\t}\n'+'}'
        save_to_file(str(link))
        if(i<len(locations)-1):
            save_to_file(',')
        final.append(link)
        if(transaction_id==1):
            transaction_id=2
            sale_type='rent_strict'
        elif(transaction_id==2):
            sale_type='sale_strict'
            transaction_id=1
        i=i+1
    save_to_file(']')
    #save_to_file(str(final))
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def about(request):
    return render(request, "hello/about.html")

def contact(request):
    return render(request, "hello/contact.html")

def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )



