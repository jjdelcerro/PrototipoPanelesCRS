# encoding: utf-8

import gvsig

from addons.PrototipoPanelesCRS.patchs.fixformpanel import fixFormPanelResourceLoader

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools.swing.api.windowmanager import WindowManager_v2 as WindowManager

class NewCrsPanel(FormPanel):
  # pylint: disable=R0904 
  # Too many public methods (%s/%s)
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "newcrspanel.xml"))
    self.setPreferredSize(300,200)
    self.txtCode.setEditable(False)
    
  def btnForceCode_click(self, event):
    self.txtCode.setEditable(True)
    self.btnForceCode.setEnabled(False)
    self.txtCode.requestFocusInWindow()
    

  
def showNewCrsDialog():
  def dialogListener(event):
    if dialog.getAction() == WindowManager.BUTTON_OK:
      print "Ok"
    else:
      print "Cancel"
    
  fixFormPanelResourceLoader()
  
  newcrspanel = NewCrsPanel()
  winManager = ToolsSwingLocator.getWindowManager()
  dialog = winManager.createDialog(
    newcrspanel.asJComponent(),
    "Create a new CRS",
    None,
    winManager.BUTTONS_OK_CANCEL
  )    
  dialog.addActionListener(dialogListener)
  dialog.show(WindowManager.MODE.DIALOG)


def main(*args):
  showNewCrsDialog()

