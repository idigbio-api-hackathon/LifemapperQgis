# -*- coding: utf-8 -*-
"""
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
"""
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import lifemapperTools as LM
from lifemapperTools.common.lmListModel import (BackSpaceEventHandler, 
                              EnterTextEventHandler, LmListModel)
from LmClient.lmClientLib import LMClient, OutOfDateException
import idigbioClient.idigbioApi as idb
from idigbioClient.constants import DWCNames, long, short

# ..............................................................................
class Ui_Dialog(object):
   def setupUi(self):
      
      self.resize(800, 690)
      self.setMinimumSize(310,630)
      self.setMaximumSize(800,1430)
      self.setSizeGripEnabled(True)
      
      self.outerGrid = QGridLayout(self)
      self.gridLayout = QGridLayout()
      self.gridLayout.setRowMinimumHeight(0,300)
      self.gridLayout.setColumnMinimumWidth(0,300)
      self.outerGrid.addLayout(self.gridLayout,0,0,1,1)
      
      self.inputGroup = QGroupBox()
      self.style = QStyleFactory.create("motif") # try plastique too!
      self.inputGroup.setStyle(self.style)
      self.inputGroup.setTitle('Search')
      
      self.hintLineEdit = QLineEdit()
      self.gridLayout.addWidget(self.hintLineEdit,0,0,1,1)
      
      self.inputGroup.setLayout(self.gridLayout)
      self.outerGrid.addWidget(self.inputGroup,0,0,1,1)
      
# ..............................................................................
class BrowseOccProviderDialog(QDialog, Ui_Dialog):
   def __init__(self, iface):
      """
      @param iface: QGIS interface object
      @param mode: describe process or execute mode
      @param RADids: additional ids passed from previous process
      @param inputs: dictionary with inputs, keys are argument names in the 
      client library
      """
      QDialog.__init__(self)
      self.setupUi()
      
# ..............................................................................
class Ui_Dock(object):  
   def setupUi(self,DockWidget): 
      DockWidget.setWindowTitle("Occurrence Data")   
      #DockWidget.resize(429, 602)
      
      self.parentWidget = QWidget()
      
      #self.tabWidget = QTabWidget(self.parentWidget)
      #self.infoWidget = QWidget()
      
      self.logoLabel = QLabel()
      self.logoPixMap = QPixmap(":/plugins/lifemapperTools/icons/lm_poster_276_45.png")
      self.logoLabel.setPixmap(self.logoPixMap)
      
      self.vertLayout = QVBoxLayout(self.parentWidget)
      #self.hintLine  = QLineEdit() #occSetCombo
      self.occSetCombo = QComboBox()
      #self.occSetCombo.setMinimumHeight(26)
      #self.occSetCombo.setStyleSheet("font-size: 12pt")
      self.occSetCombo.setEditable(True)
      self.occSetCombo.setAutoCompletion(True)
      self.occSetCombo.lineEdit().setPlaceholderText("[Start Typing]")
      self.occSetCombo.textChanged.connect(self.onTextChange) 
      self.occSetCombo.setEnabled(False)
      
      self.timeCombo = QComboBox()
      self.timeCombo.setEditable(False)
      self.timeCombo.setAutoCompletion(False)
      self.timeModel = BrowseModel(['All', '1', '5', '10', '20', '50', '100'], parent = self)
      self.timeCombo.setModel(self.timeModel)
      self.timeCombo.setEnabled(False)

      self.providerCombo = QComboBox()
      self.providerCombo.setMinimumHeight(26)
      
      #f = QFont('Courier New',19)
      #self.providerCombo.setFont(f)
      self.providerCombo.setStyleSheet("font-size: 12pt")
      self.providerCombo.currentIndexChanged.connect(self.providerChanged)
      
      self.download = QPushButton("Get Shapefile")
