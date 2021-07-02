def lon_lat_to_coords(lat, lon):
    return (int((lat+90.0)/.5), int((lon+180)/.625))
import os
import pandas as pd
import netCDF4 as nc4
def get_mean(arr):
    tot = 0
    for row in arr:
        for col in row:
            tot += col
    return tot / (len(arr) * len(arr[0]))
cities = {'Andhra Pradesh':(14.7504291,78.57002559),
    'Arunachal Pradesh':(27.10039878,93.61660071),
    'Assam':(26.7499809,94.21666744),
    'Bihar':(25.78541445,87.4799727),
    'Chandigarh':(30.71999697,76.78000565),
    'Chhattisgarh':(22.09042035,82.15998734),
    'Delhi':(28.6699929,77.23000403),
    'Goa':(15.491997,73.81800065),
    'Haryana':(28.45000633,77.01999101),
    'Himachal Pradesh':(31.10002545,77.16659704),
    'Jammu And Kashmir':(34.29995933,74.46665849),
    'Jharkhand':(23.80039349,86.41998572),
    'Karnataka':(12.57038129,76.91999711),
    'Kerala':(8.900372741,76.56999263),
    'Lakshadweep':(10.56257331,72.63686717),
    'Madhya Pradesh':(21.30039105,76.13001949),
    'Maharashtra':(19.25023195,73.16017493),
    'Manipur':(24.79997072,93.95001705),
    'Meghalaya':(25.57049217,91.8800142),
    'Mizoram':(23.71039899,92.72001461),
    'Nagaland':(25.6669979,94.11657019),
    'Orissa':(19.82042971,85.90001746),
    'Puducherry':(11.93499371,79.83000037),
    'Punjab':(31.51997398,75.98000281),
    'Rajasthan':(26.44999921,74.63998124),
    'Sikkim':(27.3333303,88.6166475),
    'Tamil Nadu':(12.92038576,79.15004187),
    'Tripura':(23.83540428,91.27999914),
    'Uttar Pradesh':(27.59998069,78.05000565),
    'Uttaranchal':(30.32040895,78.05000565),
    'West Bengal':(22.58039044,88.32994665),
}
fields = {
    'QV10M': 'specific humidity 10m above surface',
    'QV2M': 'specific humidity 2m above surface',
    'T10M': 'temperature 10m above surface',
    'T2M': 'temperature 2m above surface',
    'TQI': 'total precipitable ice water',
    'TQL': 'total precipitable liquid water',
    'TQV': 'total precipitable water vapor',
    'U10M': 'eastward wind 10m above surface',
    'U2M': 'eastward wind 2m above surface',
    'V10M': 'northward wind 10m above surface',
    'V2M': 'northward wind 2m above surface',
}
for city in cities.keys():
    files = [f for f in os.listdir(f"C:/Users/Yash Agarwal/Desktop/Data/"+city)]
    print(files)
    df_main=[]
    for f in files:
        nc = nc4.Dataset("C:/Users/Yash Agarwal/Desktop/Data/"+city+'/'+f)
        time_var = nc.variables['time']
        data={}
        dtime = nc4.num2date(time_var[:], time_var.units)
        for nasa_name, field in fields.items():
            data[field]=[]
            for i in range(24):
                data[field].append(pd.Series(
                    get_mean(nc.variables[nasa_name][i]),
                    index=[dtime[i]]))
        df={}
        for field, res_list in data.items():
            res = pd.concat(res_list, axis=0)
            res.sort_index(inplace=True)
            df[field]=res
        df=pd.DataFrame(df)
        df_main.append(df)
    result=pd.concat(df_main)
    result.to_csv("C:/Users/Yash Agarwal/Desktop/Data/"+city+'/'+f+'_final.csv')


