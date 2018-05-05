# encoding: utf-8

import gvsig

import random

from addons.PrototipoPanelesCRS.patchs.fixformpanel import fixFormPanelResourceLoader
from addons.PrototipoPanelesCRS.newcrspanel import  showNewCrsDialog

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from gvsig.libs.formpanel import MouseListenerAdapter
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools.swing.api.windowmanager import WindowManager

from gvsig.libs.formpanel import load_icon

from javax.swing.tree import DefaultTreeCellRenderer

from javax.swing.tree import DefaultMutableTreeNode

from java.awt.event import ActionListener
from org.gvsig.tools.swing.api.windowmanager import WindowManager_v2

from javax.swing import JMenuItem

from javax.swing import JPopupMenu

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

class CRSCellRenderer(DefaultTreeCellRenderer):
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
      (NodeData("EPSG:25830 - ETRS89 / UTM zone 30N", "crs"), None),
    )
  ),
  (NodeData("Favorites", "favourite"), (
      (NodeData("EPSG:25830 - ETRS89 / UTM zone 30N", "crs"), None),
    )
  ),
  (NodeData("EPSG", "folder_closed", "folder_open"), (
      (NodeData("Geographic coordinate systems", "folder_closed","folder_open"), (
          (NodeData("EPSG:3857 - WGS 84 / Pseudo Mercator", "crs"), None),
          (NodeData("EPSG:4326 - WGS 84", "crs"), None)
        )
      ),
      (NodeData("Projected coordinate systems", "folder_closed","folder_open"), (
          (NodeData("EPSG:25829 - ETRS89 / UTM zone 29N", "crs"), None),
          (NodeData("EPSG:25830 - ETRS89 / UTM zone 30N", "crs"), None)
        )
      ),
    )
  ),
  (NodeData("Esri", "folder_closed", "folder_open"),None),
  (NodeData("User", "folder_closed", "folder_open"),None),
  (NodeData("Layers", "folder_closed", "folder_open"),
    (
      (NodeData("EPSG:25830 - ETRS89 / UTM zone 30N", "crs"), None),
    )
  )
)


def makeTree(treenode,nodes):
  for nodeData, childs in nodes:
    node =  DefaultMutableTreeNode(nodeData)
    if childs!=None:
      makeTree(node,childs)
    treenode.add(node)

def createJMenuItem(label, listener, icon=None):
    if icon!=None:
      iconPath = getResource(__file__,"images",icon+".png")
      icon = load_icon(iconPath)
    item = JMenuItem(label, icon)
    item.addActionListener(listener)
    return item


class CrsPanel(FormPanel):
  # pylint: disable=R0904 
  # Too many public methods (%s/%s)
  def __init__(self):
    FormPanel.__init__(self, getResource(__file__, "crspanel.xml"))
    self.setPreferredSize(500,400)
    self.lblFilterSpatial.setVisible(False)
    self.cboFilterSpatial.setVisible(False)
    self.treeResults.setCellRenderer(CRSCellRenderer())

    root = DefaultMutableTreeNode()
    makeTree(root,treeDemo)
    self.treeResults.getModel().setRoot(root)

    self.__selectionListener = None
    self.treeResults.addMouseListener(MouseListenerAdapter(self.treeResults_mouseClicked))
    
  def getProjection(self):
    return random.choice(("EPSG:25830","EPSG:4326", "EPSG:3857"))

  def addSelectionListener(self, listener):
    self.__selectionListener = listener

  def treeResults_mouseClicked(self, event):
    if event.isPopupTrigger():
      return
    if event.getClickCount() != 1:
      return
    tree = event.getSource()
    treePath = tree.getClosestPathForLocation(event.getX(), event.getY())
    if treePath==None :
      return
    tree.setSelectionPath(treePath)
    node = treePath.getLastPathComponent()
    if not node.isLeaf():
      return
    nodeData = node.getUserObject()
    selectedcrs = nodeData.getLabel().split(" ")[0]
    if self.__selectionListener==None:
      return
    self.__selectionListener(selectedcrs)
    
 
  def btnFilterDropdown_click(self, event):  
    menu = JPopupMenu()
    menu.add(createJMenuItem("String Filter", self.enableAlphaFilter, "filter_alpha"))
    menu.add(createJMenuItem("Spatial Filter", self.enableSpatialFilter, "filter_spatial"))
    r = self.lblFilterAlpha.getBounds(None)
    menu.show(self.asJComponent(), r.x, r.y+r.height)

  def btnCrsAdd_click(self, event):
    showNewCrsDialog()
    
  def enableSpatialFilter(self, event):
    self.lblFilterAlpha.setVisible(False)
    self.cboFilterAlpha.setVisible(False)
    self.lblFilterSpatial.setVisible(True)
    self.cboFilterSpatial.setVisible(True)

  def enableAlphaFilter(self, event):
    self.lblFilterAlpha.setVisible(True)
    self.cboFilterAlpha.setVisible(True)
    self.lblFilterSpatial.setVisible(False)
    self.cboFilterSpatial.setVisible(False)
  

def showCrsSelectorDialog(onselect):
  def dialogListener(event):
    if dialog.getAction()==WindowManager_v2.BUTTON_OK:
      onselect(crspanel)
            
  crspanel = CrsPanel()
  winManager = ToolsSwingLocator.getWindowManager()
  dialog = winManager.createDialog(
    crspanel.asJComponent(),
    "Choose a CRS",
    None,
    winManager.BUTTONS_OK_CANCEL
  )    
  dialog.addActionListener(dialogListener)
  dialog.show(WindowManager.MODE.DIALOG)


def showCrsPanel():
  def dialogListener(event):
    if dialog.getAction()==WindowManager_v2.BUTTON_OK:
      print "Ok"
    else:
      print "Cancel"

  fixFormPanelResourceLoader()
  
  crspanel = CrsPanel()
  winManager = ToolsSwingLocator.getWindowManager()
  dialog = winManager.createDialog(
    crspanel.asJComponent(),
    "Select a CRS",
    None,
    winManager.BUTTONS_OK_CANCEL
  )    
  dialog.addActionListener(dialogListener)
  dialog.show(WindowManager.MODE.WINDOW)


def main(*args):
  showCrsPanel()

