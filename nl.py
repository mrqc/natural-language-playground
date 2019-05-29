# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
from nltk.stem.cistem import Cistem
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import treebank

sentence = """

Niki Lauda starb am 20. Mai in Zuerich. Jetzt tritt die Legende ihre letzte Reise an. 

Ihn als groeszten Rennfahrer aller Zeiten zu beschreiben, waere zu kurz gefasst. Niki Lauda war eine Instanz, ein Aushaengeschild unseres Landes. Er war pointierter und hoch charismatischer Chronist, Vorbild fuer viele Generationen, Humanist, ein Erfolgsmensch, Idol.

 Tausende Fans erweisen Niki Lauda die letzte Ehre

Um 7.30 Uhr wurde die Rennfahrerlegende in der Mitte des Stephansdoms im geschlossenen Sarg aufgebahrt. Seine letzte Reise wird Lauda in seinem beruehmten Rennanzug antreten. Auf dem Sarg legte Birgit Lauda gemeinsam mit Dompfarrer Toni Faber, der durch die Trauerfeierlichkeiten fuehrt, den Rennhelm der Formel 1 Ikone ab.

Vor dem Requiem haben Fans und Bewunderer die Moeglichkeit, ihrem Idol die letzte Ehre zu erweisen. Toni Faber rechnet mit mehr als 5.000 Menschen, die vom rechten Seitentor des Doms am Sarg Laudas vorbeidefilieren und am noerdlichen Seitentor die Kirche wieder verlassen.

 Bundespraesident Van der Bellen haelt Trauerrede

Um 12 Uhr wird der Sarg zur Kommunionsbank im vorderen Teil des Doms gebracht. Mehr als 400 Sitzplaetze sind fuer geladene Trauergaeste reserviert. Der Bereich links des Sargs ist fuer Familie und enge Freunde vorgesehen.

Ein Blaeserensemble und ein Organist intonieren zum Einzug das Heilig,Lied von Franz Schubert. Im Anschluss haelt Dompfarrer Faber eine Predigt. Auf jeden Fall, so Faber, wolle er sich kurz halten.

Birgit Lauda hat fuer die Trauermesse Lieblingssongs ihres verstorbenen Mannes ausgesucht (siehe unten). Interpretiert werden die Stuecke vom Musiker Christian Kolonovits mit den Saengern Joni Madden und Drew Sarich.

Die Reden werden von Bundespraesident Alexander Van der Bellen, Rennfahrerkollege Gerhard Berger und Arnold Schwarzenegger gehalten. Im Anschluss folgen die Fuerbitten der Kinder von Lauda: die Zwillinge Mia und Max sowie Mathias und Lukas.

Die Kleine Pummerin laeutet. Anschlieszend wird Niki Lauda im engsten Kreis der Familie auf einem Wiener Friedhof beigesetzt. (zac)
Imagine Fast Car , Laudas Lieblings,Lieder erklingen 

Lieder von Tracy Chapman bis John Lennon , fuer die musikalische Begleitung des Requiems hat Birgit Lauda die Lieblingssongs von Niki zusammengestellt. 


Trauerfeier im Stephansdom

Heute steht Wien ganz im Zeichen der Trauerfeier fuer einen der beruehmtesten Sportler: Niki Lauda wird im Stephansdom feierlich verabschiedet. Der Sarg der Motorsport,Legende aus Wien war bis 11.30 Uhr im Dom oeffentlich aufgebahrt, um 13.00 Uhr folgt das Requiem.

Beim Requiem sind unter anderem Bundespraesident Alexander Van der Bellen, Ex,Formel,1,Fahrer Gerhard Berger sowie Arnold Schwarzenegger als Redner vorgesehen. Die Lesung wird Laudas Ex,Teamkollege Alain Prost halten.

Lauda war am 20. Mai mit 70 Jahren in Zuerich verstorben.


Vorbereitungen fuer Requiem

Nach dem Ende der Aufbahrung wird der Sarg von Niki Lauda im Stephansdom von der Vierung zur Kommunionbank umgebettet. Ab 12.15 Uhr duerfen die allgemeinen Trauergaeste bis zu einer Absperrung in den Dom. Vor der Absperrung befindet sich der Bereich fuer die geladenen Trauergaeste. Das Requiem beginnt um 13.00 Uhr.


Oeffentliche Aufbahrung beendet

Eine in Wien lebende Polin war den Traenen nahe als sie nach fast einer Stunde des Wartens erkennen musste, dass es sich nicht mehr ausgeht. Die Frau wollte eine rote und eine weisze Rose vor dem Sarg niederlegen. Ich war ein Riesenfan von ihm. Fuer mich war es sehr wichtig, ihm heute auf Wiedersehen zu sagen.

Hunderte schafften es nicht mehr rechtzeitig zur Aufbahrung in den Stephansdom

Hunderte Menschen haben erkannt, dass es sich nicht mehr ausgeht und haben sich deshalb bereits vor dem Riesentor fuers Requiem versammelt.



"""

def printTree(obj, level):
  for subObj in obj:
    if type(subObj) is nltk.tree.Tree:
      print " " * (2 * level), subObj.label()
      printTree(subObj, level + 1)
    elif type(subObj) == tuple:
      print " " * (2 * level), subObj
    else:
      print "Error: no tree representation", subObj

def wordInLeaves(word, leaves):
  for index, leave in enumerate(leaves):
    if word == leave[0]:
      return index
  return -1

def getNodePathOfTreeForLeafNode(tree, token):
  attributes = []
  for subObj in tree:
    if type(subObj) is nltk.tree.Tree:
      attributesTmp = getNodePathOfTreeForLeafNode(subObj, token)
      if len(attributesTmp) > 0:
        attributes = attributes + attributesTmp + [subObj.label()]
    elif type(subObj) == tuple:
      if subObj[0] == token[0]:
        attributes = attributes + [subObj[1]]
    else:
      print "Error: no tree iteration for object", subObj
      quit()
  return attributes

def attributeToken(token, tree):
  leafIndex = wordInLeaves(token[0], tree.leaves())
  if leafIndex >= 0:
    return getNodePathOfTreeForLeafNode(tree, token)
  return ""

stopWords = set(stopwords.words("german"))
sentenceTokenizer = nltk.tokenize.PunktSentenceTokenizer()
sentenceTokens = sentenceTokenizer.tokenize(sentence)
for sentence in sentenceTokens:
  wordTokenizer = nltk.tokenize.WordPunctTokenizer()
  wordTokens = wordTokenizer.tokenize(sentence)
  taggedSent = nltk.pos_tag(wordTokens)
  tree = nltk.chunk.ne_chunk(taggedSent)
  #printTree(tree, 1)
  print "--"
  index = 0
  while index < len(taggedSent):
    if taggedSent[index][0].lower() in stopWords:
      index = index + 1
    else:
      textTokens = []
      oldTokenAttributes = None
      tokenAttributes = []
      while taggedSent[index][1] == "NNP":
        tokenAttributes = attributeToken(taggedSent[index], tree)
        if tokenAttributes == oldTokenAttributes or oldTokenAttributes == None:
          textTokens.append(taggedSent[index])
          index = index + 1
          oldTokenAttributes = tokenAttributes
        else:
          break
      else:
        index = index + 1
      if len(textTokens) > 0:
        text = ""
        for tokenIndex, token in enumerate(textTokens):
          if tokenIndex < len(textTokens) - 1:
            text = text + token[0] + str(attributeToken(token, tree)) + " "
          elif token[1] != ":":
            text = text + token[0] + str(attributeToken(token, tree))
        if text != "":
          print text
          pass
  tree.draw()
