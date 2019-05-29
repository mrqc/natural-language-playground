# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from lxml import etree
from lxml.html.soupparser import fromstring
import lxml
import requests

class Node:
  siblings = []
  data = None

  def addSibling(self, node):
    self.siblings.append(node)

def nodeAnalyze(node):
  childs = node.getchildren()
  deepText = node.text_content()
  flatTextRaw = node.text
  flatText = ""
  if flatTextRaw != None:
    flatText = flatTextRaw.encode("utf-8").strip()
  return {
    "childs": childs,
    "noOfChilds": len(childs),
    "deepText": "", #deepText,
    "flatText": flatText
  }

def buildCleanTree(node, cleanTree):
  nodeData = nodeAnalyze(node)
  for child in nodeData["childs"]:
    buildCleanTree


request = requests.get("https://www.oe24.at/leute/oesterreich/Adieu-Niki-Ganze-Welt-ehrt-Legende/382246711")
htmlContent = request.text
tree = lxml.html.fromstring(htmlContent)

cleanTree = Tree()
buildCleanTree(tree, cleanTree)

#for node in tree.xpath(".//p"):
#  print nodeAnalyze(node)
