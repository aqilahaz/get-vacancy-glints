
import ast
from bs4 import BeautifulSoup
import requests
import json

def make_dictionary(soup):
    lib = {}
    lib['platform'] = 'glints'
    
    for pekerjaan in soup.find_all('div', {"class":"TopFoldsc__JobOverViewTitle-kklg8i-3 gaBsxq"}):
        lib['pekerjaan'] = pekerjaan.text
    
    for perusahaan in soup.find_all('div', {"class":"TopFoldsc__JobOverViewCompanyName-kklg8i-5 ldguEd"}):
        lib['perusahaan'] = perusahaan.text
    for loc in soup.find_all('div', {"class":"TopFoldsc__JobOverViewCompanyLocation-kklg8i-6 bQlTwv"}):
        lib['lokasi'] = loc.text
        
    for pos in soup.find_all('span', {"class":"TopFoldsc__PostedAt-kklg8i-11 cRnvgg"}):
        lib['posted_at'] = pos.text
    
    result = soup.select('div.eWKiJR')
    if len(result) ==3:
        for i in range(0, len(result)):
            lib['pengalaman'] = result[-1].text
            lib['industri'] = result[0].text
            lib['tipe'] = result[1].text
    elif len(result) ==  4:
        for i in range(0, len(result)):
            lib['gaji'] = result[0].text
            lib['industri'] = result[1].text
            lib['tipe'] = result[2].text
            lib['pengalaman'] = result[3].text
    elif len(result) == 2:
        for i in range(0, len(result)):
            lib['industri'] = result[0].text
            lib['tipe'] = result[1].text
    skil =[]
#list = ['Motion Graphics, Creative Concept, ... ']
    for skill in soup.find_all('div', {"class":"TagStyle__TagContainer-sc-66xi2f-1 cPvXJd aries-tag Skillssc__TagOverride-sc-11imayw-3 bssJoZ"}):
       skil.append(skill.text)
    lib['skill'] = skil
    for jobdesc in soup.find_all('div', {"class":"JobDescriptionsc__DescriptionContainer-sc-1jylha1-2 gpAMiw"}):
        # print(jobdesc.text)
        lib['jobdesc'] = jobdesc.text
    return lib


a_list = [] 
with open('one_list.txt', 'r') as f:
    mylist = ast.literal_eval(f.read())

# mylist = ['https://glints.com/id/opportunities/jobs/social-media-specialist-content-creator/80d9e237-de42-472a-b336-5727eea6235b', 'https://glints.com/id/opportunities/jobs/staff-sales/0b1e486d-a05c-4c42-becf-40ae922e4f90','https://glints.com/id/opportunities/jobs/finance-control-manager/3c349df1-e855-4164-a3dd-bd55f8618701']
print("JobStart")
num = 0
for link in mylist:
    html_doc = requests.get(link).text
    soup = BeautifulSoup(html_doc, 'lxml')
    kamus=make_dictionary(soup)
    dictionary_copy = kamus.copy()
    a_list.append(dictionary_copy)
    num+=1
    print(num)
# print(a_list)

with open('glints.json', 'w') as fp:
    json.dump(a_list, fp)
print("Job Finished")