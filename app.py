from flask import Flask, render_template, request
from lxml import html, etree

import requests, webbrowser, sys

app = Flask(__name__)



@app.route('/')
def show_search():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def show_results():
    search = request.form['searchTerm']
    linkResults = ""

    paperTitles, paperLinks = show_papers(search)

    papers = dict(zip(paperTitles, paperLinks))

    definition = show_definition(search)

    #return '%s --' % linkResults

    return render_template('results.html', papers = papers, definition = definition)


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

#   Panel 3 -- Photo Gallery

#   Panel 4 -- Interesting Articles

def show_papers(search):
    lookup = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=6&term=%s' % search
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

    return names, links


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)