import csv
import json
from collections import namedtuple
import re
import urllib
import urllib2
import time
from types import ListType, TupleType, StringType, UnicodeType

from constants import (DWCNames, long, short, IDIGBIO_LIVE_NAME, 
      IDIGBIO_OCCURRENCE_URL,
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
   j = None
   tries = 5
   data = []
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
      print url
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
      query += '&rq={"' + IDIGBIO_SCINAME_KEY + '":{"type":"prefix","value":"' + prefix + '"},"geopoint":{"type":"exists"},"datecollected":{"type":"exists"}}'
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
def _getFieldVal(item, keys):
   if not (isinstance(keys, ListType) or isinstance(keys, TupleType)): 
      keys = keys.split('.')
   val = item
   for k in keys:
      try:
         val = val[k]
      except Exception, e:
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
def _writeColumns(fsw):
   try:
      fsw.writerow([IDIGBIO_ID_FIELD, IDIGBIO_LINK_FIELD, 
                    DWCNames.OCCURRENCE_ID[short], 
                    DWCNames.SCIENTIFIC_NAME[short], 
                    DWCNames.CATALOG_NUMBER[short], 
                    DWCNames.INSTITUTION_CODE[short], 
                    DWCNames.COLLECTION_CODE[short],
                    DWCNames.DECIMAL_LATITUDE[short],
                    DWCNames.DECIMAL_LONGITUDE[short], 
                    DWCNames.RECORDED_BY[short],
                    DWCNames.DAY[short],
                    DWCNames.MONTH[short],
                    DWCNames.YEAR[short] ])
   except Exception, e:
      return False
   else:
      return True
   
# ...............................................
def _writeRecord(fsw, item, columns=None):
   success = False
   lat = _getFieldVal(item, [IDIGBIO_IDX_KEY, IDIGBIO_PT_KEY, 
                                  IDIGBIO_LAT_KEY])
   lon = _getFieldVal(item, [IDIGBIO_IDX_KEY, IDIGBIO_PT_KEY, 
                                  IDIGBIO_LON_KEY])
   if not (lat == 0 and lon == 0):
      uuid = item[IDIGBIO_ID_FIELD]
      idigurl = IDIGBIO_OCCURRENCE_URL + uuid
      occid = _getFieldVal(item, DWCNames.OCCURRENCE_ID[long])
      sciname = _getFieldVal(item, 
                             [IDIGBIO_IDX_KEY, IDIGBIO_SCINAME_KEY])
      catnum = _getFieldVal(item, DWCNames.CATALOG_NUMBER[long])
      instcode = _getFieldVal(item, DWCNames.INSTITUTION_CODE[long])
      collcode = _getFieldVal(item, DWCNames.COLLECTION_CODE[long])
      recby = _getFieldVal(item, DWCNames.RECORDED_BY[long])
      day = _getFieldVal(item, DWCNames.DAY[long])
      month = _getFieldVal(item, DWCNames.MONTH[long])
      year = _getFieldVal(item, DWCNames.YEAR[long])
      vals = []
      for v in [uuid, idigurl, occid, sciname, catnum, instcode, collcode, 
                lat, lon, recby, day, month, year]:
         try:
            if isinstance(v, StringType) or isinstance(v, UnicodeType):
               vals.append(v.encode('utf-8'))
            else:
               vals.append(v)
         except Exception, e:
            print('Exception in encoding!! {0} {1}'.format(type(e), str(e)))
            vals.append('Encoding error')
      try:
         fsw.writerow(vals)
         success = True
      except Exception, e:
         print('Exception on writing!! {0} {1} {2}'.format(type(e), str(item), str(e)))
   return success
   
# ...............................................
def getSpecimens(prefix, filename, timeSlice=None):
   """
   @summary: Queries for all specimens with a species prefix.
   @param prefix: The genus species string to match.
   @param maxReturned: (optional) The maximum number of results to return
   """
   qryElts = []
   fldqry = 'fields=["{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}"]'.format(
      IDIGBIO_SCINAME_KEY, IDIGBIO_PT_KEY, DWCNames.OCCURRENCE_ID[long], 
      DWCNames.CATALOG_NUMBER[long], DWCNames.INSTITUTION_CODE[long], 
      DWCNames.COLLECTION_CODE[long], DWCNames.RECORDED_BY[long], 
      DWCNames.DAY[long], DWCNames.MONTH[long], DWCNames.YEAR[long])
   qryElts.append('"{0}":{{"type":"prefix","value":"{1}"}}'.format(
                                                   IDIGBIO_SCINAME_KEY, prefix))
   qryElts.append('"geopoint":{"type":"exists"}')
   if timeSlice is not None and len(timeSlice) == 2 and timeSlice[0] > 0:
      qryElts.append('"datecollected": {{"type": "range","gte": "{0}", "lt": "{1}"}}'.format(
                                       timeSlice[0], timeSlice[1]))
   qrystr = ','.join(qryElts)
   query = '?{0}&rq={{{1}}}&no_attribution'.format(fldqry, qrystr)
   
   debugOffset = 0
   queryUrl = "{0}{1}&limit={2}&offset={3}".format(IDIGBIO_SEARCH_URL_PREFIX,
                                       query, IDIGBIO_SEARCH_LIMIT, debugOffset)
   totalRetrieved = 0
   js = _wgetLoadJson(queryUrl)
   itemCount = int(js["itemCount"])
   if itemCount > 0:
      fs = open(filename,'wb')
      fsw = csv.writer(fs, dialect='excel')
      success = _writeColumns(fsw)
      for i in range(0, itemCount, IDIGBIO_SEARCH_LIMIT):
         for item in js["items"]:
            success = _writeRecord(fsw, item)
            if success:
               totalRetrieved += 1
         if totalRetrieved < itemCount:
            queryUrl = "{0}{1}&limit={2}&offset={3}".format(IDIGBIO_SEARCH_URL_PREFIX,
                                               query, IDIGBIO_SEARCH_LIMIT, totalRetrieved)
            js = _wgetLoadJson(queryUrl)
         print 'Got {0} items this round, wrote {1} items total'.format(len(js['items']), totalRetrieved)
      print 'Wrote {0} items to {1}'.format(totalRetrieved, filename)
      fs.close()
    
# ...............................................
if __name__ == '__main__':
   output = getSpeciesHint('acacia', IDIGBIO_SEARCH_LIMIT)
   
   # 100K+
#   getSpecimens('peromyscus maniculatus', '/tmp/peromyscus_maniculatus.txt')

   getSpecimens('peromyscus eremicus', '/tmp/peromyscus_eremicus.csv')
#   getSpecimens('aroapyrgus clenchi', '/tmp/aroapyrgus_clenchi.txt', 
#                         timeSlice=(1900, 1970))
#   getSpecimens('aroapyrgus clenchi', '/tmp/aroapyrgus_clenchi.txt', 
#                         timeSlice=(1970,2015))
   

   
