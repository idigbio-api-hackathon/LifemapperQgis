import os
import time
import types
import sys
from types import StringType
from collections import namedtuple
from PyQt4.QtGui import *
from PyQt4.QtCore import *



class BackSpaceEventHandler(QObject):
   
   def eventFilter(self,object,event):
      if event.type() == QEvent.KeyPress:
         if event.key() == Qt.Key_Backspace:
            currentText = object.currentText()
            try:
               currentIdx = object.currentIndex()
               numPoints = object.model().listData[currentIdx].numPoints
               if numPoints in currentText:               
                  displayName = object.model().listData[currentIdx].displayName
                  object.setEditText(displayName+displayName[-1:])
                  # this should also probably clear the scenario models and 
                  # and disable
            except:
               pass
            
      return QWidget.eventFilter(self, object, event)

   
class EnterTextEventHandler(QObject):
  
   def __init__(self,control,model, button = None):
      super(EnterTextEventHandler, self).__init__()
      self.control = control
      self.model = model
      self.button = button
      
   def eventFilter(self,object,event):
      if event.type() == QEvent.FocusIn:
         self.model.updateList([])
         self.control.setCurrentIndex(0)
        
            
      return QWidget.eventFilter(self, object, event)



class LmListModel(QAbstractListModel):
   """
   @summary: List model used by Lifemapper Qt listing widgets
   @note: Inherits from QtCore.QAbstractListModel 
   """
   # .........................................
   def __init__(self, listData, parent=None, model=False, *args):
      """
      @summary: Constructor for LmListModel
      @param listData: List of objects to insert into list
      @param parent: (optional) The parent of the LmListModel
      @param model: bool, whether or not data model is for modeling layer set
      @param args: Additional arguments to be passed
      """
      QAbstractListModel.__init__(self, parent, *args)
      self.listData = listData
      self.model = model
      
   # .........................................
   def data(self, index, role):
      """
      @summary: Gets data at the selected index
      @param index: The index to return
      @param role: The role of the item
      @return: The requested item
      @rtype: QtCore.QVariant
      """
      if index.isValid() and (role == Qt.DisplayRole or role == Qt.EditRole):
         if index.row() == 1 and self.model:
            return "build new model"
         else:
            return str(self.listData[index.row()])
      if index.isValid() and role == Qt.UserRole:
         return self.listData[index.row()]  
      else:
         return 
      
   # .........................................
   def rowCount(self, parent=QModelIndex()):
      """
      @summary: Returns the number of rows in the list
      @param parent: (optional) The parent of the object
      @return: The number of items in the list
      @rtype: Integer
      """
      return len(self.listData)
   
   # .........................................
   def updateList(self, newList):
      """
      @summary: Updates the contents of the list
      @param newList: A list of items to use for the new list
      @note: The provided list will replace the old list 
      """
      #print "its at update list ",newList
      self.beginInsertRows(QModelIndex(), 0, len(newList))
      self.listData = newList
      
      self.endInsertRows()
