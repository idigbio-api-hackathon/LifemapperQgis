import csv
import json
from collections import namedtuple
import re
import urllib
import urllib2
import time

from constants import (ShortDWCNames, IDIGBIO_LIVE_NAME, IDIGBIO_OCCURRENCE_URL,
      IDIGBIO_SEARCH_URL_PREFIX, IDIGBIO_TOP_URL_PREFIX, IDIGBIO_SEARCH_LIMIT,
      BINOMIAL_REGEX, INVALIDSP_REGEX, IDIGBIO_ID_FIELD, IDIGBIO_LINK_FIELD,
      IDIGBIO_DATA_KEY, IDIGBIO_IDX_KEY, IDIGBIO_OCCID_KEY, IDIGBIO_ATTR_KEY,
      IDIGBIO_SCINAME_KEY, IDIGBIO_PT_KEY, IDIGBIO_LAT_KEY, IDIGBIO_LON_KEY, 
      IDIGBIO_INSTNAME_KEY, IDIGBIO_COLLNAME_KEY, IDIGBIO_RESPONSE_FIELDS,
      IDIGBIO_DAY, IDIGBIO_MONTH, IDIGBIO_YEAR)


# ...............................................
# Wgets the content of the URL, loads the content as JSON
def _wgetLoadJson(url):
   # Try to get data at least n times (in case the server is loaded and returning 504 - timeout)
   tries = 5
   data = []
   print url
   for i in range(0, tries):
      try:
         data = urllib2.urlopen(urllib.quote(url, safe="%/:=&?~#+!$,;'@()*[]"))
      except urllib2.HTTPError, e:
         print "HTTP Error:", e.code, url, "Retrying in", (i + 1), "seconds"
         time.sleep(i + 1)
         continue
      except urllib2.URLError, e:
         print "URL Error:", e.reason, url
         continue
      break
   if data:
      j = json.load(data)
   return j

# ...............................................
def getLiveInstances():
   return [[IDIGBIO_LIVE_NAME, IDIGBIO_SEARCH_URL_PREFIX]]

# ...............................................
def getSpeciesHint(prefix, maxReturned=None):
   """
   @summary: Queries for top species names in occurrences.
   @param prefix: The partial string to match (genus species).
   @param maxReturned: (optional) The maximum number of results to return
   """
   prefix = prefix.lower()
   SearchHit = namedtuple('SearchHit', ['name', 'id', 'numPoints',
                                        'downloadUrl'])

   query = '?top_fields=["%s"]' % IDIGBIO_SCINAME_KEY
   if maxReturned:
      query += "&count=" + str(maxReturned)
   if len(prefix) > 0:
      query += '&rq={"' + IDIGBIO_SCINAME_KEY + '":{"type":"prefix","value":"' + prefix + '"},"geopoint":{"type":"exists"}}'
   else:
      query += '&rq={"geopoint":{"type":"exists"}}'

   js = _wgetLoadJson(IDIGBIO_TOP_URL_PREFIX + query)

   items = []
   validNames = {}
   invalidNames = {}
   invChars = set('()/')
   for key in js[IDIGBIO_SCINAME_KEY]:
      matches = re.match(BINOMIAL_REGEX, key)
      if matches:
         if any((c in invChars) for c in key):
            invalidNames[key] = int(js[IDIGBIO_SCINAME_KEY][key]["itemCount"])
            continue
         for invsp in INVALIDSP_REGEX:
            if re.match(invsp, matches.group(2)):
               invalidNames[key] = int(js[IDIGBIO_SCINAME_KEY][key]["itemCount"])
               break
         else: # Valid binomial case
            validNames[key] = int(js[IDIGBIO_SCINAME_KEY][key]["itemCount"])
      else:
         invalidNames[key] = int(js[IDIGBIO_SCINAME_KEY][key]["itemCount"])
   for valid in validNames:
      for invalid in invalidNames.keys():
         if invalid.startswith(valid):
            validNames[valid] += invalidNames[invalid]
            del invalidNames[invalid]
   names = validNames.keys()
   names.sort()
   for key in names:
      items.append(SearchHit(name=key,id=key,downloadUrl=key,
                             numPoints=validNames[key]))
   return items

