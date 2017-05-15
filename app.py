from flask import Flask, render_template, request
from lxml import html, etree
from multiprocessing import Process

import requests, webbrowser, sys
import os

app = Flask(__name__)



@app.route('/')
def show_search():
    return render_template('search.html')

@app.route('/search', methods = ['GET', 'POST'])
def show_results():
    search = request.form['searchTerm']

    #Panel 1 -- Definition
    #definition = show_definition(search)
    definition = "Mesothelioma: A malignant tumor of the mesothelium, the thin lining of the surface of the body cavities and the organs that are contained within them. Most mesotheliomas begin as one or more nodules that progressively grow to form a solid coating of tumor surrounding the lung, abdominal organs, or heart. Mesothelioma occurs most commonly in the chest cavity and is associated with exposure to asbestos in up to 90 percent of cases. The risk of mesothelioma increases with the intensity and duration of exposure to asbestos. Family members and others living with asbestos workers may also have an increased risk of developing mesothelioma and possibly other asbestos-related diseases. This risk may be the result of exposure to asbestos dust brought home on the clothing and hair of asbestos workers. Mesothelioma is currently difficult to treat in most cases, and carries a poor prognosis."

    #Panel 2 -- Videos
    #videoIds = show_videos(search)
    videoIds = [u'uAs6eTHN-U8', u'wY_i1OT4kjo', u'8GaklC6RXvQ', u'1lg_qS2b1VE']

    #Panel 3 -- Image Gallery
    #diagram = show_diagram(search)
    diagram = 'https://thumbs.dreamstime.com/z/pleural-mesothelioma-medical-illustration-effects-32786689.jpg'

    #Panel 4 -- Interesting Papers
    #papers = show_papers(search)
    papers = {'Primary pericardial mesothelioma and asbestos exposure: a rare fatal disease.': 'https://www.ncbi.nlm.nih.gov/pubmed/28500034', 'Induction of IL-17 production from human peripheral blood CD4+ cells by asbestos exposure.': 'https://www.ncbi.nlm.nih.gov/pubmed/28498408', 'Multiple malignant epithelioid mesotheliomas of the liver and greater omentum: a case report and review of the literature.': 'https://www.ncbi.nlm.nih.gov/pubmed/28493096', 'Pemetrexed-induced acute kidney failure following irreversible renal damage: two case reports and literature review.': 'https://www.ncbi.nlm.nih.gov/pubmed/28491851', 'Immune checkpoint inhibitors in malignant pleural mesothelioma.': 'https://www.ncbi.nlm.nih.gov/pubmed/28495276', '[Malignant Pleural Mesothelioma Presenting Refractory Pneumothorax Successfully Treated by Intrapleural Administration of Diluted Fibrin Glue;Report of a Case].': 'https://www.ncbi.nlm.nih.gov/pubmed/28496089'}


    #return '%s --' % linkResults

    return render_template('results.html', definition = definition, videoIds = videoIds, diagram = diagram, papers = papers)


### HELPER METHODS

#   Panel 1 -- Layman's Terms

def show_definition(search):
    lookup = 'http://www.medicinenet.com/script/main/srchcont.asp?cat=dict&src=%s' % search
    page = requests.get(lookup)
    tree = html.fromstring(page.content)

    #list of terms
    results = tree.xpath('//ul[contains(@class, "bulletArrow")]/li/a/@href')

    #choose the first term and append URL for further definition scraping
    link = "http://www.medicinenet.com" + results[0]
    page = requests.get(link)
    tree = html.fromstring(page.content)

    entryList = tree.xpath('//div[@id="artPromoCunk"]/following::p')
    #return strictly text content of definitions, stripping boldface/hyperlinks
    definition = entryList[0].text_content()

    return definition

#   Panel 2 -- Gallery of Videos

def show_videos(search):

    key = 'AIzaSyCDK1mWAeZTtRmVk40tM4ZLwjTNjlyeTvI'
    lookup = 'https://www.googleapis.com/youtube/v3/search?part=snippet&q={0}+medical&maxResults=10&key={1}'.format(search, key)
    page = requests.get(lookup)

    data = page.json()
    items = data['items']

    videoIds = []

    for i in items:
        string = i['id']['videoId']
        videoIds.append(string)

    return videoIds

#   Panel 3 -- Photo Gallery

def show_diagram(search):

    key = 'AIzaSyA_WGveT9U1rhkB4ppZPScD7WagP3vhSUs'
    engine = '010994566073850053384:4veokx4sn9o'
    lookup = 'https://www.googleapis.com/customsearch/v1?q={0}+medical+diagram&cx={1}&searchType=image&key={2}'.format(search, engine, key)
    page = requests.get(lookup)

    data = page.json()

    items = data['items']

    picLinks = []

    for i in items:
        string = i['link']
        picLinks.append(string)

    #change return type for 10 pics
    return picLinks[0]

#   Panel 4 -- Interesting Articles

def show_papers(search):
    lookup = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=10&term=%s' % search
    page = requests.get(lookup)
    tree = etree.fromstring(page.content)

    paperIDs = tree.xpath('/eSearchResult/IdList/Id/text()')

    names = []
    links = []
    
    for p in paperIDs:
        paperLookup = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=%s' % p
        paperPage = requests.get(paperLookup)
        tree = etree.fromstring(paperPage.content)

        paperName = tree.xpath('//Item[@Name="Title"]/text()')[0]
        paperLink = "https://www.ncbi.nlm.nih.gov/pubmed/%s" % p  

        names.append(paperName)
        links.append(paperLink)

    papers = dict(zip(names, links))
    return papers


#   Helper methods

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)