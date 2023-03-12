# MyBankCardManager , manage all your bank cards at one place :)
# Note : Before running this, make sure SQL Server is active

#--------------------------------------------------------------------------

DBACredentrials=["DBA707","Mercury80"]

Driver="ODBC Driver 17 for SQL Server"
ServerName="tcp:mybankcardsmanagerserver.database.windows.net,1433"
DatabaseName="MyBankCardsManager"
UserID="rootadmin"
Password="redplanetMARS07"

port=7000

#---------------------------------------------------------------------------

#- - - - - -
def install(package):
    # This function will install a package if it is not present
    from importlib import import_module
    try:
        import_module(package)
    except:
        from sys import executable as se
        from subprocess import check_call
        check_call([se,'-m','pip','-q','install',package])


for package in ['flask','pymongo','time','pathlib','pypyodbc','csv','threading','codecs','pandas','os']:
    install(package)
#- - - - - -
    
from flask import *
import pymongo
import time
from pathlib import Path
import pypyodbc
import csv
import threading
import codecs
import pandas as pd
import os

# Global Variables

app=Flask(__name__) 

GenuineDBA=True
FailCount=0
driver='Driver={ODBC Driver 17 for SQL Server};Server=tcp:mybankcardsmanagerserver.database.windows.net,1433;Database=MyBankCardsManager;Uid=rootadmin;Pwd={redplanetMARS07};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
original=[]
superoriginal=[]
makeinaccessable=False
mystr=""
def getTabData(driver, TableName, allFields=True):
    cnxn = pypyodbc.connect(driver, autocommit=True)
    mydb=cnxn
    
    cursorObject = mydb.cursor()
    fetchQuery="SELECT * FROM "+TableName
    if not allFields:
        cols=""
        for i in Columns[0:-1]:
            cols+=i
            cols+=","
        cols+=Columns[-1]
        fetchQuery="SELECT "+cols+" FROM "+TableName
        
    cursorObject.execute(fetchQuery)
    myresult = cursorObject.fetchall()
    tableData=[]
    for i in myresult:
        tableData.append(i)
    return tableData

def ComputeOriginal():
    global original
    TableName='original'
    originald=getTabData(driver, TableName, allFields=True)
    for r in originald:
        r=list(r)
        original.append(tuple(r[1:-1]))
def ComputeSuperOriginal():
    global superoriginal
    TableName='superoriginal'
    originald=getTabData(driver, TableName, allFields=True)
    for r in originald:
        r=list(r)
        superoriginal.append(tuple(r[0:-1]))

def sendAlertMail():
    
    import smtplib

    # list of email_id to send the mail
    li = ["ramzno1@gmail.com","joelvar541@gmail.com"]

    for dest in li:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("mybankcardsmanager.alert@gmail.com", "qmejfglvkqmetgdo")
            mail_subject='Intrusion Alter [Important]'
            mail_body='Hey User, System has detected an Intrusion attempt to breach information stored on Azure Databse Server. The access has been diverted. Kindly secure the servers.'
            message = 'Subject: {}\n\n{}'.format(mail_subject, mail_body)
            #message = "tst"
            s.sendmail("sender_email_id", dest, message)
            s.quit()

def killProcessRunningAtPort(port):
    import subprocess
    port=str(port)
    command="netstat -ano | findstr :"+port
    output=subprocess.getoutput(command).split('\n')
    PIDs=[]
    for i in output:
        if "127.0.0.1:"+port in i and "LISTENING" in i:
            PIDs.append(i.split()[-1])
    for i in PIDs:
        subprocess.getoutput("taskkill /PID "+i+" /F") 
        
@app.route('/MyBankCardsManager') #ONE
def fun1():
    time.sleep(1)
    FailCount==0
    GenuineDBA=True
    return render_template("1.EntryPage.html")


@app.route('/MyBankCardsManager/ThisIsDBA') #TWO
def home():
    time.sleep(1)
    FailCount==0
    GenuineDBA=True
    return render_template("2.AuthenticateDBA.html")


@app.route('/MyBankCardsManager/AuthenticateAgain') #THREE
def home2():
    time.sleep(1)
    return render_template("3.AuthenticateAgain.html")


