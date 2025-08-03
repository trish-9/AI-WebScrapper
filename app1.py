from tkinter import *
from tkinter import ttk
from  selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep 
import pandas as pd 
import sqlite3 as sql
sqli = sql.connect("database.db")

chrom = Options()
chrom.add_argument("--headless=new")
dri = webdriver.Chrome(options=chrom)
dri.get("https://faridabad.dcourts.gov.in/case-status-search-by-case-number")
dri1 = webdriver.Chrome()
image_element = dri.find_element(By.ID, "siwp_captcha_image_0")
image_id = image_element.get_attribute("src")
dri1.get(image_id)
#sleep(60)
s = Tk()
s.title("WEB SCRAPPER")
s.geometry('500x500')
l = Label(s , text = "Web Scrapper",font = 120)
l.pack()
w = Label(s, text = "Case Type",font=70)
w.place(x = 80 , y = 60)
c = ttk.Combobox(s , values=["446 CR.P.C","APP","ARB","BA","CA","CHA","CHI","CMA","CM APPLI","COMA","COMI","COMMERCIAL APPEAL","COMMERCIAL SUIT","CP","CR","CRA","CRM","CRMP","CRR","CS","CS37","DMC","ELC","EP","EXE","FD","GW","HAMA","HDRA","HMA","HMCA","INDIG","INDIGA","INSO","IT ACT","JJB","LAC","LAC EXE","LAC MISC","MACM","MACM-FORM1","MACP","MHA","MNT125","MPL","MPLA","NACT","NDPS","OBJ","PC","PFC","PP","PRI","PROB","RA","REMP","REW APP","RP","SC","SUCC","SUMM","TA","TELA ACT","TELE ACT","TRA","UCR","WKF"])
c.place(x = 200 , y = 60)
w1 = Label(s , text = "Case Number" , font = 70)
w1.place(x = 80 , y = 120)
e = Entry(s , width=23)
e.place(x = 200 , y = 125)
w2 = Label(s , text = "Year",font = 70)
w2.place(x =80 , y = 176 )
e1 = Entry(s , width=23)
e1.place(x = 200 , y = 178)
w3 = Label(s , text = "Catcha" , font = 70)
w3.place(x = 80 , y = 232)
e2 = Entry(s ,width=23 )
e2.place(x =200 , y= 231 )
w4 = Label(s , text = "NOTE - Please Fill the Captcha after opening other link for Captcha in Browser")
w4.place(x = 74 , y = 290)
def pop():
    l = dri.find_element(By.NAME,"est_code")
    l.send_keys("District Court , Faridabad")

    l1 = dri.find_element(By.NAME , "case_type")
    sleep(10)
