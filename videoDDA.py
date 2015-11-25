from pymarc import *
import time
import csv
import tkinter
import os
# import codecs
# import unicodedata

root = tkinter.Tk()
root.withdraw()

def readPDAList():
    """
    update PDA Title list with the following query:
    select b.Z13U_REC_KEY, a.Z13_TITLE, a.Z13_IMPRINT, b.Z13U_USER_DEFINED_4 AS Control_Number, a.Z13_UPDATE_DATE, a.*
    from PDA01.Z13 a
    join PDA01.z13u b on a.Z13_REC_KEY = b.Z13U_REC_KEY
    where 1=1
    and Z13U_USER_DEFINED_5 = 'FA'
    and b.Z13U_USER_DEFINED_1 = 'VM'
    """
    pdaListFile = 'Kanopy.csv'

    pdaList = []

    with open(pdaListFile, 'r') as csvf:
            u = csv.reader(csvf)
            for row in u:
                pdaList.append(row)

    return pdaList

def cleanText(title):

    title = title.rstrip()
    textToRemove = ['-', ':', ',', '.']

    for txt in textToRemove:
        title = title.replace(txt,'')

    title = title.replace(' ','')
    title = title.upper()
    return title

def writeResults(result):
    resultFile = 'video_dda_check_results.txt'
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    result = now+': '+result+'\n'
    with open(resultFile, 'a') as out:
        out.write(result)

def readMarcFile():
    pdaList = readPDAList()

    input('press any key to select the input MARC file...\n')
    from tkinter import filedialog
    marcPath = tkinter.filedialog.askopenfile()
    input('thanks! press any key to run the check...\n')

    marcFile = marcPath.name

    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)

        counter = 0
        for rec in reader:
            rec.force_utf8 = True
            counter += 1

            title = rec['245']['a']
            if rec['245']['b'] is not None:
                title = title+": "+str(rec['245']['b']).replace('/','')

            title = cleanText(title)

            for row in pdaList:

                rTitle = row[1]
                rTitle = cleanText(rTitle)

                if title == rTitle:
                    try:
                        recID = '('+str(rec['003'].value())+')'+str(rec['001'].value())
                    except:
                        recID = '(unknown)'
                    result = ('record '+str(counter)+', ID: '+str(recID)+' found in '+str(row))
                    writeResults(result)
                    # input('press any key to continue')
                    continue

    input('thanks! check finished! press any key to launch the log file')
    os.system("start "+'video_dda_check_results.txt')

readMarcFile()