
# coding: utf-8

# In[18]:


import pandas as pd
import seaborn as sns
import numpy as np

data = pd.read_csv("kc_house_data.csv")
data = data.drop_duplicates(subset=('id','lat','long','price'), keep='first')
data['lat_group'] = ''
data['long_group']=''

heat_data = pd.concat([data['price'], data['long'], data['lat']], axis=1, keys=['price', 'long','lat'])
heat_data = heat_data.reset_index()
heat_data = heat_data.groupby(['lat', 'long']).mean()
heat_data = heat_data.reset_index()
heat_data.head()


# In[27]:


max_price = max(data['price'])
min_price = min(data['price'])
print('max_price: ', max_price)
print('min_price: ', min_price)


# In[52]:


heat = heat_data.pivot(index="lat", columns="long", values="price")
ax = sns.heatmap(heat,vmin=min_price, vmax=max_price,cmap="gist_rainbow",center=250000) #gist_rainbow


# In[53]:


print(ax)


# In[54]:


import matplotlib.pyplot as plt
plt.show()

