"""
@summary: Module containing common Lifemapper constants

@license: gpl2
@copyright: Copyright (C) 2015, University of Kansas Center for Research

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
"""

# .............................................................................
# .                               File constants                              .
# .............................................................................
# DATA FORMATS
class OutputFormat:
# ............................................................................
   TAR_GZ = '.tar.gz'
   TXT = '.txt'
   XML = '.xml'
   ZIP = '.zip'
   TMP = '.tmp'
   MAP = '.map'
   CSV = '.csv'
   JSON = '.json'
   NUMPY = '.npy'
   PICKLE = '.pkl'
   GTIFF = '.tif'
   ASCII = '.asc'
   HFA = '.img'
   SHAPE = '.shp'
   LOG = '.log'
   
# TODO: Replace with OutputFormat
# CSV_EXTENSION = '.csv'
# JSON_EXTENSION = '.json'
# NUMPY_EXTENSION = '.npy'
# PICKLE_EXTENSION = '.pkl'
RASTER_EXTENSION = '.tif'
SHAPE_EXTENSION = '.shp'

SHAPEFILE_EXTENSIONS = [".shp", ".shx", ".dbf", ".prj", ".sbn", ".sbx", ".fbn", 
                        ".fbx", ".ain", ".aih", ".ixs", ".mxs", ".atx", 
                        ".shp.xml", ".cpg", ".qix"]
SHAPEFILE_MAX_STRINGSIZE = 255

# .............................................................................
# .                               Job constants                               .
# .............................................................................
class InputDataType:
   LM_LOWRES_CLIMATE = 1
   LM_HIRES_CLIMATE = 2
   EDAC = 3
   
   USER_PRESENCE_ABSENCE = 11
   USER_ANCILLARY = 12

class JobStage:
   """ 
   Constants to define the stages of any Job:
         RAD w/ Experiment, Bucket, or PamSum
         SDM w/ Model or Projection
         Common w/ General (exists) and Notify
   """
   # ==========================================================================   
   #           Valid Stage for All Jobs and Objects                     
   # ==========================================================================
   # This Job object has not yet been processed
   GENERAL = 0
   # ==========================================================================   
   #           Valid Stage for RAD Jobs and Objects                        
   # ==========================================================================
   # RADIntersectJob contains RADExperiment object
   INTERSECT = 10
   # _RadCompressJob contains Original or Splotch Pam 
   COMPRESS = 20
   # _RadSwapJob contains RADBucket and random PamSum
   SWAP = 31
   SPLOTCH = 32
   # _RadCalculateJob contains original or random PamSum
   CALCULATE = 40
   # ==========================================================================   
   #           Valid Stage for SDM Jobs and Objects                     
   # ==========================================================================
   # SDMOccurrenceJob contains OccurrenceSet 
   OCCURRENCE = 105
   # SDMModelJob contains SDMModel 
   MODEL = 110
   # SDMProjectionJob contains SDMProjection 
   PROJECT = 120
   # ==========================================================================   
   #           Valid Stage for Notification Jobs and Objects                     
   # ==========================================================================
   # This Job object is complete, and the user must be notified
   NOTIFY = 500

class JobStatus:
   """ 
   @summary: Constants to define the status of a job
   """
   # Pull / Push job statuses.  Replaces older statuses
   GENERAL = 0
   INITIALIZE = 1
   PULL_REQUESTED = 90
   PULL_COMPLETE = 100
   ACQUIRING_INPUTS = 105
   COMPUTE_INITIALIZED = 110
   RUNNING = 120
   COMPUTED = 130
   PUSH_REQUESTED = 140
   PUSHED = 150
   PUSH_COMPLETE = 200
#    NOTIFY_READY = 210
   COMPLETE = 300
   
   # ==========================================================================   
   # =                             General Errors                             =
   # ==========================================================================
   # Not found in database, could be prior to insertion
   NOT_FOUND = 404

   GENERAL_ERROR = 1000
   UNKNOWN_ERROR = 1001
   DEPENDENCY_ERROR = 1002
   UNKNOWN_CLUSTER_ERROR = 1003
   PUSH_FAILED = 1100
   
   # Remote kill status.  This happens when something signals a stop
   REMOTE_KILL = 1150
   
   # ==========================================================================
   # =                              Common Errors                             =
   # ==========================================================================
   # Database
   # ............................................
   DB_CREATE_ERROR = 1201
   DB_DELETE_ERROR = 1202
   DB_INSERT_ERROR = 1203
   DB_READ_ERROR = 1204
   DB_UPDATE_ERROR = 1205
   
   # I/O
   # ............................................
   IO_READ_ERROR = 1301
   IO_WRITE_ERROR = 1302
   IO_WAIT_ERROR = 1303
   
   # ==========================================================================   
   # =                            Lifemapper Errors                           =
   # ==========================================================================
   #LM_GENERAL_ERROR = 2000 - conflicts with MODEL_ERROR and is not used.
   
   # Python errors
   # ............................................
   LM_PYTHON_ERROR = 2100
   LM_PYTHON_MODULE_IMPORT_ERROR = 2101
   LM_PYTHON_ATTRIBUTE_ERROR = 2102
   LM_PYTHON_EXPAT_ERROR = 2103

   # Lifemapper job errors
   # ............................................
   LM_JOB_ERROR = 2200
   LM_JOB_NOT_FOUND = 2201
   LM_JOB_NOT_READY = 2202
      
   # Lifemapper data errors
   # ............................................
   LM_DATA_ERROR = 2300
   LM_POINT_DATA_ERROR = 2301
   LM_RAW_POINT_DATA_ERROR = 2302
   
   # Lifemapper Pipeline errors
   LM_PIPELINE_ERROR = 2400
   LM_PIPELINE_WRITEFILE_ERROR = 2401
   LM_PIPELINE_WRITEDB_ERROR = 2402
   LM_PIPELINE_UPDATEOCC_ERROR = 2403

   LM_PIPELINE_DISPATCH_ERROR = 2415

   # ==========================================================================   
   # =                           SDM Errors                          =
   # ==========================================================================
   # General model error, previously 1002
   MODEL_ERROR = 2000
   # openModeller errors
   # ............................................
   OM_GENERAL_ERROR = 3000
      
   # Error in request file
   # ............................................
   OM_REQ_ERROR = 3100
      
   # Algorithm error
   # ............................................
   OM_REQ_ALGO_ERROR = 3110
   OM_REQ_ALGO_MISSING_ERROR = 3111
   OM_REQ_ALGO_INVALID_ERROR = 3112
      
   # Algorithm Parameter error
   # ............................................
   # ............................................
   OM_REQ_ALGOPARAM_ERROR = 3120
   OM_REQ_ALGOPARAM_MISSING_ERROR = 3121
   OM_REQ_ALGOPARAM_INVALID_ERROR = 3122
   OM_REQ_ALGOPARAM_OUT_OF_RANGE_ERROR = 3123
    
   # Layer error
   # ............................................
   OM_REQ_LAYER_ERROR = 3130
   OM_REQ_LAYER_MISSING_ERROR = 3131
   OM_REQ_LAYER_INVALID_ERROR = 3132
   OM_REQ_LAYER_BAD_FORMAT_ERROR = 3134
   OM_REQ_LAYER_BAD_URL_ERROR = 3135
    
   # Points error
   # ............................................
   OM_REQ_POINTS_ERROR = 3140
   OM_REQ_POINTS_MISSING_ERROR = 3141
   OM_REQ_POINTS_OUT_OF_RANGE_ERROR = 3143
   
   # Projection error
   # ............................................
   OM_REQ_PROJECTION_ERROR = 3150
   
   # Coordinate system error
   # ............................................
   OM_REQ_COORDSYS_ERROR = 3160
   OM_REQ_COORDSYS_MISSING_ERROR = 3161
   OM_REQ_COORDSYS_INVALID_ERROR = 3162
   
   # Error in openModeller execution
   # ............................................
   OM_EXEC_ERROR = 3200
   
   # Error generating model
   # ............................................
   OM_EXEC_MODEL_ERROR = 3210
   
   # Error generating projection
   # ............................................
   OM_EXEC_PROJECTION_ERROR = 3220
    
   # ............................................
   # Maxent errors
   # ............................................
   ME_GENERAL_ERROR = 3500
   
   # Maxent layer errors
   # ............................................
   ME_MISMATCHED_LAYER_DIMENSIONS = 3601
   ME_CORRUPTED_LAYER = 3602 # Could be issue with header or data
   ME_LAYER_MISSING = 3603
   ME_FILE_LOCK_ERROR = 3604
   
   # Maxent points issues
   # ............................................
   ME_POINTS_ERROR = 3740
   
   # Other Maxent problems
   # ............................................
   ME_HEAP_SPACE_ERROR = 3801
   
   # ==========================================================================   
   # =                               HTTP Errors                              =
   # ==========================================================================
   # Last 3 digits are the http error code, only 400 and 500 levels listed
   HTTP_GENERAL_ERROR = 4000
      
   # Client error
   # ............................................
   HTTP_CLIENT_BAD_REQUEST = 4400
   HTTP_CLIENT_UNAUTHORIZED = 4401
   HTTP_CLIENT_FORBIDDEN = 4403
   HTTP_CLIENT_NOT_FOUND = 4404
   HTTP_CLIENT_METHOD_NOT_ALLOWED = 4405
   HTTP_CLIENT_NOT_ACCEPTABLE = 4406
   HTTP_CLIENT_PROXY_AUTHENTICATION_REQUIRED = 4407
   HTTP_CLIENT_REQUEST_TIMEOUT = 4408
   HTTP_CLIENT_CONFLICT = 4409
   HTTP_CLIENT_GONE = 4410
   HTTP_CLIENT_LENGTH_REQUIRED = 4411
   HTTP_CLIENT_PRECONDITION_FAILED = 4412
   HTTP_CLIENT_REQUEST_ENTITY_TOO_LARGE = 4413
   HTTP_CLIENT_REQUEST_URI_TOO_LONG = 4414
   HTTP_CLIENT_UNSUPPORTED_MEDIA_TYPE = 4415
   HTTP_CLIENT_REQUEST_RANGE_NOT_SATISFIABLE = 4416
   HTTP_CLIENT_EXPECTATION_FAILED = 4417

   # Server error
   # ............................................
   HTTP_SERVER_INTERNAL_SERVER_ERROR = 4500
   HTTP_SERVER_NOT_IMPLEMENTED = 4501
   HTTP_SERVER_BAD_GATEWAY = 4502
   HTTP_SERVER_SERVICE_UNAVAILABLE = 4503
   HTTP_SERVER_GATEWAY_TIMEOUT = 4504
   HTTP_SERVER_HTTP_VERSION_NOT_SUPPORTED = 4505
   
   # Not found in database, could be prior to insertion
   NOT_FOUND = 404
   
   # ==========================================================================   
   # =                             Database Errors                            =
   # ==========================================================================
   #   """
   #   Last digit meaning:
   #      0: General error
   #      1: Failed to read
   #      2: Failed to write
   #      3: Failed to delete
   #   """
   DB_GENERAL_ERROR = 5000
   
   # Job
   # ............................................
   DB_JOB_ERROR = 5100
   DB_JOB_READ_ERROR = 5101
   DB_JOB_WRITE_ERROR = 5102
   DB_JOB_DELETE_ERROR = 5103
   
   # Layer
   # ............................................
   DB_LAYER_ERROR = 5200
   DB_LAYER_READ_ERROR = 5201
   DB_LAYER_WRITE_ERROR = 5202
   DB_LAYER_DELETE_ERROR = 5203
   
   # Layer node
   # ............................................
   DB_LAYERNODE_ERROR = 5300
   DB_LAYERNODE_READ_ERROR = 5301
   DB_LAYERNODE_WRITE_ERROR = 5302
   DB_LAYERNODE_DELETE_ERROR = 5303
   
   # ==========================================================================   
   # =                                IO Errors                               =
   # ==========================================================================
   #   """
   #   Last digit meaning:
   #      0: General error
   #      1: Failed to read
   #      2: Failed to write
   #      3: Failed to delete
   #   """
   IO_GENERAL_ERROR = 6000
   IO_NOT_FOUND = 6001
   
   # Model
   # ............................................
   IO_MODEL_ERROR = 6100

   # Model request
   # ............................................
   IO_MODEL_REQUEST_ERROR = 6110
   IO_MODEL_REQUEST_READ_ERROR = 6111
   IO_MODEL_REQUEST_WRITE_ERROR = 6112
   IO_MODEL_REQUEST_DELETE_ERROR = 6113
   
   # Model script
   # ............................................
   IO_MODEL_SCRIPT_ERROR = 6120
   IO_MODEL_SCRIPT_READ_ERROR = 6121
   IO_MODEL_SCRIPT_WRITE_ERROR = 6122
   IO_MODEL_SCRIPT_DELETE_ERROR = 6123

   # Model output
   # ............................................
   IO_MODEL_OUTPUT_ERROR = 6130
   IO_MODEL_OUTPUT_READ_ERROR = 6131
   IO_MODEL_OUTPUT_WRITE_ERROR = 6132
   IO_MODEL_OUTPUT_DELETE_ERROR = 6133
   
   # Projection
   # ............................................
   IO_PROJECTION_ERROR = 6200

   # Projection request
   # ............................................
   IO_PROJECTION_REQUEST_ERROR = 6210
   IO_PROJECTION_REQUEST_READ_ERROR = 6211
   IO_PROJECTION_REQUEST_WRITE_ERROR = 6212
   IO_PROJECTION_REQUEST_DELETE_ERROR = 6213
   
   # Projection script
   # ............................................
   IO_PROJECTION_SCRIPT_ERROR = 6220
   IO_PROJECTION_SCRIPT_READ_ERROR = 6221
   IO_PROJECTION_SCRIPT_WRITE_ERROR = 6222
   IO_PROJECTION_SCRIPT_DELETE_ERROR = 6223

   # Projection output
   # ............................................
   IO_PROJECTION_OUTPUT_ERROR = 6230
   IO_PROJECTION_OUTPUT_READ_ERROR = 6231
   IO_PROJECTION_OUTPUT_WRITE_ERROR = 6232
   IO_PROJECTION_OUTPUT_DELETE_ERROR = 6233
   
   # Layer
   # ............................................
   IO_LAYER_ERROR = 6300
   IO_LAYER_READ_ERROR = 6301
   IO_LAYER_WRITE_ERROR = 6302
   IO_LAYER_DELETE_ERROR = 6303
   
   # Matrix
   # ............................................
   IO_MATRIX_ERROR = 6400
   IO_MATRIX_READ_ERROR = 6401
   IO_MATRIX_WRITE_ERROR = 6402
   IO_MATRIX_DELETE_ERROR = 6403

   # Pickled RAD Objects
   # ............................................
   IO_INDICES_ERROR = 6500
   IO_INDICES_READ_ERROR = 6501
   IO_INDICES_WRITE_ERROR = 6502
   IO_INDICES_DELETE_ERROR = 6503

   # Occurrence Set jobs
   # ............................................
   IO_OCCURRENCE_SET_ERROR = 6600
   IO_OCCURRENCE_SET_READ_ERROR = 6601
   IO_OCCURRENCE_SET_WRITE_ERROR = 6602
   IO_OCCURRENCE_SET_DELETE_ERROR = 6603

   # ==========================================================================   
   # =                               SGE Errors                               =
   # ==========================================================================
   SGE_GENERAL_ERROR = 7000
   SGE_BASH_ERROR = 7100

   # ==========================================================================   
   # =                           RAD Errors                                   =
   # ==========================================================================
   RAD_GENERAL_ERROR = 8000
  
   RAD_INTERSECT_ERROR = 8100
   RAD_INTERSECT_ZERO_LAYERS_ERROR = 8110

   RAD_COMPRESS_ERROR = 8200
   
   RAD_CALCULATE_ERROR = 8300
   RAD_CALCULATE_FAILED_TO_CREATE_SHAPEFILE = 8312
   
   RAD_SWAP_ERROR = 8400
   RAD_SWAP_TOO_FEW_COLUMNS_OR_ROWS_ERROR = 8410
   
   RAD_SPLOTCH_ERROR = 8500
   RAD_SPLOTCH_PYSAL_NEIGHBOR_ERROR = 8510

   # ==========================================================================   
   #                               Compute Status                             =
   # ==========================================================================
   # 301000-301999  - Process (3) openModeller Model SDM (01)   
   # ............................................
   # Error in request file
   OM_MOD_REQ_ERROR = 301100
   # Algorithm error
   OM_MOD_REQ_ALGO_INVALID_ERROR = 301112
   # Algorithm Parameter error
   OM_MOD_REQ_ALGOPARAM_MISSING_ERROR = 301121
   # Layer error
   OM_MOD_REQ_LAYER_ERROR = 301130
   # Points error
   OM_MOD_REQ_POINTS_MISSING_ERROR = 301141
   OM_MOD_REQ_POINTS_OUT_OF_RANGE_ERROR = 301143
   
   # 301000-301999  - Process (3) openModeller SDM Projection (02)   
   # ............................................
   OM_PROJECTION_ERROR = 302150 

# ............................................................................
class ProcessType:
   # .......... SDM ..........
   ATT_MODEL = 110
   ATT_PROJECT = 120
   OM_MODEL = 210
   OM_PROJECT = 220
   # .......... RAD ..........
   RAD_BUILDSHAPE = 305
   RAD_INTERSECT = 310
   RAD_COMPRESS = 320
   RAD_SWAP = 331
   RAD_SPLOTCH = 332
   RAD_CALCULATE = 340
   # .......... GBIF Query ..........
   GBIF_TAXA_OCCURRENCE = 405
   BISON_TAXA_OCCURRENCE = 410
   IDIGBIO_TAXA_OCCURRENCE = 415
   # .......... Notify ..........
   SMTP = 510
   
   @staticmethod
   def isSDM(ptype):
      if ptype in (ProcessType.SMTP, ProcessType.ATT_MODEL, 
                   ProcessType.ATT_PROJECT, ProcessType.OM_MODEL, 
                   ProcessType.OM_PROJECT, ProcessType.GBIF_TAXA_OCCURRENCE, 
                   ProcessType.BISON_TAXA_OCCURRENCE, 
                   ProcessType.IDIGBIO_TAXA_OCCURRENCE):
         return True
      return False
      
   @staticmethod
   def isRAD(ptype):
      if ptype in (ProcessType.SMTP, ProcessType.RAD_BUILDSHAPE, 
                   ProcessType.RAD_INTERSECT, ProcessType.RAD_COMPRESS, 
                   ProcessType.RAD_SWAP, ProcessType.RAD_SPLOTCH, 
                   ProcessType.RAD_CALCULATE):
         return True
      return False
   
   

# .............................................................................
# .                               RAD constants                               .
# .............................................................................
class RandomizeMethods:
   NOT_RANDOM = 0
   SWAP = 1
   SPLOTCH = 2

# .............................................................................
# .                             Service constants                             .
# .............................................................................
BUCKETS_SERVICE = 'buckets'
EXPERIMENTS_SERVICE = 'experiments'
LAYERS_SERVICE = 'layers'
LAYERTYPES_SERVICE = 'typecodes'
MODELS_SERVICE = 'models'
OCCURRENCES_SERVICE = 'occurrences'
PAMSUMS_SERVICE = 'pamsums'
PROJECTIONS_SERVICE = 'projections'
SCENARIOS_SERVICE = 'scenarios'

# Generic layersets, not Scenarios
LAYERSETS_SERVICE = 'layersets'
# Biogeography Tools
SHAPEGRIDS_SERVICE = 'shpgrid'


# .............................................................................
# .                              Time constants                               .
# .............................................................................
# Time constants in Modified Julian Day (MJD) units 
ONE_MONTH = 1.0 * 30
ONE_DAY = 1.0
ONE_HOUR = 1.0/24.0
ONE_MIN = 1.0/1440.0
ONE_SEC = 1.0/86400.0

# Time formats
ISO_8601_TIME_FORMAT_FULL = "%Y-%m-%dT%H:%M:%SZ"
ISO_8601_TIME_FORMAT_TRUNCATED = "%Y-%m-%d"
YMD_HH_MM_SS = "%Y-%m-%d %H:%M%S"

# .............................................................................
# .                               User constants                              .
# .............................................................................
DEFAULT_POST_USER = 'anon'

# .............................................................................

# .............................................................................
# .                              Other constants                              .
# .............................................................................
DEFAULT_EPSG = 4326

URL_ESCAPES = [ [" ", "%20"] ]

class HTTPStatus:
   """
   @summary: HTTP 1.1 Status Codes as defined by 
                http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
   """
   # Informational 1xx
   CONTINUE = 100
   SWITCHING_PROTOCOLS = 101
   
   # Successful 2xx
   OK = 200
   CREATED = 201
   ACCEPTED = 202
   NON_AUTHORITATIVE_INFORMATION = 203
   NO_CONTENT = 204
   RESET_CONTENT = 205
   PARTIAL_CONTENT = 206
   
   # Redirectional 3xx
   MULTIPLE_CHOICES = 300
   MOVED_PERMANENTLY = 301
   FOUND = 302
   SEE_OTHER = 303
   NOT_MODIFIED = 204
   USE_PROXY = 305
   TEMPORARY_REDIRECT = 307
   
   # Client Error 4xx
   BAD_REQUEST = 400
   UNAUTHORIZED = 401
   FORBIDDEN = 403
   NOT_FOUND = 404
   METHOD_NOT_ALLOWED = 405
   NOT_ACCEPTABLE = 406
   PROXY_AUTHENTICATION_REQUIRED = 407
   REQUEST_TIMEOUT = 408
   CONFLICT = 409
   GONE = 410
   LENGTH_REQUIRED = 411
   PRECONDITION_FAILED = 412
   REQUEST_ENTITY_TOO_LARGE = 413
   REQUEST_URI_TOO_LONG = 414
   UNSUPPORTED_MEDIA_TYPE = 415
   REQUEST_RANGE_NOT_SATISFIABLE = 416
   EXPECTATION_FAILED = 417
   
   # Server Error 5xx
   INTERNAL_SERVER_ERROR = 500
   NOT_IMPLEMENTED = 501
   BAD_GATEWAY = 502
   SERVICE_UNAVAILABLE = 503
   GATEWAY_TIMEOUT = 504
   HTTP_VERSION_NOT_SUPPORTED = 505
   
# .............................................................................
# .                            Namespace constants                            .
# .............................................................................
# Lifemapper Namespace constants
LM_NAMESPACE = "http://lifemapper.org"
LM_NS_PREFIX = "lm"
LM_RESPONSE_SCHEMA_LOCATION = "/schemas/serviceResponse.xsd"
LM_PROC_NAMESPACE = "http://lifemapper.org/process"
LM_PROC_NS_PREFIX = "lmProc"
LM_PROC_SCHEMA_LOCATION = "/schemas/lmProcess.xsd"

# .............................................................................
# .                             Logging constants                             .
# .............................................................................
LOG_FORMAT = ' '.join(["%(asctime)s",
                       "%(threadName)s.%(module)s.%(funcName)s",
                       "line",
                       "%(lineno)d",
                       "%(levelname)-8s",
                       "%(message)s"])

# Date format for log dates
LOG_DATE_FORMAT = '%d %b %Y %H:%M'

# Maximum log file size before new log file is started
LOGFILE_MAX_BYTES = 52000000 

# The number of backups to keep.  as the log file approaches MAX_BYTES in size
#    it will be renamed and a new log file will be created.  The renamed file
#    will have the same name with a number appended (.1 - .BACKUP_COUNT).
#    When the maximum number of backups has been met, the oldest will be 
#    discarded.
LOGFILE_BACKUP_COUNT = 5
