# encoding: utf-8

import gvsig

from addons.PrototipoPanelesCRS.patchs.fixformpanel import fixFormPanelResourceLoader
from addons.PrototipoPanelesCRS.crspanel import showCrsSelectorDialog
from addons.PrototipoPanelesCRS.newctpanel import showNewCtDialog
import random
from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools.swing.api.windowmanager import WindowManager

from gvsig.libs.formpanel import load_icon

from javax.swing.tree import DefaultTreeCellRenderer

from javax.swing.tree import DefaultMutableTreeNode

from java.awt.event import ActionListener
from org.gvsig.tools.swing.api.windowmanager import WindowManager_v2

class NodeData(object):
  def __init__(self, label, iconName, iconNameOpen=None):
    self.__label = label
    iconPath = getResource(__file__,"images",iconName+".png")
    self.__iconClosed = load_icon(iconPath)
    if iconNameOpen==None:
      self.__iconOpen = self.__iconClosed
    else:
      iconPath = getResource(__file__,"images",iconNameOpen+".png")
      self.__iconOpen = load_icon(iconPath)
    
    
  def getLabel(self):
    return self.__label

  __repr__ = getLabel
  
  def getIconClosed(self):
    return self.__iconClosed
  
  def getIconOpen(self):
    return self.__iconOpen

class CtCellRenderer(DefaultTreeCellRenderer):
  def __init__(self):
    pass
    
  def getTreeCellRendererComponent(self, tree, value, selected, expanded, isLeaf, row, focused):
    c = DefaultTreeCellRenderer.getTreeCellRendererComponent(self, tree, value, selected, expanded, isLeaf, row, focused)
    nodeData = value.getUserObject()
    if nodeData!=None:
      if isLeaf:
        self.setIcon(nodeData.getIconClosed())
      else:
        self.setIcon(nodeData.getIconOpen())
    return c

treeDemo = (
  (NodeData("Recents", "recents"), (
      (NodeData("EPSG:1149 - ETRS89 to WGS 84", "ct"), None),
    )
  ),
  (NodeData("Favorites", "favourite"), (
      (NodeData("EPSG:1571 - Amersfoort to ETRS89", "ct"), None),
    )
  ),
  (NodeData("EPSG", "folder_closed", "folder_open"), (
      (NodeData("EPSG:1149 - ETRS89 to WGS 84", "ct"), None),
      (NodeData("EPSG:1571 - Amersfoort to ETRS89", "ct"), None),
    )
  ),
  (NodeData("Grids", "folder_closed", "folder_open"), (
      (NodeData("BALR2009.gsb", "ct"), None),
      (NodeData("CA61_003.gsb", "ct"), None),
      (NodeData("CA7072_003.gsb", "ct"), None),
      (NodeData("canoa_wgs84_mb.gsb", "ct"), None),
      (NodeData("D73_ETRS89_geo.gsb", "ct"), None),
      (NodeData("DLX_ETRS89_geo.gsb", "ct"), None),
      (NodeData("PENR2009.gsb", "ct"), None),
      (NodeData("sped2et.gsb", "ct"), None),
    )
  ),
  (NodeData("User", "folder_closed", "folder_open"),None),
)


def makeTree(treenode,nodes):
  for nodeData, childs in nodes:
    node =  DefaultMutableTreeNode(nodeData)
    if childs!=None:
      makeTree(node,childs)
    treenode.add(node)

class CtPanel(FormPanel):
  # pylint: disable=R0904 
  # Too many public methods (%s/%s)
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "ctpanel.xml"))
    self.setPreferredSize(500,400)
    self.treeResults.setCellRenderer(CtCellRenderer())

    root = DefaultMutableTreeNode()
    makeTree(root,treeDemo)
    self.treeResults.getModel().setRoot(root)

  def btnSelectSoureCRS_click(self, evet):
    def onChooseSourceCrs(crspanel):
      self.txtSourceCRS.setText(crspanel.getProjection())
    showCrsSelectorDialog(onChooseSourceCrs)

  def btnSelectTargetCRS_click(self, evet):
    def onChooseTargetCrs(crspanel):
      self.txtTargetCRS.setText(crspanel.getProjection())
    showCrsSelectorDialog(onChooseTargetCrs)

  def btnCtAdd_click(self, event):
    showNewCtDialog()

  def getTransform(self):
    return random.choice(("EPSG:1149","EPSG:1571"))

  def setTargetCRS(self, crs):
    self.txtTargetCRS.setText(crs)

  def getTargetCRS(self):
    return self.txtTargetCRS.getText()
    
  def setSourceCRS(self, crs):
    self.txtSourceCRS.setText(crs)

  def getSourceCRS(self):
    return self.txtSourceCRS.getText()

  def setEnabledCRSTargetSelector(self, enabled):
    self.btnSelectTargetCRS.setEnabled(enabled)
    
  def setEnabledCRSSourceSelector(self, enabled):
    self.btnSelectSoureCRS.setEnabled(enabled)
    
def showCtPanel():
  def dialogListener(event):
    if dialog.getAction()==WindowManager_v2.BUTTON_OK:
      print "Ok"
    else:
      print "Cancel"

  fixFormPanelResourceLoader()
  
  ctpanel = CtPanel()
  winManager = ToolsSwingLocator.getWindowManager()
  dialog = winManager.createDialog(
    ctpanel.asJComponent(),
    "Choose a coordinate transform",
    None,
    winManager.BUTTONS_OK_CANCEL
  )    
  dialog.addActionListener(dialogListener)
  dialog.show(WindowManager.MODE.WINDOW)

def main(*args):
  showCtPanel()