#WebDriverWait(dri, 10).until(EC.presence_of_element_located((By.XPATH, "//select[@name='case_type']/option[text()='CA']")))
    sele = Select(l1)
    sleep(10)
    sele.select_by_visible_text(c.get())

    l2 = dri.find_element(By.NAME,"reg_no")

    l2.click()
    l2.send_keys(int(e.get()))

    l3 = dri.find_element(By.NAME,"reg_year")

    l3.click()
    l3.send_keys(int(e1.get()))
    l4 = dri.find_element(By.NAME , "siwp_captcha_value")
    l4.click()
    l4.send_keys(e2.get())
    l5 = dri.find_element(By.NAME,"submit")
    sleep(10)
    l5.click()
    sleep(20)
    l6 = dri.find_element(By.LINK_TEXT,"View")
    l6.click()
    sleep(20)

    v = dri.find_element(By.XPATH,'//*[@id="cnrResultsDetails"]/div[2]/table/tbody/tr/td[6]/span')
    print(v.text)
    f = dri.find_element(By.TAG_NAME,'td')
    print(f.text)

    l9 = []
    l10 = []
    for a in range(1,50):
        try:
          t = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[7]/table/tbody/tr[{a}]/td[1]/span')
          t1 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[6]/table/tbody/tr[{a}]/td[1]/span')
          if int(t.text) == a:
             l9.append(a)
          if str(t1.text) == str(t1.text):
              l10.append(a)
            
          else:
             exit()
        except:
            pass
    
    order_number = []
    order_date = []
    order_detail = []
    for b in range(1,len(l9)+1):
        po = dri.find_element(By.XPATH ,f'//*[@id="cnrResultsDetails"]/div[7]/table/tbody/tr[{b}]/td[1]/span')
        order_number.append(po.text)
        po1 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[7]/table/tbody/tr[{b}]/td[2]/span')
        order_date.append(po1.text)
    

    po21 = dri.find_elements(By.LINK_TEXT,'Copy of order')
    for link in po21:
        mb = link.get_attribute("href")
        print(mb)
        dri1.get(mb)
        order_detail.append(mb)
    for xy in range(len(order_detail)):
        
       
        d122xy = webdriver.Chrome()
        d122xy.get(order_detail[xy])
        
    data = {"order_number":order_number,"order_date":order_date,"order_detail":order_detail}
    s45 = pd.DataFrame(data)
    s45.to_sql("order",sqli)
    print(s45["order_detail"])
    lcase = []
    for cv in range(1,7):
        x1 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[2]/table/tbody/tr/td[{cv}]/span')
        lcase.append(x1.text)
    l = {'Case Type':lcase[0],'filling Number':lcase[1],'Filling date':lcase[2],'Registration Number':lcase[3],'Registration Date':lcase[4],'CNR Number':lcase[5]}
    data1 = pd.DataFrame(l,index = [0])
    data1.to_sql("case_detail",sqli)
    print(data1)
    casest = []
    for casi in range(1,6):
        x2 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[3]/table/tbody/tr/td[{casi}]/span')
        casest.append(x2.text)
        
    luh = {'f_Hearing Date':casest[0],'N_Hearing Date':casest[1],'Case Status':casest[2],'Stage_of_Case':casest[3],'Crt_no and Judge':casest[4]}
    data2 = pd.DataFrame(luh , index = [0])
    data2.to_sql("case_status",sqli)
    print(data2)
    act = []
    for acti in range(1,3):
        x3 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[5]/table/tbody/tr/td[{acti}]/span')
        act.append(x3.text)
    luh1 = {'under_act':act[0],'under_sec':act[1]}
    data3 = pd.DataFrame(luh1,index = [0])
    data3.to_sql("acts",sqli)
    print(data3)
    try:
       asl = []
       asl1 = []
       asl2 = []
       asl3 = []
       asl4 = []
       for acto in range(1,len(l10)+1):
           asx = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[6]/table/tbody/tr[{acto}]/td[1]/span')
           asl.append(asx.text)
           asx1 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[6]/table/tbody/tr[{acto}]/td[2]/span')
           asl1.append(asx1.text)
           asx2 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[6]/table/tbody/tr[{acto}]/td[3]/span')
           asl2.append(asx2.text)
           asx3 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[6]/table/tbody/tr[{acto}]/td[4]/span')
           asl3.append(asx3.text)
           asx4 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[6]/table/tbody/tr[{acto}]/td[5]/span')
           asl4.append(asx4.text)
       data4 = {"Registration_no":asl , "judge":asl1,"buss_on_date":asl2,"hearing_on_date":asl3,"purpose_of_hearing":asl4}
       sfv = pd.DataFrame(data4)
       sfv.to_sql("case_history",sqli)
       print(sfv)
    except:
        pass
    try:
        asd1 = []
        asd2 = []
        asd3 = []
        asd4 = []
        asd5 = []
        for cd3 in range(1,3):
            as3 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[8]/table/tbody/tr[{cd3}]/td[1]/span')
            asd1.append(as3.text)
            as31 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[8]/table/tbody/tr[{cd3}]/td[2]/span')
            asd2.append(as31.text)
            as32 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[8]/table/tbody/tr[{cd3}]/td[3]/span')
            asd3.append(as32.text)
            as33 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[8]/table/tbody/tr[{cd3}]/td[4]/span')
            asd4.append(as33.text)
            as34 = dri.find_element(By.XPATH,f'//*[@id="cnrResultsDetails"]/div[8]/table/tbody/tr[{cd3}]/td[5]/span')
            asd5.append(as34.text)
            lhg = {"process_id":asd1,"process_date":asd2,"process_title":asd3,"party_name":asd4,"issure_proc":asd5}
        data5 = pd.DataFrame(lhg)
        data5.to_sql("process_detail",sqli)
        print(data5)
    except:
        pass
b = Button(s , text = "Submit Carefully" , width=15 , height=1 , command = pop)
b.place(x = 200 , y = 350)
s.mainloop()