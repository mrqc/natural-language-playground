# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from lxml import etree
from lxml.html.soupparser import fromstring
import lxml
import requests

def nodeAnalyze(node):
  childs = node.getchildren()
  deepText = node.text_content().encode("utf-8").strip()
  flatTextRaw = node.text
  tagName = node.tag
  flatText = ""
  if flatTextRaw != None:
    flatText = flatTextRaw.encode("utf-8").strip()
  return {
    "childs": "", #childs,
    "noOfChilds": len(childs),
    "deepText": "", #deepText,
    "deepTextLength": len(deepText),
    "flatText": flatText,
    "flatTextLength": len(flatText),
    "tagName": tagName
  }

def cleanTree(tree):
  toRemove = []
  for child in tree:
    cleanTree(child)
    if isinstance(child, lxml.html.HtmlComment):
      toRemove.append(child)
    else:
      nodeData = nodeAnalyze(child)
      if nodeData["tagName"] == "script":
        toRemove.append(child)
      elif nodeData["noOfChilds"] == 0 and nodeData["flatText"] == "":
        toRemove.append(child)
      elif nodeData["tagName"] == "img":
        toRemove.append(child)
      #else:
      #  print nodeData
  for element in toRemove:
    element.getparent().remove(element)

def iterateTree(tree):
  nodeData = nodeAnalyze(tree)
  if nodeData["noOfChilds"] == 0:
    print "--"
    processNodeUpwards(tree)
    print "--"
  else:
   for child in tree:
     iterateTree(child)

def processNodeUpwards(leafNode):
  nodeData = nodeAnalyze(leafNode)
  print nodeData
  if leafNode.getparent() != None:
    processNodeUpwards(leafNode.getparent())

request = requests.get("https://www.oe24.at/leute/oesterreich/Adieu-Niki-Ganze-Welt-ehrt-Legende/382246711")
htmlContent = request.text
tree = lxml.html.fromstring(htmlContent)
cleanTree(tree)
iterateTree(tree)

#nodes = tree.xpath(".//*")
#for node in nodes:
#  print nodeAnalyze(node)
