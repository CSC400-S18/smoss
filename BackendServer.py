#!/usr/bin/env python3.6

#
#   FILE:   BackendServer.py
#   AUTHOR: mmiddleton
#   DATE:   19 FEB 2018
#
#   DESCRIPTION:
#   This file comprises the code that runs the Flask server for our MOSS solution.
#

from flask import *
from SortResults import SortResults
from AggregateData import AggregateData
from MossURLsRetrieval import MossURLsRetrieval
from Graph import Graph
from Result import Result
from MossParser import MossParser
import os
import re



# Global Variables
app = Flask(__name__, template_folder=os.path.dirname('./'))
sorter = SortResults ()
mossURLSretrieval = MossURLsRetrieval()
aggregate = AggregateData(None)
urlRetrieval = MossURLsRetrieval()
graph = Graph(None)


#
#   _Index ():     Generates the landing page for SMOSS.
#
@app.route ('/', methods = ['GET', 'POST'])
def _Index ():
    print('[BackendServer]\tIndex page displayed!')
    urlRetrieval.urls = []
    if request.method == "POST":
        inputURLs = request.form['text'] #input from the user
        urlList = inputURLs.split("\n")

        valid, url = getValidorInvalidURL(urlList)
        if not valid:
            template = "templates/errorpage.html"
            error = ("Invalid URL: "+ url)
            return render_template(template, value=error)
        else:
            urlRetrieval.urls=urlList
            return redirect('selectionpage')

    template = "templates/index.html"
    return render_template (template)

@app.route('/selectionpage',  methods = ['GET', 'POST'])
def _MOSSselectpage():
    print('[BackendServer]\tMOSS Selection page displayed!')
    template = "templates/SelectionPage.html"

    if request.method == "POST":
        selection = request.form['selection']
        mossURLSretrieval.reInit()
        #mossURLSretrieval.urls = []

        if (selection == "allURLs"):
            for url in urlRetrieval.urls:
                updated_url = url.rstrip()
                mossURLSretrieval.urls.append(updated_url)
        else:
            mossURLSretrieval.urls.append(selection)
        mossURLSretrieval.get_results()
        aggregate.reInit(mossURLSretrieval.results)
        return redirect('moss')
    duplicateValues, urlList = checkForDuplicates(urlRetrieval.urls)
    return render_template(template, urlList=urlList, duplicateValues=duplicateValues)

#
#   _MOSSOutput (): Formerly held within SortResults.py
# , this displays the MOSSoutput template at localhost:5000/moss
#
@app.route ('/moss')
def _MOSSOutput ():
    print('[BackendServer]\tMOSS Output page displayed!')
    template, value = getValidorInvalidMossTemplate()
    percentsValues = getValidorInvalidAggregateLinesTemplate()
    linesValues = getValidorInvalidAggregatePercentTemplate()
    results = mossURLSretrieval.results;

    graph = Graph(results)
    graphJson = graph.getJsonObject(results)
    nodes = graphJson["nodes"]
    edges = graphJson["edges"]
    return render_template(template, value=value, percentsValues=percentsValues, linesValues=linesValues, nodes=nodes, edges=edges)


@app.route('/URLvalidation')
def _MOSSurlvalidation():
    print('[BackendServer]\tMOSS URL validation page displayed!')
    template, value = getValidorInvalidURL()
    return render_template(template, value=value)


def checkForDuplicates(urlList):
    nonDuplicates = set()
    duplicates=set()
    for url in urlList:
        if url.rstrip() not in nonDuplicates:
            nonDuplicates.add(url.rstrip())
        else:
            duplicates.add(url.rstrip())

    return duplicates, nonDuplicates


def getValidorInvalidURL(urlList):

    valid, url = urlRetrieval.getValidity(urlList)
    if not valid:
        return False, url
    else:
        return True, url


def getValidorInvalidMossTemplate():
    if not(sorter.validateData()):
        template = "templates/errorpage.html"
        value = "Invalid File Data"
    else:
        template = "templates/MOSSoutput.html"
        value = sorter.get_csv()
    return template, value


def getValidorInvalidAggregatePercentTemplate():
    percentsValues = aggregate.top_percents
    return percentsValues


def getValidorInvalidAggregateLinesTemplate():
    linesValues = aggregate.top_lines
    return linesValues

#
#   _ErrorHandler ():   Displays the generic error page with output on the error type
#


@app.errorhandler (403)
@app.errorhandler (404)
def _ErrorHandler (errorCode):
    template = "templates/errorpage.html"
    return render_template (template, value = errorCode)


if __name__ == '__main__':
    app.run(debug = True, use_reloader=True)
