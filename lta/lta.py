import sys
import json
import urllib
from urlparse import urlparse
import httplib2 as http #External library

uri1 = 'http://datamall.mytransport.sg/ltaodataservice.svc/'
uri2 = 'http://datamall2.mytransport.sg/ltaodataservice/'
uris = {'BusArrival' : uri2,
        'SBSTRouteSet' : uri1,
        'SMRTRouteSet' : uri1,
        'SBSTInfoSet' : uri1,
        'SMRTInfoSet' : uri1,
        'BusStopCodeSet' : uri1,
        'TaxiAvailability' : uri2,
        'CarParkSet' : uri1,
        'ERPRateSet' : uri1,
        'TravelTimeSet' : uri1,
        'AlarmInfoSet' : uri1,
        'PlannedRoadOpeningSet' : uri1,
        'RoadWorkSet' : uri1,
        'CameraImageSet' : uri1,
        'IncidentSet' : uri1,
        'TrafficSpeedBandSet' : uri1,
        'VMSSet' : uri1}

def lta_request_ex (api_name, params, skip):
    #Authentication parameters
    headers = { 'AccountKey' : 'DysYzwCUc2H+JShCNLmUMA==',
                'UniqueUserID' : '0e918f77-3874-47e4-a4ed-a24951635a33',
                'accept' : 'application/json'} #Request results in JSON
    #API parameters
    # uri = 'http://datamallplus.cloudapp.net' #Resource URL
    #uri = 'http://datamall2.mytransport.sg/ltaodataservice/'
    uri = uris[api_name]
    # path = '/ltaodataservice.svc/IncidentSet?'
    #Query parameters
    # params = {'Latitude':'1.304980', #Search within a radius
    #           'Longitude':'103.831984', # from a central point
    #          'Distance':'5000'}; # Distance in metres
    #Build query string & specify type of API call
    if (skip == 0):
        skip_param = ''
    else:
        skip_param = '&$skip=' + str(skip)
    target = urlparse(uri + api_name + '?' + urllib.urlencode( params ) + skip_param )
    print target.geturl()
    method = 'GET'
    body = ''
    #Get handle to http
    h = http.Http()
    #Obtain results
    response, content = h.request(
        target.geturl(),
        method,
        body,
        headers)
    #Parse JSON to print
    jsonObj = json.loads(content)
    #print json.dumps(jsonObj, sort_keys=True, indent=4)
    return jsonObj
    #Save result to file
    # with open("traffic_incidents.json","w") as outfile: #Saving jsonObj["d"]
    #    json.dump(jsonObj, outfile, sort_keys=True, indent=4, ensure_ascii=False)

def lta_request(api_name, param):
    uri = uris[api_name]
    if (uri == uri2):
        # uri2 APIs return only one record
        return lta_request_ex(api_name, param, 0)
    # assume uri == uri1, which returns a set of records
    skip = 0
    data = []
    while(True):
        # print "Request"
        partialRes = lta_request_ex(api_name, param, skip)
        partialData = partialRes['d']
        if (len(partialData) == 0):
            break
        skip += len(partialData)
        data.extend(partialRes)
    return data

def dump_lta_request(api_name, param):
    res = lta_request(api_name, param)
    with open(api_name + ".json", "w") as outfile:
        json.dump(res, outfile, sort_keys=True, indent=4, ensure_ascii=False)

#dump_lta_request('IncidentSet', {'Latitude':'1.366667', 'Longitude':'103.8', 'Distance':'26000'})

if __name__ == "__main__":
    #dump_lta_request('CarParkSet', {})
    #dump_lta_request('TravelTimeSet', {})
    #dump_lta_request('AlarmInfoSet', {})
    #dump_lta_request('TrafficSpeedBandSet', {'LinkID':'103003846'})
    #dump_lta_request('BusArrival', {'BusStopID':'01012'})
    #dump_lta_request('IncidentSet', {})
    dump_lta_request(sys.argv[1], {})