@app.route('/MyBankCardsManager/DBAMenu') #Four
def home3():
    time.sleep(1)
    return render_template("4.DBAMenu.html")

@app.route('/MyBankCardsManager/ProcessDBAdata',methods = ['GET'])
def processthedata():
    DBACode=request.args.get('DBACode')  
    Password=request.args.get('Password')
    global FailCount
    global GenuineDBA
    if str(DBACode)==DBACredentrials[0]:
        if str(Password)==DBACredentrials[1]:
            if FailCount==0 or FailCount==1:
                GenuineDBA=True
            return redirect("http://localhost:7000/MyBankCardsManager/DBAMenu")
        else:
            FailCount+=1
            
            if FailCount==3:
                GenuineDBA=False
                return redirect("http://localhost:7000/MyBankCardsManager/DBAMenu")
            
            return redirect("http://localhost:7000/MyBankCardsManager/AuthenticateAgain")
    else:
        FailCount+=1
        if FailCount==3:
            GenuineDBA=False
            sendAlertMail()
            return redirect("http://localhost:7000/MyBankCardsManager/DBAMenu")
        return redirect("http://localhost:7000/MyBankCardsManager/AuthenticateAgain")


@app.route('/MyBankCardsManager/DBAMenu/DropDB') # FIVE
def DropDB():
    global original
    global superoriginal
    time.sleep(2)
    original=['Database made inaccessible']
    superoriginal=['NULL, 0 records selected']
    return "<h1>Dropped the database</h1>"
@app.route('/MyBankCardsManager/DBAMenu/AddEntry') # SIX
def AddEntry():
    time.sleep(1)
    return render_template("6.AddEntry.html")

@app.route('/MyBankCardsManager/DBAMenu/ViewDatabase') # Seven
def ViewDatabase():
    time.sleep(1)
    global makeinaccessable
    global mystr
    mystr=''
    temp=''
    if GenuineDBA==True:
        
        mystr="<h1> ORIGINAL DATABASE </h1><br>"
        mystr+="<h5>"
        for i in original:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        if makeinaccessable:
            return "<h1> Database InAccessable!! </h1>"
        return temp
        
    else:
        mystr="<h1> HONEYPOT DATABASE </h1><br>"
        mystr+="<h5>"
        for i in superoriginal:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        makeinaccessable=True
        return temp

@app.route('/MyBankCardsManager/DBAMenu/DownloadDB')
def DownloadDB():
    time.sleep(1)
    downloads_path = str(Path.home() / "Downloads")
    #return str(downloads_path)
    #return 'hello'
    p=downloads_path.replace('\\','/')
    print(p)
    p+='/MyBankCardsManagerDatabase.txt'
    d=open(p,'w')
    data=[]
    if GenuineDBA:
        data=original+[]
    else:
        data=superoriginal+[]
    for i in data:
        i=str(i)+'\n'
        d.write(i)

    d.close()
    
    
    if GenuineDBA:
        return "<h1>Database Downloaded</h1>"
    else:
        return "<h1>Database Downloaded</h1>"
@app.route('/MyBankCardsManager/DBAMenu/AddEntryData',methods=['GET'])
def AddEntryData():
    time.sleep(1)
    CName=request.args.get('CName')
    CNumber=request.args.get('CNum')
    CExpiry=request.args.get('CExpiry')
    CCVV=request.args.get('CCVV')
    record={'username':'DBA707', 'CardName':str(CName), 'CardNumber':str(CNumber), 'Expiry':str(CExpiry), 'CVV':str(CCVV)}
    record=(CName,'National Bank',CNumber,CExpiry,CCVV)
  
    if GenuineDBA:
        original.append(record)
    else:
        superoriginal.append(record)
    return render_template("9.EntrySuccessful.html")
    
def DBADone():
    return render_template("DBADone.html")
if __name__ =='__main__':
    killProcessRunningAtPort(port)
    ComputeOriginal()
    ComputeSuperOriginal()
    print("To access application, go to:","http://127.0.0.1:"+str(port)+"/MyBankCardsManager\n\n\nServer Traffic and other details:\n")
    app.run(host="localhost", port=port,debug = True)

    
