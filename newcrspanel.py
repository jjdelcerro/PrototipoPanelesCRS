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
    self.setPreferredSize(500,400)

  
def showNewCrsPanel():
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
  dialog.show(WindowManager.MODE.WINDOW)


def main(*args):
  showNewCrsPanel()