# ...............................................
def _getOptionalField(item, keys):
   val = item
   for k in keys:
      try:
         val = val[k]
      except:
         val = ''
   return val
   
# ...............................................
def _getOptionalListField(item, listKey, fldKey):
   vals = []
   try:
      subitems = item[listKey]
   except:
      pass
   else:
      for dict in subitems:
         try:
            vals.append(dict[fldKey])
         except:
            pass
   return vals

# ...............................................
def getSpecimens(prefix, filename):
   """
   @summary: Queries for all specimens with a species prefix.
   @param prefix: The genus species string to match.
   @param maxReturned: (optional) The maximum number of results to return
   """
   query =('?fields=["{0}","{1}","{2}.{3}","{4}","{5}","{2}.{6}","{2}.{7}","{2}.{8}"]&rq={{"{0}":{{"type":"prefix","value":"{9}"}}').format(
      IDIGBIO_SCINAME_KEY, IDIGBIO_PT_KEY, IDIGBIO_DATA_KEY, IDIGBIO_OCCID_KEY, 
      IDIGBIO_INSTNAME_KEY, IDIGBIO_COLLNAME_KEY, IDIGBIO_DAY, IDIGBIO_MONTH,
      IDIGBIO_YEAR, prefix)

   query += ',"geopoint":{"type":"exists"}}&no_attribution'
   print query
   
   js = _wgetLoadJson(IDIGBIO_SEARCH_URL_PREFIX + query + "&limit=1&offset=0")
   numPoints = int(js["itemCount"])
   fs = open(filename,'wb')
   fsw = csv.writer(fs, dialect='excel')
   fsw.writerow([IDIGBIO_ID_FIELD, IDIGBIO_LINK_FIELD, IDIGBIO_OCCID_KEY, 
                 IDIGBIO_SCINAME_KEY, IDIGBIO_LAT_KEY,IDIGBIO_LON_KEY,
                 IDIGBIO_DAY, IDIGBIO_MONTH, IDIGBIO_YEAR, IDIGBIO_ATTR_KEY])
   limit = "&limit=" + str(IDIGBIO_SEARCH_LIMIT)
   j = 0
   for i in range(0, numPoints, IDIGBIO_SEARCH_LIMIT):
      js = _wgetLoadJson(IDIGBIO_SEARCH_URL_PREFIX + query + limit + "&offset=" + str(i))
      for item in js["items"]:
         uuid = item[IDIGBIO_ID_FIELD]
         occid = _getOptionalField(item, [IDIGBIO_DATA_KEY, IDIGBIO_OCCID_KEY])
         attributionLst = _getOptionalListField(item, IDIGBIO_ATTR_KEY, 'name')
         attribution = ','.join(attributionLst)
         if IDIGBIO_DAY in item[IDIGBIO_DATA_KEY]:
            day = item[IDIGBIO_DATA_KEY][IDIGBIO_DAY]
         else:
            day = ''
         if IDIGBIO_MONTH in item[IDIGBIO_DATA_KEY]:
            month = item[IDIGBIO_DATA_KEY][IDIGBIO_MONTH]
         else:
            month = ''
         if IDIGBIO_YEAR in item[IDIGBIO_DATA_KEY]:
            year = item[IDIGBIO_DATA_KEY][IDIGBIO_YEAR]
         else:
            year = ''
         fsw.writerow([uuid, IDIGBIO_OCCURRENCE_URL + uuid, occid, 
                       item[IDIGBIO_IDX_KEY][IDIGBIO_SCINAME_KEY], 
                       item[IDIGBIO_IDX_KEY][IDIGBIO_PT_KEY][IDIGBIO_LAT_KEY], 
                       item[IDIGBIO_IDX_KEY][IDIGBIO_PT_KEY][IDIGBIO_LON_KEY],
                       day, month, year, attribution])
         j += 1
   fs.close()
    
# ...............................................
if __name__ == '__main__':
   output = getSpeciesHint('acacia', IDIGBIO_SEARCH_LIMIT)
   print output
   
   output = getSpecimens('aroapyrgus clenchi', '/tmp/acacia_caven.txt')
   print output
   
