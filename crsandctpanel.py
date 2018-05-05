# encoding: utf-8

import gvsig

from addons.PrototipoPanelesCRS.patchs.fixformpanel import fixFormPanelResourceLoader
from addons.PrototipoPanelesCRS.crspanel import CrsPanel
from addons.PrototipoPanelesCRS.ctpanel import CtPanel

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools.swing.api.windowmanager import WindowManager_v2 as WindowManager

from java.awt import BorderLayout

class CrsAndCtPanel(FormPanel):
  # pylint: disable=R0904 
  # Too many public methods (%s/%s)
  def __init__(self, targetCRS=None):
    FormPanel.__init__(self, getResource(__file__, "crsandctpanel.xml"))
    self.setPreferredSize(500,400)
    self.__targetCRS = targetCRS
    self.__crspanel = CrsPanel()
    self.__ctpanel = CtPanel()

    if self.__targetCRS == None:
      self.tabMain.setEnabledAt(1, False)
    else:
      self.__ctpanel.setTargetCRS(self.__targetCRS)
      self.__crspanel.addSelectionListener(self.onSelectCRS)
      
    self.crsContainer.setLayout(BorderLayout())
    self.transformContainer.setLayout(BorderLayout())
    
    self.crsContainer.add(self.__crspanel.asJComponent(), BorderLayout.CENTER)
    self.transformContainer.add(self.__ctpanel.asJComponent(), BorderLayout.CENTER)

    self.__ctpanel.setEnabledCRSTargetSelector(False)
    self.__ctpanel.setEnabledCRSSourceSelector(False)

  def onSelectCRS(self, selectedCRS):
    self.__ctpanel.setSourceCRS(selectedCRS)
    if selectedCRS == self.__ctpanel.getTargetCRS():
      self.tabMain.setEnabledAt(1, False)
    else:
      self.tabMain.setEnabledAt(1, True)

def showCrsAndCtDialog():
  def dialogListener(event):
    if dialog.getAction() == WindowManager.BUTTON_OK:
      print "Ok"
    else:
      print "Cancel"
    
  fixFormPanelResourceLoader()
  
  panel = CrsAndCtPanel("EPSG:25830")
  winManager = ToolsSwingLocator.getWindowManager()
  dialog = winManager.createDialog(
    panel.asJComponent(),
    "Create a new CRS",
    None,
    winManager.BUTTONS_OK_CANCEL
  )    
  dialog.addActionListener(dialogListener)
  dialog.show(WindowManager.MODE.DIALOG)


def main(*args):
  showCrsAndCtDialog()

