import requests
from datetime import timedelta, date
import numpy as np
import os
lat_coords = np.arange(0, 361, dtype=int)
lon_coords = np.arange(0, 576, dtype=int)

def translate_lat_to_geos5_native(latitude):
    return ((latitude + 90) / 0.5)

def translate_lon_to_geos5_native(longitude):
    return ((longitude + 180) / 0.625)

def find_closest_coordinate(calc_coord, coord_array):
    index = np.abs(coord_array-calc_coord).argmin()
    return coord_array[index]

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

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2016, 1, 1)
end_date = date(2016, 1, 15)

# ***********************
# overriding requests.Session.rebuild_auth to maintain headers when redirected
# ***********************
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) and \
               redirect_parsed.hostname != self.AUTH_HOST and \
               original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return

if __name__ ==  '__main__':
    # create session with the user credentials that will be used to authenticate access to the data
    username = "yash362"
    password = "Yash13579"
    session = SessionWithHeaderRedirection(username, password)

    # ***********************
    # Loop through Files
    # ***********************
    for key, values in cities.items():
        print(key, values[0], values[1])
        lat_coord = translate_lat_to_geos5_native(values[0])
        lon_coord = translate_lon_to_geos5_native(values[1])
        lat = find_closest_coordinate(lat_coord, lat_coords)
        lon = find_closest_coordinate(lon_coord, lon_coords)
        for single_date in daterange(start_date, end_date):
            YYYY = single_date.strftime("%Y")
            MM = single_date.strftime("%m")
            DD = single_date.strftime("%d")
            fpath1 = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I1NXASM.5.12.4/' + YYYY + '/' + MM + '/'
            fpath2 = 'MERRA2_400.inst1_2d_asm_Nx.' + YYYY + MM + DD + '.nc4.nc?'
            fpath3 = 'U2M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TROPT[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TROPPB[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'T2M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TQL[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TOX[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'PS[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],V50M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],DISPH[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'TO3[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TS[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],T10M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'TROPPT[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TQI[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],SLP[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'TQV[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],V2M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TROPQ[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'V10M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],U50M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],U10M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'QV2M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],TROPPV[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],' \
                     'QV10M[0:23]['+str(lat)+':1:'+str(lat)+']['+str(lon)+':1:'+str(lon)+'],time,lat['+str(lat)+':1:'+str(lat)+'],lon['+str(lon)+':1:'+str(lon)+']'
            url = fpath1 + fpath2 + fpath3
            print(url)

            # extract the filename from the url to be used when saving the file
            filename = 'C:/Users/Yash Agarwal/Desktop/Data/'+key+'/'+key+'_MERRA2_400.inst1_2d_asm_Nx.' + YYYY + MM + DD + '.nc4.nc' #change directory path accordingly
            if not os.path.exists('C:/Users/Yash Agarwal/Desktop/Data/'+key): #change directory path accordingly
                os.mkdir('C:/Users/Yash Agarwal/Desktop/Data/'+key) #change directory path accordingly
            print(filename)

            try:
                # submit the request using the session
                response = session.get(url, stream=True)
                print(response.status_code)

                # raise an exception in case of http errors
                response.raise_for_status()

                # save the file
                with open(filename, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        fd.write(chunk)

            except requests.exceptions.HTTPError as e:
                # handle any errors here
                print(e)