#      self.download.clicked.connect(self.downloadShpFile)
      self.download.clicked.connect(self.pullAndWriteShapeFiles)
      self.vertLayout.addWidget(self.logoLabel)
      self.vertLayout.addWidget(QWidget())
      self.vertLayout.addWidget(self.providerCombo)
      self.vertLayout.addWidget(QWidget())
      self.vertLayout.addWidget(self.occSetCombo)
      self.vertLayout.addWidget(self.timeCombo)
      self.vertLayout.addWidget(QWidget())
      self.vertLayout.addWidget(self.download)
      
      DockWidget.setWidget(self.parentWidget)
      
# ..............................................................................
class BrowseOccProviderDock(QDockWidget, Ui_Dock):
   def __init__(self, iface, action = None):
      QDockWidget.__init__(self,None)
      
      self._serviceRoot = None
      self.setTmpDir()
      self.action = action
      self.iface = iface   
      self.setupUi(self)
      self.client = None
      self.action.triggered.connect(self.showHideBrowseDock)
      #self.signIn()
      
      self.occListModel = BrowseModel([], parent = self)
      self.occSetCombo.setModel(self.occListModel)
      self.BackSpaceEvent = BackSpaceEventHandler()
      self.occSetCombo.installEventFilter(self.BackSpaceEvent)

# ...............................................
   def showHideBrowseDock(self):
      if self.isVisible():
         #if self.client != None:
            #self.client.logout()    
            #self.client = None       
         self.hide()
      else:
         if self.client == None:
            self.signIn() 
            self.loadInstanceCombo()
         self.show()
         
# .......................................
   def providerChanged(self, idx):
      self.occListModel.updateList([])
      self.occSetCombo.clearEditText()
      if idx != 0 and idx != -1:
         self.serviceRoot, self.serviceType = self.providerCombo.itemData(idx, role=Qt.UserRole)
         self.occSetCombo.setEnabled(True)
         if self.serviceType == "live":
            self.timeCombo.setEnabled(True)
         else:
            self.timeCombo.setEnabled(False)
      else:
         self.serviceRoot = None
         self.serviceType = None
         self.occSetCombo.setEnabled(False)
         self.timeCombo.setEnabled(False)
         
# .......................................
   def setTmpDir(self):  
      """
      NEED TO TEST ON WINDOWS!
      """    
      tmp = None
      try:
         tmp = QDir.tempPath()  # this on windows might be weird
         if not os.path.exists(tmp):
            raise
      except:
         tmp = None
         try:
            import tempfile
            tmp = tempfile.gettempdir()
            if not os.path.exists(tmp):
               raise
         except:
            tmp = None
      self._tmpDir = tmp

   @property
   def tmpDir(self):
      return self._tmpDir

# .......................................
   @property
   def serviceRoot(self):
      
      if self._serviceRoot is None:
         pCurrentIdx = self.providerCombo.currentIndex()
         if pCurrentIdx != 0 and pCurrentIdx != -1:
            self._serviceRoot, self.serviceType = self.providerCombo.itemData(pCurrentIdx, role=Qt.UserRole)
      return self._serviceRoot
   
   @serviceRoot.setter   
   def serviceRoot(self, value):      
      self._serviceRoot = value
      
# ...............................................
   def _getTimeSlices(self, interval, tocBaseName):
      slices = {}
      startYear = 1701
      endYear = 2015
      if interval is not None:
         for fromDate in range(startYear, endYear, interval):
            toDate = fromDate + interval
            tocName = '{0}_{1}-{2}'.format(tocBaseName, fromDate, toDate)
            tmpFname = os.path.join(self.tmpDir,"%s.csv" % (tocName))
            try:
               slices[fromDate] = (toDate, tocName, tmpFname)
            except Exception, e:
               QMessageBox.warning(self, "status: ",'error: ' + str(e))
      else:
         tmpFname = os.path.join(self.tmpDir,"%s.csv" % (tocBaseName))
         slices[0] = (endYear, tocBaseName, tmpFname)
      return slices
   
