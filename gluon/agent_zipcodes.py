
def remove_dupes(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


# returns zip code based on (lat, lng)
def reverse_geocode(lat, lng):
    import json
    import requests

    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(lat)+','+str(lng)+\
          '&sensor=true_or_false&key=AIzaSyC5tj3ulnc4nZCQR1ui1ZAqpdaxpCU9wYA'
    r = requests.get(url)
    json = r.json()
    #zip_code = json['results'][1]['address_components'][5]['long_name']
    zip_code = json['results'][0]['address_components'][7]['long_name']
    return zip_code


def get_ap_zip(code):
    import urllib2
    import json

    ap_code = code
    url = 'https://api.flightstats.com/flex/airports/rest/v1/json/'+ap_code+\
          '/today?appId=47c14783&appKey=432be7f372adf6d5eff1d894767d4036'
    json_data = urllib2.urlopen(url).read()
    json_airports = json.loads(json_data)

    lat=json_airports['airport']['latitude']
    lng = json_airports['airport']['longitude']

    zip_code = reverse_geocode(lat, lng)
    return zip_code


def process_zipcodes_serviced(usaZip, airportCode, radius=30):

    zips=[]
    try:
        ap_codes = [x.strip() for x in airportCode.split(',')]       #split string into list
        for ap_code in ap_codes:                                     #for each airport code
            ap_zip = get_ap_zip(ap_code)                             #get zip code
            if len(str(ap_zip)) == 5:                                #make sure return value has len=5
                zips = zips + get_zips(ap_zip, radius)
                return zips
    except:
        pass
    try:
        zips = zips + get_zips(usaZip, radius)
        zips = remove_dupes(zips)
        return zips
    except:
        pass

    return


    #need to do this for airport codes. use curl -v  -X GET "https://api.flightstats.com/flex/airports/rest/v1/json/lax/today?appId=47c14783&appKey=432be7f372adf6d5eff1d894767d4036"
    #to get airport lat, lng. Then geocode this to get zip code. Run script again through this zip code to get a new list of zip codes. Remove any duplicates.

def get_zips(zip_code, radius):
    from pyzipcode import ZipCodeDatabase
    zcdb = ZipCodeDatabase()
    zips = [z.zip for z in zcdb.get_zipcodes_around_radius(zip_code, radius)]
    return zips