from flask import Flask,render_template,request
import random
import requests
app = Flask(__name__, template_folder='templates')
@app.route('/',methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        mname=request.form['movie']
        if not (mname ==""):
            op=findm(mname)
            return "\t"+op
        else:
            return  processquery(mname)+"\nCheck the movie name field"

"""
===========================================================
"""
def findms(mname):
        return "1"
"""=========================================================="""
def cleanrev(raw_html):
    import re, string
    raw_html = str(raw_html)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.translate(string.maketrans("", ""), string.punctuation)
    return cleantext
"""=========================================================="""
def processquery(mname):
    mname=str(mname)
    import string
    mname=mname.strip().lower().replace(' ','_')
    return mname
def getarray(mname):
    mname=processquery(mname)
    import requests
    from bs4 import BeautifulSoup
    url = 'https://www.rottentomatoes.com/m/'
    try:
        result = requests.get(url + mname + '/reviews/')
        csharpcorner = result.content
        scrap = BeautifulSoup(csharpcorner, 'html.parser')
        post = scrap.find_all("div", attrs={'class': 'the_review'})
        if(len(post) == 0):
            url=result.url+"/reviews/"
            result = requests.get(url + mname + '/reviews/')
            csharpcorner = result.content
            scrap = BeautifulSoup(csharpcorner, 'html.parser')
            post = scrap.find_all("div", attrs={'class': 'the_review'})
        return post
    except Exception :
        stre=[]
        return stre
"""=========================================================="""
def fetchS(mname, status):
    import json
    import requests
    if (status != "-1"):
        score_arr = []
        host = "westus.api.cognitive.microsoft.com"
        content_type = "application/json"
        Key = "f00b6601f4a442a39738c4f9cf974d6c"
        hedrs = {'HOST': host, "Content-Type": content_type, "Ocp-Apim-Subscription-Key": Key}
        url = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
        post = getarray(mname)
        k = len(post)
        if k == 0 :
            return "Couldn't Scrape the movie review :("
        for i in range(0,k):
            posts = post[i]
            single_review = str(cleanrev(posts))
            # print len(single_review),repr(single_review)
            json = "{	   \"documents\": [   {   \"language\": \"en\",\"id\": \"string\",\"text\":\"" + single_review + "\" }]}"
            req = requests.post(url, headers=hedrs, data=json)
            geq = req.json()
            score = geq['documents'][0]['score']
            score_arr.append(score)
        sum = 0.0
        for i in score_arr:
            sum = sum + float(i)
        if not( len(score_arr) < 1):
            sum = (sum *100) / len(score_arr)
            sum=round(sum,2)
            if (sum > 60.00):
                return "It's very likey that the movie " + mname + " is going to be hit \n with rating(out of 100) "+str(sum)
            elif sum > 30:
                return "It's moderately likey that the movie " + mname+ " is going to be hit\n with rating(out of 100) "+str(sum)
            else:
                return "It's higly unlikey that the movie " + mname + " is going to be hit \n with rating(out of 100) "+str(sum)
        else :
            return "Couldn't scrape the movie reviews :(, Try with some other name"
    else:
        return "Kindly check the movie name OR Maybe it's your connection"
"""================================================="""
def findm(mname):
    status = findms(mname)
    return fetchS(mname, status)
if __name__=='__main__':
    app.run()
#    app.run(host='0.0.0.0',port=8080,debug=True)