# ...............................................
   def _getChoices(self):
      tocName = interval = hit = None
      provider = self.providerCombo.currentText()
      sHcurrentIdx = self.occSetCombo.currentIndex()
      timeCurrentIdx = self.timeCombo.currentIndex()
      try:
         hit = self.occListModel.listData[sHcurrentIdx].searchHit 
      except Exception, e:
         pass
      else:
         tocName = '%s_%s' % (provider, hit.name)
         try:
            timeChoice = self.timeModel.listData[timeCurrentIdx]
         except Exception, e:
            print 'Exception on timeIdx {0} ({1})'.format(str(timeCurrentIdx), 
                                                          str(e))
         else:
            if timeChoice != 'All':
               interval = int(timeChoice)
      return tocName, provider, hit, interval

# ...............................................
   def pullAndWriteShapeFiles(self):
      if self.serviceRoot:
         tocBaseName, provider, hit, interval = self._getChoices()
         print tocBaseName, provider, hit, interval
         if tocBaseName is not None and self.tmpDir is not None:
            try:
               zeroKeys = []
               if self.serviceType == "snapshot":
                  tmpFname = os.path.join(self.tmpDir,"%s.shp" % (tocBaseName))
                  slices = {0: (None, tocBaseName, tmpFname)}
                  self.client.sdm.getShapefileFromOccurrencesHint(hit,tmpFname,
                                                                  overwrite=True)
               elif self.serviceType == "live":
                  print '** live:', interval, tocBaseName
                  slices = self._getTimeSlices(interval, tocBaseName)
                  print '   slices =', slices.keys()
                  for startYear in slices.keys():
                     (endYear, tocName, tmpFname) = slices[startYear]
                     print '  ... getting {0} for {1}-{2} into {3}'.format(
                                         hit.name, startYear, endYear, tmpFname)
                     idb.getSpecimens(hit.name, tmpFname, 
                                      timeSlice=(startYear, endYear))
                     if not os.path.exists(tmpFname):
                        zeroKeys.append(startYear)
            except Exception, e:
               print 'Exception!! ', str(e)
            else:
               for empty in zeroKeys:
                  slices.pop(empty)
               print 'Remaining keys = ' + str(slices.keys())
               try:
                  self.addOccsetsToCanvas(slices)
               except Exception, e:
                  message = "couldn't add shp file to canvas "+str(e)
                  QMessageBox.warning(self,"status: ", message)                  
         else:
            message = "No tmp directory set in Environment variable, try setting TMPDIR"
            QMessageBox.warning(self,"status: ",message)
      else:
         QMessageBox.warning(self,"status: ", "serviceRoot is not set")
                      
# ...............................................
   def downloadShpFile(self):
      if self.serviceRoot:
         provider = self.providerCombo.currentText()
         sHcurrentIdx = self.occSetCombo.currentIndex()
         timeCurrentIdx = self.timeCombo.currentIndex()
         try:
            hit = self.occListModel.listData[sHcurrentIdx].searchHit 
         except Exception, e:
            pass
         else:
            tocName = '%s_%s' % (provider, hit.name)
         if tocName is not None and self.tmpDir is not None:
            try:
               if self.serviceType == "snapshot":
                  tmpFname = os.path.join(self.tmpDir,"%s.shp" % (tocName))
                  self.client.sdm.getShapefileFromOccurrencesHint(hit,tmpFname,
                                                                  overwrite=True)
               elif self.serviceType == "live":
                  tmpFname = os.path.join(self.tmpDir,"%s.csv" % (tocName))
                  print 'live', tocName
                  idb.getSpecimens(hit.name, tmpFname)
            except Exception, e:
               pass
            else:
               try:
                  print tmpFname, tocName
                  self.addToCanvas(tmpFname, tocName)
               except Exception, e:
                  message = "couldn't add shp file to canvas "+str(e)
                  QMessageBox.warning(self,"status: ", message)
               #else:
               #   try:
               #      # this doesn't work, have no idea why, works from console
               #      self.iface.zoomFull()
               #   except Exception, e:
               #      print "EXCEPTION IN ZOOM ",str(e)                     
         else:
            message = "No tmp directory set in Environment variable, try setting TMPDIR"
            QMessageBox.warning(self,"status: ",message)  
               
