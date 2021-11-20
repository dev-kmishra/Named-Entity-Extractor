from flask import Flask, render_template, request, url_for
import re as re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_sm

nlp = spacy.load('en_core_web_sm')

#Regex
email_regex= re.compile(r"[\w\.\-]+@[\w\.-]+")
phone_regex = re.compile(r"\d\d\d.\d\d\d.\d\d\d\d")
url_https_regex = re.compile(r"https?://www\.?\w+\.\w+")
url_regex=re.compile(r"http?://www\.?w+\.\w+")



#initialize app
app=Flask(__name__,template_folder='template')


#Route
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['GET','POST'])
def process():
    df=pd.DataFrame()
    ORG_named_entity=""
    
    if request.method=="POST":
        rawtext=request.form['rawtext']
        choice=request.form['taskoption']
        results=""

        doc=nlp(rawtext)
        d=[]
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df=pd.DataFrame(d, columns=('named_entity','Text'))
            ORG_named_entity= df.loc[df['named_entity']=='ORG']['Text']
            PERSON_named_entity=df.loc[df['named_entity']=='PERSON']['Text']
            GPE_named_entity=df.loc[df['named_entity']=='GPE']['Text']
            MONEY_named_entity=df.loc[df['named_entity']=='MONEY']['Text']

            if choice == 'oraganization':
                results=ORG_named_entity
                num_of_results=len(results)
            elif choice == 'person':
                results=PERSON_named_entity
                num_of_results=len(results)
            elif choice == 'geopolitical':
                results=GPE_named_entity
                num_of_results=len(results)
            elif choice == 'money':
                results=MONEY_named_entity
                num_of_results=len(results)
        
    return render_template("index.html", results=results)


if __name__=='__main__':
    app.run(debug=True)
