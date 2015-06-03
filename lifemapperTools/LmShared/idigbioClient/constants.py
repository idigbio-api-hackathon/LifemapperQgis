from osgeo.ogr import OFTInteger, OFTReal, OFTString
# .............................................................................
# .                           iDigBio constants                               .
# .............................................................................
IDIGBIO_LIVE_NAME = 'iDigBio Live'

IDIGBIO_SEARCH_URL_PREFIX = 'http://beta-search.idigbio.org/v2/search/records/'
IDIGBIO_TOP_URL_PREFIX = 'http://beta-search.idigbio.org/v2/summary/top/records/'
IDIGBIO_SEARCH_LIMIT = 5000

IDIGBIO_OCCURRENCE_URL = 'https://www.idigbio.org/portal/records/'

BINOMIAL_REGEX = "(^[^ ]*) ([^ ]*)$"
INVALIDSP_REGEX = ["sp[.?0-9]*$", "[(]*indet[).?]*$", "[?]$", "l[.]*$"]

class ShortDWCNames:
   OCCURRENCE_ID = 'occurid'
   INSTITUTION_CODE = 'inst_code'
   COLLECTION_CODE = 'coll_code'
   CATALOG_NUMBER = 'catnum'
   BASIS_OF_RECORD = 'basisofrec'
   DECIMAL_LATITUDE = 'dec_lat'
   DECIMAL_LONGITUDE = 'dec_long'
   SCIENTIFIC_NAME = 'sciname'
   DAY = 'day'
   MONTH = 'month'
   YEAR = 'year'
   RECORDED_BY = 'rec_by'

IDIGBIO_ID_FIELD = 'uuid'
IDIGBIO_LINK_FIELD = 'idigbiourl'

IDIGBIO_DATA_KEY = 'data'
IDIGBIO_IDX_KEY = 'indexTerms'
IDIGBIO_PT_KEY = 'geopoint'
IDIGBIO_LAT_KEY = 'lat'
IDIGBIO_LON_KEY = 'lon'
IDIGBIO_OCCID_KEY = 'dwc:occurrenceID'
IDIGBIO_SCINAME_KEY = 'scientificname'
IDIGBIO_INSTNAME_KEY = 'institutionname'
IDIGBIO_COLLNAME_KEY = 'collectionname'
IDIGBIO_DAY = 'dwc:day'
IDIGBIO_MONTH = 'dwc:month'
IDIGBIO_YEAR = 'dwc:year'
IDIGBIO_ATTR_KEY = 'attribution'

IDIGBIO_RESPONSE_FIELDS = {IDIGBIO_ID_FIELD: (IDIGBIO_ID_FIELD, OFTString), 
                         1: (ShortDWCNames.OCCURRENCE_ID, OFTInteger),
                         2: (IDIGBIO_LINK_FIELD, OFTString),
                         3: (ShortDWCNames.SCIENTIFIC_NAME, OFTString),
                         4: (ShortDWCNames.DECIMAL_LATITUDE, OFTReal),
                         5: (ShortDWCNames.DECIMAL_LONGITUDE, OFTReal),
                         6: ('inst_name', OFTString)
                         }