# ...............................................
   def addOccsetsToCanvas(self, occTimeSlices):
      fromYears = occTimeSlices.keys()
      fromYears.sort()
      for fromYr in fromYears:
         (toDate, tocName, tmpFname) = occTimeSlices[fromYr]
         if os.path.exists(tmpFname):
            fileName, fileExtension = os.path.splitext(tmpFname)
            vectortype = "ogr"
            if fileExtension == ".csv":
               csvPath = "file:///{0}?delimiter=,&xField={1}&yField={2}&crs=epsg:4326".format(
                          tmpFname, DWCNames.DECIMAL_LONGITUDE[short], 
                          DWCNames.DECIMAL_LATITUDE[short])
               shpFname = fileName + '.shp'
               vectorLayer = QgsVectorLayer(csvPath, tocName, "delimitedtext")
               if not vectorLayer.isValid():
                  QMessageBox.warning(self,"status: ", "%s not valid" % (tocName))
               else:
                  vectorwriter = QgsVectorFileWriter.writeAsVectorFormat(vectorLayer,
                                             shpFname,"utf-8",None,"ESRI Shapefile")
                  vectorLayer = QgsVectorLayer(shpFname, tocName, vectortype)
                  if not vectorLayer.isValid():
                     QMessageBox.warning(self, "status: ", "%s not valid" % (tocName))           
                  else:
                     QgsMapLayerRegistry.instance().addMapLayer(vectorLayer)
         
# ...............................................
   def addToCanvas(self, vectorpath, shapename):
      fileName, fileExtension = os.path.splitext(vectorpath)
      vectortype = "ogr"
      if fileExtension == ".csv":
         csvVectorpath = "file:///" + vectorpath
         csvVectorpath += "?delimiter=,&xField={0}&yField={1}&crs=epsg:4326".format(
            DWCNames.DECIMAL_LATITUDE[short],DWCNames.DECIMAL_LONGITUDE[short])
         vectorpath = vectorpath.replace('.csv', '.shp')
         vectorLayer = QgsVectorLayer(csvVectorpath,shapename,"delimitedtext")
         warningname = shapename    
         if not vectorLayer.isValid():
            QMessageBox.warning(self,"status: ",
               "%s not valid" % (warningname))
         else:
            vectorwriter = QgsVectorFileWriter.writeAsVectorFormat(vectorLayer,
                                       vectorpath,"utf-8",None,"ESRI Shapefile")
      vectorLayer = QgsVectorLayer(vectorpath,shapename,vectortype)
      warningname = shapename    
      if not vectorLayer.isValid():
         QMessageBox.warning(self,"status: ",
           "%s not valid" % (warningname))           
      else:
         QgsMapLayerRegistry.instance().addMapLayer(vectorLayer)
         #self.iface.zoomFull()
                           
# ...............................................
   def signIn(self):
      try:
         cl = LMClient()
      except OutOfDateException, e:
         message = "Your plugin version is out of date, please update from the QGIS python plugin repository."
         QMessageBox.warning(self,"Problem...",message,QMessageBox.Ok)
      except:
         message = "No Network Connection"
         QMessageBox.warning(self,"Problem...",message,QMessageBox.Ok)
      else:
         self.client = cl
         #print "COOKIE AT TOGGLE WIDGET ",self.client._cl.cookieJar," ",self.client
         try:
            myVersion = LM.version() # test"Version 0.1.2" #
            myVersion = myVersion.strip("Version")
            myVersion = myVersion.strip()
            self.client._cl.checkVersion(clientName="lmQGIS",verStr=myVersion)
         except OutOfDateException, e:
            
            message = "Your plugin version is out of date, please update from the QGIS python plugin repository."
            self.client.logout()
            self.client = None
            msgBox = QMessageBox.warning(self,
                                             "Problem...",
                                             message,
                                             QMessageBox.Ok) 

