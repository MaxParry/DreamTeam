import pandas as pd

data = pd.read_csv("kc_house_data.csv")
print(len(data))
data = data.drop_duplicates(subset='id', keep='first')
print(len(data))

data['lat_group'] = ""
data['long_group']=''

max_long = max(data['long'])
min_long = min(data['long'])
max_lat = max(data['lat'])
min_lat = min(data['lat'])

print('max_long: ', max_long)
print('min_long: ', min_long)
print('max_lat: ', max_lat)
print('min_lat: ', min_lat)

iter_long = (max_long-min_long)/43
iter_lat = (max_lat-min_lat)/56

lat_list = []
long_list = []

for i, row in data.iterrows():
    if i%1000 ==0:
        print(i)
    grouped_lat ='n'
    lat = min_lat
    while lat <= max_lat+iter_lat and grouped_lat == 'n':
        lat_test = data.get_value(i, 'lat', takeable=False)
        if lat_test <= lat:
            lat_group = lat
            lat_list.append(lat - (iter_lat)/2)
            grouped_lat = 'y'
            #print(lat - (iter_lat)/2)
        else:
            lat = lat + iter_lat
            #print('else')
            
    grouped_long = 'n'
    long = min_long
    while long <= max_long+iter_long and grouped_long == 'n':
        long_test = data.get_value(i, 'long', takeable=False)
        if long_test <= long:
            long_group = long
            long_list.append(long - (iter_long)/2)
            grouped_long = 'y'
        else:
            long = long + iter_long
            
lat_se = pd.Series(lat_list)
long_se = pd.Series(long_list)

data['lat_group'] = lat_se.values
data['long_group']=long_se.values


writer = pd.ExcelWriter('lat_lon_grouped.xlsx')
data.to_excel(writer,'data')