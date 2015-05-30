"""
@summary: Module containing functions for API Queries
@status: beta

@license: gpl2
@copyright: Copyright (C) 2014, University of Kansas Center for Research

          Lifemapper Project, lifemapper [at] ku [dot] edu, 
          Biodiversity Institute,
          1345 Jayhawk Boulevard, Lawrence, Kansas, 66045, USA
   
          This program is free software; you can redistribute it and/or modify 
          it under the terms of the GNU General Public License as published by 
          the Free Software Foundation; either version 2 of the License, or (at 
          your option) any later version.
  
          This program is distributed in the hope that it will be useful, but 
          WITHOUT ANY WARRANTY; without even the implied warranty of 
          MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
          General Public License for more details.
  
          You should have received a copy of the GNU General Public License 
          along with this program; if not, write to the Free Software 
          Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 
          02110-1301, USA.

@copyright: Copyright (C) 2015, University of Florida, iDigBio project
"""
import json
import urllib, urllib2
import re
from types import BooleanType, FloatType, IntType, ListType, TupleType, StringType 

# .............................................................................
# .                           General constants                               .
# .............................................................................
URL_ESCAPES = [ [" ", "%20"] ]
BINOMIAL_REGEX = "(^[^ ]*) ([^ ]*)$"

# .............................................................................
# .                           iDigBio constants                               .
# .............................................................................
IDIGBIO_SEARCH_URL_PREFIX = 'http://search.idigbio.org/idigbio/records/_search'
# Query to aggregate all reoreferenced scientific names with minimun number (40) of occurrences
IDIGBIO_AGG_SPECIES_GEO_MIN_40 = '{"query":{"bool":{"must_not":[{"term":{"lat":"0"}},{"term":{"lon":"0"}}]}},"size":0,"aggregations":{"my_agg":{"terms":{"field":"scientificname","min_doc_count":40,"size":100000}}},"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]}}'
IDIGBIO_SPECIMENS_BY_BINOMIAL = '{"query":{"prefix":{"scientificname":"__BINOMIAL__"}},"filter":{"and":[{"exists":{"field":"geopoint"}},{"exists":{"field":"scientificname"}}]},"fields":["uuid","scientificname","geopoint.lat","geopoint.lon"],"size":1000000}'
IDIGBIO_QFILTERS = {}
IDIGBIO_FILTERS = {}

# .............................................................................
# .                              Time constants                               .
# .............................................................................
# Time constants in Modified Julian Day (MJD) units 
ONE_MONTH = 1.0 * 30
ONE_DAY = 1.0
ONE_HOUR = 1.0/24.0
ONE_MIN = 1.0/1440.0
ONE_SEC = 1.0/86400.0


# .............................................................................
class APIQuery(object):
   """
   Class to query APIs and return results
   """
   def __init__(self, baseurl, 
                qFilters={}, otherFilters={}, filterString=None, 
                headers={}):
      """
      @summary Constructor for the APIQuery class
      """
      self.headers = headers
      # No added filters are on url (unless initialized with filters in url)
      self.baseurl = baseurl
      self._qFilters = qFilters
      self._otherFilters = otherFilters
      self.filterString = self._assembleFilterString(filterString=filterString)
      self.output = None
      self.debug = False
      
# ...............................................
   @classmethod
   def initFromUrl(cls, url, headers={}):
      base, filters = url.split('?')
      qry = APIQuery(base, filterString=filters)
      return qry
      
   # .........................................
   @property
   def url(self):
      # All filters added to url
      return '%s?%s' % (self.baseurl, self.filterString)

# ...............................................
   def addFilters(self, qFilters={}, otherFilters={}):
      """
      @summary: Add new or replace existing filters.  This does not remove 
                existing filters, unless existing keys are sent with new values.
      """
      self.output = None
      for k, v in qFilters.iteritems():
         self._qFilters[k] = v
      for k, v in otherFilters.iteritems():
         self._otherFilters[k] = v
      self.filterString = self._assembleFilterString()
         
