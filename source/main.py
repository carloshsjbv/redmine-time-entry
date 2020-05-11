from yattag import Doc
import requests

CONST_FILENAME = 'horas2.csv'

redmineKey = '284b8c7b863b7702a33584e1234406b0ee97e824'
redmineURL = 'http://srvredmine.hst.br/issues/'

def main():

    f = open(CONST_FILENAME, 'r')
    
    index = 0
    header = ''

    for line in f:

        if (index == 0):
            header = line.split(',')
            index += 1
        else:
            details = line.split(',')

            xmlDoc = buildXML(header, details)
            
            doPost(xmlDoc, index)

            index += 1
            print(xmlDoc.getvalue())

def buildXML(header, details):

    doc, tag, text = Doc().tagtext()

    with tag('time_entry'):
        for i in range(len(details)):
            with tag(header[i]):
                text(details[i])

    return doc
        
def doPost(xmlDoc, index):

    try:
        headers = {'Content-Type': 'application/xml'}

        httpRequest = requests.post(redmineURL, data=xmlDoc, headers=headers, verify=False)

        processMessage = ''

        if httpRequest.status_code == 200:
            processMessage = 'line ' + index + ' OK'
        else:
            processMessage = 'There is a problem at line ' + index + '. Plase, consider processing it manualy'

        print(processMessage)

        writeMessageInReportFile(processMessage)

    except Exception as e:
        print('There were problems to connect to readmine, this commit is going to be stored into ## FEATURES WITHOUT CARDS session')    
        return None

def writeMessageInReportFile(processMessage):

    reportFilename = 'report-' + CONST_FILENAME
    
    try:

        f = open(reportFilename, "x")
        f = open(reportFilename, "a")
        
        f.write(processMessage)

    except:
        print('Error while writing report file')
    finally:
        f.close()

if __name__ == '__main__':
    main()
else:
    print('me executou como um módulo')

