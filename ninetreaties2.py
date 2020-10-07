# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:57:25 2020

@author: gusta
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
import patsy


iccpr = pd.read_excel("UnderlyingData_ICCPR_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
icescr = pd.read_excel("UnderlyingData_ICESCR_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
icerd = pd.read_excel("UnderlyingData_ICERD_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
cedaw = pd.read_excel("UnderlyingData_CEDAW_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
crc = pd.read_excel("UnderlyingData_CRC_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
catc = pd.read_excel("UnderlyingData_CAT_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
crpd = pd.read_excel("UnderlyingData_CRPD_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
crmw = pd.read_excel("UnderlyingData_ICRMW_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
ced = pd.read_excel("UnderlyingData_CPED_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)

#Critical dates as gathered in a quick search

sdate_iccpr = pd.to_datetime("1966-12-06")
sdate_iescr =  pd.to_datetime("1966-12-06")
sdate_icerd =  pd.to_datetime("1965-12-21")
sdate_cedaw =  pd.to_datetime("1980-03-01")
sdate_crc =  pd.to_datetime("1989-11-20")
sdate_catc =  pd.to_datetime("1984-12-10")
sdate_crpd =  pd.to_datetime("1990-12-18")
sdate_crwm =  pd.to_datetime("2007-02-06")
sdate_ced =  pd.to_datetime("2007-03-30")

#Getting the time differences

dataframes = [iccpr,icescr,icerd,cedaw,crc,catc,crpd,crmw,ced]

sdates = [sdate_iccpr,sdate_iescr,sdate_icerd,sdate_cedaw,sdate_crc, sdate_catc,sdate_crpd,sdate_crwm,sdate_ced]

            
for i in dataframes:
    for d in sdates:
        i['difference']=(i['Date of Ratification/Accession']-d)

for i in dataframes:
    i['difference']=i['difference'].dt.days

## Wrong way of doing it
##for i in dataframes:
##    i['difference'] = pd.to_numeric(i['difference'])

var_list =[]

for i in dataframes:
    var_list.append(np.var(i['difference']))


#Leaving only time difference

i = [i.drop(['Date of Signature (dd/mm/yyyy)','Date of Ratification/Accession'],axis=1,inplace=True) for i in dataframes]

#Getting the other datasets (experimental)
#These are taken from Our World in Data

democracy = pd.read_csv('data/age-of-democracies (1).csv')
av_gdp =  pd.read_csv('data/average-real-gdp-per-capita-across-countries-and-regions (1).csv')
hdi = pd.read_csv('data/human-development-index (1).csv')
religion = pd.read_csv('data/main-religion-of-the-country-in (1).csv')

independents = [democracy,av_gdp,hdi,religion]

idps = [idps.rename({"Entity":"Country"},axis=1,inplace=True) for idps in independents]

#An experimental merge. Quite messy.

id2 = [iccpr, democracy,av_gdp,hdi,religion]

id2 = [iccpr, democracy,av_gdp,hdi,religion]

id3 = [iccpr,icescr,icerd,cedaw,crc,catc,crpd,crmw,ced,democracy,av_gdp,hdi,religion]

result = pd.concat([independents], axis=1,join='inner',keys='Country')
result2 = pd.concat(id2, axis=1,join='inner',keys='Country')
results3 = pd.concat(id3, axis=1,join='inner',keys='Country')


iccpr2 = iccpr.merge(democracy,on="Country")
iccpr2 = iccpr2.merge(av_gdp,on="Country")
iccpr2 = iccpr2.merge(hdi,on="Country")
iccpr2 = iccpr2.merge(religion,on="Country")


iccpr2.drop(['Code_x','Code_y', 'Year_x','Code_x', 'Year_y','Code_y'],axis=1,inplace=True)
iccpr2.head()
iccpr2.columns
iccpr2.rename({'Date of Ratification/Accession':'Date',
       'Age of democracies at the end of 2015 (Boix, Miller, and Rosato, 2013, 2018)':'Age',
       'Real GDP per capita in 2011US$, multiple benchmarks (Maddison Project Database (2018))':'AvGDP',
       'Human Development Index (UNDP)':'GDP', 'Main religion ':'Religion'},axis=1,inplace=True)

iccpr2.head()

pd.plotting.scatter_matrix(result2)

iccpr2['Age']=iccpr2['Age'].replace('Not a democracy in 2015',0)

iccpr2['Age'] = pd.to_numeric(iccpr2['Age'])
mod3 = smf.ols(formula='difference ~ Age',data=iccpr2)
res = mod3.fit()
print(res.summary())

iccpr2.to_csv('iccpr2.csv')


patsy.dmatrices('difference ~ Age',data=iccpr2)