# ...............................................
   def clearAll(self, qFilters=True, otherFilters=True):
      """
      @summary: Clear existing qFilters, otherFilters, and output
      """
      self.output = None
      if qFilters:
         self._qFilters = {}
      if otherFilters:
         self._otherFilters = {}
      self.filterString = self._assembleFilterString()

# ...............................................
   def clearOtherFilters(self):
      """
      @summary: Clear existing otherFilters and output
      """
      self.clearAll(otherFilters=True, qFilters=False)

# ...............................................
   def clearQFilters(self):
      """
      @summary: Clear existing qFilters and output
      """
      self.clearAll(otherFilters=False, qFilters=True)

# ...............................................
   def _assembleFilterString(self, filterString=None):
      if filterString is not None:
         for replaceStr, withStr in URL_ESCAPES:
            filterString = filterString.replace(replaceStr, withStr)
      else:
         allFilters = self._otherFilters.copy()
         if self._qFilters:
            qVal = self._assembleQVal(self._qFilters)
            allFilters['q'] = qVal
         filterString = self._assembleKeyValFilters(allFilters)
      return filterString

# ...............................................
   def _assembleKeyValFilters(self, ofDict):
      for k, v in ofDict.iteritems():
         if isinstance(v, BooleanType):
            v = str(v).lower()
         ofDict[k] = unicode(v).encode('utf-8')               
      filterString = urllib.urlencode(ofDict)
      return filterString
      
# ...............................................
   def _interpretQClause(self, key, val):
      cls = None
      if (isinstance(val, StringType) or 
          isinstance(val, IntType) or 
          isinstance(val, FloatType)):
         cls = '%s:%s' % (key, str(val))
      # Tuple for negated or range value
      elif isinstance(val, TupleType):            
         # negated filter
         if isinstance(val[0], BooleanType) and val[0] is False:
            cls = 'NOT ' + key + ':' + str(val[1])
         # range filter (better be numbers)
         elif ((isinstance(val[0], IntType) or isinstance(val[0], FloatType))
               and (isinstance(val[1], IntType) or isinstance(val[1], FloatType))):
            cls = '%s:[%s TO %s]' % (key, str(val[0]), str(val[1]))
         else:
            print 'Unexpected value type %s' % str(val)
      else:
         print 'Unexpected value type %s' % str(val)
      return cls
   
# ...............................................
   def _assembleQItem(self, key, val):
      itmClauses = []
      # List for multiple values of same key
      if isinstance(val, ListType):
         for v in val:
            itmClauses.append(self._interpretQClause(key, v))
      else:
         itmClauses.append(self._interpretQClause(key, val))
      return itmClauses

# ...............................................
   def _assembleQVal(self, qDict):
      clauses = []
      qval = ''
      # interpret dictionary
      for key, val in qDict.iteritems():
         clauses.extend(self._assembleQItem(key, val))
      # convert to string
      firstClause = None
      for cls in clauses:
         if not firstClause and not cls.startswith('NOT'):
            firstClause = cls
         elif cls.startswith('NOT'):
            qval = ' '.join((qval, cls))
         else:
            qval = ' AND '.join((qval, cls))
      qval = firstClause + qval
      return qval

# ...............................................
   def query(self, outputType='json'):
#       # Also Works
#       response = urllib2.urlopen(fullUrl.decode('utf-8'))
      data = None
      if self._qFilters:
         # All q and other filters are on url
         req = urllib2.Request(self.url, None, self.headers)
      else:
         if self._otherFilters:
            data = urllib.urlencode(self._otherFilters)
         # Any filters are in data
         req = urllib2.Request(self.url, data, self.headers)
      response = urllib2.urlopen(req)
      output = response.read()
      if outputType == 'json':
         import json
         try:
            self.output = json.loads(output)
         except Exception, e:
            print str(e)
            raise
      elif outputType == 'xml':
         try:
            root = ET.fromstring(output)
            self.output = root    
         except Exception, e:
            print str(e)
            raise
      else:
         print 'Unrecognized output type %s' % str(outputType)
         self.output = None  

