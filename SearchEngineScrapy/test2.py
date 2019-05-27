import requests
import json
from fuzzywuzzy import fuzz
index = "ccoemparts"
ccoemparts = str(123)
indextype ="oemparts"
category_id =1
sub_category_id=2
publish_url =""
oem_list=[]
start =0
size=1000
for i in range(7):
    oem_url = "http://localhost:9200/ccoemparts/oemparts/_search?size="+str(size)+"&from="+str(start)
    start = start + size
    oem_data = requests.get(oem_url)
    oem_data = json.loads(oem_data._content)['hits']['hits']
    for i in oem_data:
        oem_list.append(i)
cat_data = requests.get('http://localhost:9200/cccategory/category/_search?size=1000')
z = json.loads(cat_data._content)
cat_data = z['hits']['hits']
#url = "curl -X POST "+"localhost:9200/"+ccoemparts+"/"+ccoemparts+"/"+ccoemparts+"/"+"_update "+"-H"+"' Content-Type: application/json' -d'"+"{"+'"doc"'+":"+"{"+'"category_id"'+":"+ccoemparts+","+'"sub_category_id"'+":"+ccoemparts+"}}"

# import pdb
# pdb.set_trace()
for idx in oem_list:
    data={}
    max1 = 95
    for idy in cat_data:
        perc = fuzz.ratio(idy['_source']['name'], idx['_source']['name'])
        if perc>max1:
            data.update({'category_id':idy['_source']['parent_id']})
            data.update({'sub_category_id':idy['_source']['id']})
            data.update({'id':idx['_source']['id']})

            max1=perc
    if max1>95:
        url = "curl -X POST " + ' "localhost:9200/ccoemparts/oemparts/'+ str(data["id"]) + '/' + '_update"' + "-H " + "'Content-Type: application/json' -d'" + "{" + '"doc"' + ":" + "{" + '"category_id"' + ":" + str(data['category_id']) + "," + '"sub_category_id"' + ":" + str(data['sub_category_id']) + "}}'"
        with open("data.sh",'a+') as f:
            f.write(url)
            f.write("\n")
