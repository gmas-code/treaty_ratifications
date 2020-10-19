# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:19:57 2020

@author: gusta
"""
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

# Idea is to merge these 9 treaty datasets, as modified for a date difference, and 4 independent variable datasets.

# os.chdir(wherever your data is stored)

iccpr = pd.read_excel("UnderlyingData_ICCPR_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
icescr = pd.read_excel("UnderlyingData_ICESCR_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
icerd = pd.read_excel("UnderlyingData_ICERD_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
cedaw = pd.read_excel("UnderlyingData_CEDAW_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
crc = pd.read_excel("UnderlyingData_CRC_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
catc = pd.read_excel("UnderlyingData_CAT_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
crpd = pd.read_excel("UnderlyingData_CRPD_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
crmw = pd.read_excel("UnderlyingData_ICRMW_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)
ced = pd.read_excel("UnderlyingData_CPED_OHCHR_19_09_2020.xls",skiprows=[0],nrows=198)

#Critical dates as gathered in a quick search. There is probably a mistake here, but it is just a matter
# of fact checkind latter

# sdate_iccpr = pd.to_datetime("1966-12-06")
# sdate_iescr =  pd.to_datetime("1966-12-06")
# sdate_icerd =  pd.to_datetime("1965-12-21")
# sdate_cedaw =  pd.to_datetime("1980-03-01")
# sdate_crc =  pd.to_datetime("1989-11-20")
# sdate_catc =  pd.to_datetime("1984-12-10")
# sdate_crpd =  pd.to_datetime("1990-12-18")
# sdate_crwm =  pd.to_datetime("2007-02-06")
# sdate_ced =  pd.to_datetime("2007-03-30")

iccpr['sdate'] = pd.to_datetime("1966-12-06")
icescr['sdate'] =  pd.to_datetime("1966-12-06")
icerd['sdate'] =  pd.to_datetime("1965-12-21")
cedaw['sdate'] =  pd.to_datetime("1980-03-01")
crc['sdate'] =  pd.to_datetime("1989-11-20")
catc['sdate'] =  pd.to_datetime("1984-12-10")
crpd['sdate'] =  pd.to_datetime("1990-12-18")
crmw['sdate'] =  pd.to_datetime("2007-02-06")
ced['sdate'] =  pd.to_datetime("2007-03-30")

#Getting the time differences

dataframes = [iccpr,icescr,icerd,cedaw,crc,catc,crpd,crmw,ced]
dataframes_names = 'iccpr, icescr, icerd, cedaw, crc, catc, crpd, crmw, ced'.split(', ')

# sdates = [sdate_iccpr,sdate_iescr,sdate_icerd,sdate_cedaw,sdate_crc, sdate_catc,sdate_crpd,sdate_crwm,sdate_ced]

            
# for i in dataframes:
#     for d in sdates:
#         i['difference']=(i['Date of Ratification/Accession']-d)

for df in dataframes:
    df['difference'] = df.apply(lambda row: row['Date of Ratification/Accession'] - row['sdate'], axis=1)

for df in dataframes:
    print(df.head())

#Leaving only time difference

# i = [i.drop(['Date of Signature (dd/mm/yyyy)'],axis=1,inplace=True) for i in dataframes]

# i = [i.drop(['Date of Ratification/Accession'],axis=1,inplace=True) for i in dataframes]

# i = [i.drop(['Date of acceptance of individual communications procedure'],axis=1,inplace=True) for i in dataframes]


# icescr.drop(['Date of acceptance of inquiry procedure'],axis=1,inplace=True)

# cedaw.drop(['Date of acceptance of inquiry procedure'],axis=1,inplace=True)

# crc.drop(['Date of acceptance of inquiry procedure'],axis=1,inplace=True)

# catc.drop(['Date of acceptance of inquiry procedure'],axis=1,inplace=True)

# crpd.drop(['Date of acceptance of inquiry procedure'],axis=1,inplace=True)

# ced.drop(['Date of acceptance of inquiry procedure'],axis=1,inplace=True)

for df in dataframes:
    try:
        df.drop(['Date of Signature (dd/mm/yyyy)', 'Date of Ratification/Accession', 'Date of acceptance of individual communications procedure', 'sdate'], axis=1, inplace=True)
        df.drop('Date of acceptance of inquiry procedure', axis=1, inplace=True)
    except:
        pass

# I wanted to transform "Country" to an index of rows to facilitate merging

for df in dataframes:
    df.set_index(keys='Country',inplace=True)

# I could not find a way to merge in loop without errors

# full = pd.merge(iccpr,icescr,left_index=True, right_index=True)
# full = pd.merge(full,icerd,left_index=True, right_index=True)
# full = pd.merge(full,cedaw,left_index=True, right_index=True)
# full = pd.merge(full,crc,left_index=True, right_index=True)
# full = pd.merge(full,catc,left_index=True, right_index=True)
# full = pd.merge(full,crpd,left_index=True, right_index=True)
# full = pd.merge(full,crmw,left_index=True, right_index=True)
# full = pd.merge(full,ced,left_index=True, right_index=True)

full_df = pd.concat(dataframes, keys=dataframes_names, axis=1)
print(full.head())

   
#Getting the other datasets for exog variables
#These are taken from Our World in Data

democracy = pd.read_csv('data/age-of-democracies (1).csv')
av_gdp =  pd.read_csv('data/average-real-gdp-per-capita-across-countries-and-regions (1).csv')
hdi = pd.read_csv('data/human-development-index (1).csv')
religion = pd.read_csv('data/main-religion-of-the-country-in (1).csv')

independents = [democracy,av_gdp,hdi,religion]

idps = [idps.rename({"Entity":"Country"},axis=1,inplace=True) for idps in independents]

for i in independents:
    i.set_index(keys='Country',inplace=True)

# This part of the merge does not work

full = pd.merge(full,democracy,left_index=True, right_index=True)
full = pd.merge(full,av_gdp,left_index=True, right_index=True)
full = pd.merge(full,hdi,left_index=True, right_index=True)
full = pd.merge(full,religion,left_index=True, right_index=True)

# End result is not what is intended
full.info()

