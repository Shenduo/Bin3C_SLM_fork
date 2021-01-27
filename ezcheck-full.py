#!/usr/bin/env python
# coding: utf-8

# In[233]:


import pandas as pd
import numpy as np
from ast import literal_eval
import sys
import argparse
import os


# In[9]:


# argument
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="path", help="Input CheckM summary table. Must be .tsv or .csv")
parser.add_argument("-f", "--FullTree", action="store_true", help="Full Tree CheckM summary table or not.")
parser.add_argument("-o", "--output", default="", help="Store Full Tree CheckM summary table as normal format, and output to the target path.")
args = parser.parse_args()


# In[3]:


filepath = args.path.split('.')
if (filepath[-1] != 'tsv') and (filepath[-1] != 'csv'):
    print(type(filepath[-1]))
    print('Summary table format must be .tsv or .csv')
    sys.exit(0)
elif args.FullTree:
    # 讀入需要被矯正的檔案&依照CL編號排序
    df_f = pd.read_csv(args.path, sep='\t', header=None)
    df_f = df_f.sort_values(by=[0])
    df_f = df_f.reset_index(drop=True)
    # 建立已排序的df
    d = {'Bin Name': df_f[0].values}
    df = pd.DataFrame(data=d)
    # 對所有df_f的第二欄進行拆解，取得所需欄位做成 len(row) x 12 的 array
    needcol = ['marker lineage', '# genomes', '# markers', '# marker sets', '0', '1', '2', '3', '4', '5+', 'Completeness', 'Contamination']
    list_tep = []
    for i in range(len(df_f)):
        dic = literal_eval(df_f[1][i])
        row = list(map(dic.get, needcol))
        list_tep.append(row)
    # 拆解完成，合併dataframe
    df_tep = pd.DataFrame(list_tep, columns=needcol)
    df = pd.concat([df, df_tep], axis=1)
    # 如果有輸入路徑，儲存df
    if args.output:
        outpath, outfile = os.path.split(args.output)
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        df.to_csv(args.output, index=False)
elif filepath[-1] == 'tsv':
    df = pd.read_csv(args.path, sep='\t')
else:
    df = pd.read_csv(args.path)


# In[227]:


## 這邊以下是測試


# In[221]:


# ## 這邊做個整理，上面太亂
# # 讀入需要被矯正的檔案&依照CL編號排序
# df_f = pd.read_csv("/Users/chloecheng/Desktop/bin_stats_ext.tsv", sep='\t', header=None)
# df_f = df_f.sort_values(by=[0])
# df_f = df_f.reset_index(drop=True)
# # 建立已排序的df
# d = {'Bin Name': df_f[0].values}
# df = pd.DataFrame(data=d)


# In[223]:


# # 對所有df的第二欄進行拆解，取得所需欄位做成 1072 x 12 的 array
# needcol = ['marker lineage', '# genomes', '# markers', '# marker sets', '0', '1', '2', '3', '4', '5+', 'Completeness', 'Contamination']

# list_tep = []
# for i in range(len(df)):
#     dic = literal_eval(df[1][i])
#     row = list(map(dic.get, needcol))
#     list_tep.append(row)
    
# df_tep = pd.DataFrame(list_tep, columns=needcol)


# In[225]:


# df_final = pd.concat([df_final, df_tep], axis=1)
# df_final


# In[226]:


## 這邊以上是測試


# In[27]:


# Near Completeness>=90, Contamination<=5
mask1 = df['Completeness']>=90 
mask2 = df['Contamination']<=5
near = len(df[(mask1 & mask2)])
#df[(mask1 & mask2)]


# In[29]:


# Substantial 90>Completeness>=70, 5<Contamination<=10
# 包含兩種特別情況: 完成度>90但污染度>5 & 完成度>=70但污染度<5
mask1 = df['Completeness']>=70
mask2 = df['Completeness']<90 
mask3 = df['Contamination']>5
mask4 = df['Contamination']<=10
sub = len(df[((mask1 & mask2 & mask4)|(mask1 & mask3 & mask4))])
#df[((mask1 & mask2 & mask4)|(mask1 & mask3 & mask4))]


# In[32]:


# Moderate 70>Completeness>=50, 10<Contamination<=15
# 包含兩種特別情況: 完成度>70但污染度>10 & 完成度>=50但污染度<10
mask1 = df['Completeness']>=50
mask2 = df['Completeness']<70 
mask3 = df['Contamination']>10
mask4 = df['Contamination']<=15
mod = len(df[((mask1 & mask2 & mask4)|(mask1 & mask3 & mask4))])
#df[((mask1 & mask2 & mask4)|(mask1 & mask3 & mask4))]


# In[33]:


# output the results
print('total:', len(df))
print('Near:', near)
print('Substantial:', sub)
print('Moderate:', mod)

