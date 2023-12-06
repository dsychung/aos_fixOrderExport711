#!/usr/bin/env python
# coding: utf-8

# In[7]:


#export excel for 711

import pandas as pd
import numpy as np

input_excel_name = 'modified2_orders_export_711_20231205'
output_excel_name ='modified2_orders_export_711_20231205-output'

df = pd.read_excel('./source/'+input_excel_name+'.xlsx')  

def fixdate():
    datetimeVal = df['訂購日期']
    # print(datetimeVal[0])
    datetimeVal=datetimeVal[0].replace("/","")
    # print(datetimeVal)
    return datetimeVal

def export_to_excel_file(df,fname):
    df.to_excel('output/'+fname+'.xlsx', index = False)      
    
def createExtraRowForShipping(df):
    #create extra rows for 運費
    for index, row in df.iterrows():
        if row['運費'] != 0:    
            #print(row['訂單編號'])
            d = {'訂單編號': [row['訂單編號']], 
                 '出貨日期1': [row['出貨日期1']], 
                 '收件人':[row['收件人']],
                 '購買數量':[row['購買數量']],
                 '地址':[row['地址']],
                 '郵遞區號 (Billing)':[row['郵遞區號 (Billing)']],
                 '手機 (Billing)':[row['手機 (Billing)']],
                 '運費':[row['運費']],
                 '商品名稱':['運費'],
                 '購買金額':[row['購買金額']],
                 '訂單總金額':[row['訂單總金額']],
                 'Email (Billing)':[row['Email (Billing)']],
                 '配送方式':[row['配送方式']]
                }
            df2 = pd.DataFrame(data=d)        
            df = df.append(df2, ignore_index=True)
    return df
    
def renameColumnNames(df):
    #rename column names
    df = df.rename(columns = {     '商品總額\n(A+B-C-D-E)': '購買金額',
                                   '數量': '購買數量',
                                   '商品名稱\n(品名/規格)':'商品名稱',
                                   '取件地址':'地址', 
                                   '收件人姓名':'收件人'}, inplace = False)
    return df

def drop_duplicated_shippings(df):
    df = df.drop_duplicates(subset=['出貨日期', '訂單編號', '商品名稱'])
    return df

def drop_duplicated_shipping_fee(df):
    for index, row in df.iterrows():
        #print(df.iloc[index]['出貨日期'])
        #print(df.iloc[index-1]['出貨日期'])
        if (df.iloc[index]['出貨日期'] == df.iloc[index-1]['出貨日期']) and (df.iloc[index]['訂單編號'] == df.iloc[index-1]['訂單編號']) and (df.iloc[index]['運費'] == df.iloc[index-1]['運費'] == 420):
            #print(df.iloc[index]['訂單編號'])
            #remove 同訂單的previous運費
            df.iloc[(index-1), df.columns.get_loc('運費')] = 0    
    return df


#main program----------------------------------------------------------

df['出貨日期'] = fixdate()

df = renameColumnNames(df)

# #copy a df for export
df_for_export = df[['出貨日期', '收件人', '地址', '訂單編號', '購買數量','購買金額','商品名稱']].copy()

print(df_for_export)

# #add empty column
df_for_export["規格名稱"] = ""
df_for_export["商品編號"] = ""
df_for_export["訂單日期"] = ""
df_for_export["貨運單號"] = ""
df_for_export["發票統編"] = ""
df_for_export["發票抬頭"] = ""
df_for_export["手機"] = ""
df_for_export["郵遞區號"] = ""
df_for_export["配送方式"] = ""
df_for_export["運費"] = ""
df_for_export["發票通知e-mail"] = ""
df_for_export["Customer Note"] = ""


# #change column order
df_for_export = df_for_export[['出貨日期', '訂單編號', '商品編號', '商品名稱', '規格名稱', '購買數量', '購買金額', '訂單日期', '收件人', '手機',
                     '郵遞區號','地址','配送方式','貨運單號','發票統編','發票抬頭','運費','發票通知e-mail','Customer Note']]


# In[8]:


#for col in df.columns: 
 #   print(col) 


# In[9]:


fname = output_excel_name
export_to_excel_file(df_for_export,fname)


# In[ ]:




