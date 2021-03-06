"""
@summary: Location of local configuration options
@author: CJ Grady
@contact: cjgrady [at] ku [dot] edu
@version: 1.0
@status: beta

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
import ConfigParser
import os

from LmCommon.common.singleton import singleton

# Looks for a Lifemapper configuration file path environment variable.  If one
#    cannot be found, raise an exception
CONFIG_FILENAME = os.getenv('LIFEMAPPER_CONFIG_FILE') 
# if CONFIG_FILENAME is None or len(CONFIG_FILENAME) == 0:
#    raise Exception, "No configuration file found.  Set LIFEMAPPER_CONFIG_FILE environment variable"

# .............................................................................
@singleton
class Config(object):
   """
   @summary: Lifemapper configuration object will read config.ini and store 
                values
   """
   # .....................................
   def __init__(self, fn=CONFIG_FILENAME):
      if fn is None or len(fn) == 0:
         raise ValueError, "No configuration file found.  Set LIFEMAPPER_CONFIG_FILE environment variable"
      self.fn = fn
      self.reload()
      
   # .....................................
   def get(self, section, item):
      return self.config.get(section, item)
   
   # .....................................
   def getboolean(self, section, item):
      return self.config.getboolean(section, item)

   # .....................................
   def getfloat(self, section, item):
      return self.config.getfloat(section, item)
   
   # .....................................
   def getint(self, section, item):
      return self.config.getint(section, item)

   # .....................................
   def getlist(self, section, item):
      listStr = self.config.get(section, item).strip('[').strip(']')
      return [itm.strip() for itm in listStr.split(',')]

   # .....................................
   def reload(self):
      """
      @summary: This function will reload the configuration file.  This will 
                   catch any updates to the configuration without having to 
                   stop and restart the process.
      """
      self.config = ConfigParser.SafeConfigParser()
      self.config.read(self.fn)
      