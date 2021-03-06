"""
@summary: Constants for the Lifemapper web service clients
@author: CJ Grady
@version: 3.1.0
@status: release

@license: Copyright (C) 2015, University of Kansas Center for Research

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
from LmCommon.common.localconstants import WEBSITE_ROOT

CONTENT_TYPES = {
                 "AAIGrid" : "text/plain",
                 "GTiff" : "image/tiff"
                }

LM_CLIENT_VERSION_URL = "http://lifemapper.org/clients/versions.xml"
LM_INSTANCES_URL = "http://lifemapper.org/clients/instances.xml"
   