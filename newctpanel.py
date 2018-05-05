# encoding: utf-8

import gvsig

from addons.PrototipoPanelesCRS.patchs.fixformpanel import fixFormPanelResourceLoader
from addons.PrototipoPanelesCRS.crspanel import showCrsSelectorDialog

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools.swing.api.windowmanager import WindowManager_v2 as WindowManager

from java.awt import BorderLayout

from javax.swing import DefaultComboBoxModel

from gvsig.commonsdialog import openFileDialog
import os

from gvsig.commonsdialog import msgbox

class Wkt1Panel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "newctwkt1panel.xml"))

  def __repr__(self):
    return "WKT1"
    
  def btnSelectSoureCRS_click(self, evet):
    def onChooseSourceCrs(crspanel):
      self.txtSourceCRS.setText(crspanel.getProjection())
    showCrsSelectorDialog(onChooseSourceCrs)

  def btnSelectTargetCRS_click(self, evet):
    def onChooseTargetCrs(crspanel):
      self.txtTargetCRS.setText(crspanel.getProjection())
    showCrsSelectorDialog(onChooseTargetCrs)
    
class Wkt2Panel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "newctwkt2panel.xml"))

  def __repr__(self):
    return "WKT2"
    
class ManualPanel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "newct7paramspanel.xml"))

  def __repr__(self):
    return "7 parameters (Position vector transformation / Helmert / Bursa-Wolf)"
    
class NadGridPanel(FormPanel):
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "newctntgridpanel.xml"))

  def __repr__(self):
    return "NTv2 Grid"

  def btnSelectGridFile_click(self,event):
    f = openFileDialog(
      "Select a NTv2 Grid file",
      os.path.expanduser('~'),
      self.asJComponent()
    )
    if f==None or len(f)<1:
      return
    self.txtGridFile.setText(f[0])
    

class NewCtPanel(FormPanel):
  # pylint: disable=R0904 
  # Too many public methods (%s/%s)
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "newctpanel.xml"))
    self.__subpanels = [
      Wkt1Panel(),
      Wkt2Panel(),
      ManualPanel(),
      NadGridPanel()
    ] 
    model = DefaultComboBoxModel()
    for item in self.__subpanels:
      model.addElement(item)
    self.cboType.setModel(model)
    self.subpanelContainer.setLayout(BorderLayout())
    self.cboType.setSelectedItem(self.__subpanels[2])
    #self.setPreferredSize(600,300)

  def btnForceCode_click(self, event):
    print ">>> btnForceCode_click"
    self.txtCode.setReadOnly(False)
    self.btnForceCode.setEnabled(False)
    
  def cboType_change(self,event):
    subpanel = self.cboType.getSelectedItem()
    self.subpanelContainer.removeAll()
    self.subpanelContainer.add(subpanel.asJComponent(),BorderLayout.CENTER)
    self.asJComponent().validate()

    
def showNewCtDialog():
  def dialogListener(event):
    if dialog.getAction() == WindowManager.BUTTON_OK:
      print "Ok"
    else:
      print "Cancel"
  
  newctpanel = NewCtPanel()
  winManager = ToolsSwingLocator.getWindowManager()
  dialog = winManager.createDialog(
    newctpanel.asJComponent(),
    "Create a new coordinate transform",
    None,
    winManager.BUTTONS_OK_CANCEL
  )    
  dialog.addActionListener(dialogListener)
  dialog.show(WindowManager.MODE.DIALOG)


def main(*args):
  fixFormPanelResourceLoader()

  showNewCtDialog()

