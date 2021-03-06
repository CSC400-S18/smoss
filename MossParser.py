# Class MossParser
# This class is designed to take a url as input and creates a csv file of results from MOSS in the same directory
# as this program
import urllib
import urllib.request
import lxml.html
from html.parser import HTMLParser
from Config import Config
from Result import Result


class MossParser ():
    def __init__(self):
        self.config = Config()

    # Parse a single URL
    def parse(self, url, assignmentNum):
        # Get the html text from the URL
        html = self.getHtml(url)

        if html is None:
            return False

        # Process the html into table strings
        tableStrings = self.processHtml(html)

        # Process the table strings into Result objects
        data, validFileName = self.processTableStrings(tableStrings, assignmentNum)

        if(validFileName):
            return data

    # Returns True if the URL is valid, else returns False
    def testUrl(self, url):
        if (not (isinstance(url, str)) or (("moss.stanford.edu/results" not in url) and ("171.64.78.49" not in url))):
            return False
        try:
            text=lxml.html.parse(url)
            html=text.find(".//title").text
            if(html != "Moss Results"):
                return False
            else:
                return True
        # Create an exception and return False if the URL is not valid
        except:
            return False

    # Return a list representing the table
    def processHtml(self, html):
        # Parse until table
        htmlParser = myHtmlParser()
        htmlParser.feed(html)

        # Here we have all of the rows in one long string
        # now we parse through the string and split them up into individual strings
        stripped = htmlParser.tableString.strip('\n')
        stripped = stripped.replace('\n', '')
        splitStrings = stripped.split("<tr>")

        # Have list of strings split up
        # first two indexes are a blank space and the header, so remove them
        del(splitStrings[0])
        del(splitStrings[0])
        return splitStrings

    # Get the size of the table
    def getSizeOfTables(self, urls):
        tableSizes = []
        for url in urls:
            html = self.getHtml(url)
            tableSizes.append(len(self.processHtml(html)))
        return tableSizes

    # Takes a url and returns its html
    def getHtml(self, url):
        if(self.testUrl(url) is True):
            html = urllib.request.urlopen(url)
            mybytes = html.read()
            mystr = mybytes.decode("utf8")
            html.close()
            return mystr
        else:
            return None

    def getTableStringValues(self, tableString):
        if not isinstance(tableString, str):
            return False
        tableString=self.formatTableString(tableString)

        # if we didn't get a csv format string, that's an error
        if(not ("," in tableString)):
            return False

        tableStringValues = tableString.split(",")
        return tableStringValues

    def processTableStrings(self, tableStrings, assignmentNum):
        # Go through list and turn them into a list of data
        results = []
        previousResults = []

        for tableString in tableStrings:
            tableStringValues = self.getTableStringValues(tableString)
            fileName1 = tableStringValues[1].strip().lower()
            fileName2 = tableStringValues[4].strip().lower()

            if self.testFileNaming(fileName1) and self.testFileNaming(fileName2):
                result = Result(assignmentNum, fileName1, fileName2, tableStringValues[0].strip(), int(tableStringValues[2]), int(tableStringValues[5]), int(tableStringValues[6]))
                if result.nameOneIsPrevious() and result.nameTwoIsPrevious():
                    previousResults.append(result)
                else:
                    results.append(result)

        # Returns
        if len(results)>0:
            return results, True
        elif len(previousResults) > 0:
            return previousResults, True
        return None, False


    def testFileNaming(self, fileName):
        # we need an underscore to seperate username and the assignment name,
        #  _ is suppose to seperate, not precede the name
        if "_" in fileName and ("_" is not fileName[0]):
            return True

        return False

    def formatTableString(self,tableString):
        tableString.lstrip()
        tableString = tableString.replace("<td> a href", '')
        tableString = tableString.replace("a  <td> align right", '')
        tableString = tableString.replace("a       ", '')
        tableString=tableString.replace("  http://",'http://')
        tableString=tableString.replace("  ",",")
        tableString=tableString.replace(" ",", ")
        tableString=tableString.replace(" (","(")
        tableString=tableString.replace("(","")
        tableString=tableString.replace(")","")
        tableString=tableString.replace("%","")
        tableString = tableString.replace(" ","")
        return tableString

#
# Inner class myHtmlParser extends HTMLParser
#
class myHtmlParser (HTMLParser):
    tableString=""
    seenTable=False
    seenEndOfTable=False

    def handle_starttag(self, tag, attrs):
        if(self.seenTable and (not self.seenEndOfTable)):
            if(tag=="tr" or tag=="td"):
                self.tableString = self.tableString + "<"+tag+">" + " "
            else:
                self.tableString=self.tableString+tag+" "
            for attr in attrs:
                tupleList=list(attr)
                for item in tupleList:
                    self.tableString=self.tableString+item+" "
        if(tag=="table"):
            self.seenTable=True

    def handle_endtag(self, tag):
        if(self.seenTable and (not self.seenEndOfTable)):
            if(tag=="table"):
                self.seenEndOfTable=True
            else:
               self.tableString=self.tableString+tag+" "

    def handle_data(self, data):
        if(self.seenTable and (not self.seenEndOfTable)):
             self.tableString = self.tableString + data + " "