# ...............................................
   def loadInstanceCombo(self):
      self.providerCombo.clear()
      self.providerCombo.clearEditText()
      try:
         instanceObjs = self.client.sdm.getAvailableInstances()
      except:
         pass
      else:
         self.providerCombo.addItem('Select Provider',userData='None')
         for idx,instance in enumerate(instanceObjs):
            self.providerCombo.addItem(instance[0], [instance[1], "snapshot"])

      for idx,instance in enumerate(idb.getLiveInstances()):
         self.providerCombo.addItem(instance[0], [instance[1], "live"])

# ...............................................
   def setPreviewDownloadText(self, displayName):
      if id == '':
         self.download.setEnabled(False)
         self.download.setToolTip("Load Data from search")
      else:
         self.download.setEnabled(True)
         self.download.setToolTip("Load Data for %s" % (displayName))

# ...............................................
   def getIdxFromTuples(self,currentText):
      idx = 0
      # sO search result Object
      for sH in self.namedTuples:
         if sH.name.lower() in currentText.lower():
            break
         idx += 1
      return idx

# ...............................................
   def onTextChange(self, text):
      displayName = text
      noChars = len(displayName)
      # %20
      occurrenceSetId = None
      if text == '':
         
         self.occSetCombo.clear()
         self.occSetCombo.clearEditText()
                          
      if noChars >= 3:
         if ")" in text:
            
            currentText = self.occSetCombo.currentText()
            idx = self.getIdxFromTuples(currentText)
            
            self.occSetCombo.setCurrentIndex(idx) 
            currentIdx = self.occSetCombo.currentIndex()                       
            occurrenceSetId = self.occListModel.listData[currentIdx].occurrenceSetId
            displayName = self.occListModel.listData[currentIdx].displayName
            self.setPreviewDownloadText(displayName)
            return
         if ' ' in text:
            text.replace(' ','%20')
         
         self.searchOccSets(text)
         
# ...............................................
   def searchOccSets(self,searchText=''):
      root = self.serviceRoot
      try:
         if self.serviceType == "snapshot":
            self.namedTuples = self.client.sdm.hint(searchText,maxReturned=60,serviceRoot=root)
         elif self.serviceType == "live":
            self.namedTuples = idb.getSpeciesHint(searchText, maxReturned=100)         
      except Exception, e:
         pass
      else:
         items = []
         if len(self.namedTuples) > 0:
            for species in self.namedTuples:
               items.append(SpeciesSearchResult(species.name,species.id,species.numPoints,species))
         else:
            items.append(SpeciesSearchResult('', '', '',''))
         self.occListModel.updateList(items)

# ..............................................................................
class BrowseModel(LmListModel):

   def data(self, index, role):
      """
      @summary: Gets data at the selected index
      @param index: The index to return
      @param role: The role of the item
      @return: The requested item
      @rtype: QtCore.QVariant
      """
      if index.isValid() and (role == Qt.DisplayRole or role == Qt.EditRole):
         if index.row() == 0 and self.model:
            return "[start typing]"
         else:   
            try: return self.listData[index.row()].customData()
            except: return self.listData[index.row()]
           
      if index.isValid() and role == Qt.UserRole:
         return int(self.listData[index.row()])
      else:
         return    
   

# ..............................................................................
class SpeciesSearchResult(object):
   """
   @summary: Data structure for species search results (occurrence sets)
   """
   # .........................................
   def __init__(self, displayName, occurrenceSetId, numPoints, searchHit):
      """
      @summary: Constructor for SpeciesSearchResult object
      @param displayName: The display name for the occurrence set
      @param occurrenceSetId: The Lifemapper occurrence set id
      @param numPoints: The number of points in the occurrence set
      """
      self.displayName = displayName
      self.occurrenceSetId = occurrenceSetId
      self.numPoints = numPoints
      self.searchHit = searchHit

   # .........................................
   def customData(self):
      """
      @summary: Creates a string representation of the SpeciesSearchResult 
                   object
      """
      return "%s (%s points)" % (self.displayName, self.numPoints)
            
   
   
if __name__ == "__main__":
#  
   #client =  LMClient(userId='blank', pwd='blank')
   qApp   =  QApplication(sys.argv)
   d = BrowseOccProviderDialog(None)
   d.show()
   sys.exit(qApp.exec_())   
   