# .............................................................................
class IdigbioAPI(APIQuery):
# .............................................................................
   """
   Class to query iDigBio APIs and return results
   """
# ...............................................
   def __init__(self, qFilters={}, otherFilters={}, filterString=None,
                headers={'Content-Type': 'application/json'}):
      """
      @summary: Constructor for IdigbioAPI class      
      """
      # Add Q filters for this instance
      for key, val in IDIGBIO_QFILTERS.iteritems():
         qFilters[key] = val
      # Add other filters for this instance
      for key, val in IDIGBIO_FILTERS.iteritems():
         otherFilters[key] = val
         
      APIQuery.__init__(self, IDIGBIO_SEARCH_URL_PREFIX, qFilters=qFilters, 
                        otherFilters=otherFilters, filterString=filterString, 
                        headers=headers)
      
# ...............................................
   @classmethod
   def initFromUrl(cls, url, headers={'Content-Type': 'application/json'}):
      base, filters = url.split('?')
      if base == IDIGBIO_SEARCH_URL_PREFIX:
         qry = IdigbioAPI(filterString=filters)
      else:
         raise Exception('iDigBio occurrence API must start with %s' 
                         % IDIGBIO_SEARCH_URL_PREFIX)
      return qry
      
# ...............................................
   def _burrow(self, keylst):
      dict = self.output
      for key in keylst:
         dict = dict[key]
      return dict
         
# ...............................................
   def getBinomial(self):
      """
      @summary: Returns a list of dictionaries where each dictionary is an 
                occurrence record
      """
      if self.debug:
         print self.url
      if self.output is None:
         self.query()
      dataList = self._burrow(["aggregations", "my_agg", "buckets"])
      binomialList = []
      filtered = []
      print 'Distinct scientific names count = %d' % (len(dataList))
      for entry in dataList:
         matches = re.match(BINOMIAL_REGEX, entry["key"])
         if matches:
            if not matches.group(2) == "sp.":
               binomialList.append(entry)
            else:
               if self.debug:
                  filtered.append(entry["key"])
         else:
            if self.debug:
               filtered.append(entry["key"])
      print 'Distinct binomials count = %d' % (len(binomialList))
      if self.debug:
         print 'Filtered:', filtered
      return binomialList

# ...............................................
   def getSpecimensByBinomial(self):
      """
      @summary: Returns a list of dictionaries.  Each dictionary is an occurrence record
      """
      if self.debug:
         print self.url
      if self.output is None:
         self.query()
      specimenList = []
      dataList = self._burrow(["hits", "hits"])
      for entry in dataList:
         specimenList.append(entry["fields"])
      return specimenList

# ...............................................
   def query(self):
      """
      @summary: Queries the API and sets 'output' attribute to a JSON object 
      """
      APIQuery.query(self, outputType='json')
      
      
# .............................................................................
# Main method to (a) retrieve all scientific names in iDigBio, (b) keep only
# binomials, (c) for each binomial create a list of other names to be included
# (usually subspecies and names with authors), and (d) retrieve occurrences
# for each species.
# .............................................................................

if __name__ == '__main__':
   scinameQuery = IdigbioAPI(filterString="source=" + IDIGBIO_AGG_SPECIES_GEO_MIN_40)
   binomials = scinameQuery.getBinomial()
   #print binomials

   for id, binomial in enumerate(binomials):
      if id > 10:
         quit()
      else:
         specimenQuery = IdigbioAPI(filterString="source=" + IDIGBIO_SPECIMENS_BY_BINOMIAL.replace("__BINOMIAL__", binomial["key"]))
         specimens = specimenQuery.getSpecimensByBinomial()
         print "Retrieved %d specimens as %s" % (len(specimens), binomial["key"])
