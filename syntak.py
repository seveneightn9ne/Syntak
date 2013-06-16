import nltk
from sets import Set
# from nltk.tag.stanford import StanfordTagger
# nltk.internals.config_java("C:/Program Files/Java/jdk1.7.0_04/bin/java.exe")
# path_to_model = "C:/Dropbox/_Ubuntu/project/NLTK/src/lib/wsj-0-18-bidirectional-distsim.tagger"
# path_to_jar = "C:/Dropbox/_Ubuntu/project/NLTK/src/lib/stanford-postagger.jar"

# tagger = StanfordTagger(path_to_model, path_to_jar)
# tokens = nltk.tokenize.word_tokenize("I hope this works!")
# print tagger.tag(tokens)
class Closed(object):
	def __init__(self):
		self.quantifiers = Set("BILLION BILLIONTH EIGHT EIGHTEEN EIGHTEENTH EIGHTH EIGHTIETH EIGHTY ELEVEN ELEVENTH FIFTEEN FIFTEENTH FIFTH FIFTIETH FIFTY FIRST FIVE FORTIETH FORTY FOUR FOURTEEN FOURTEENTH FOURTH HUNDRED HUNDREDTH LAST MILLION MILLIONTH NEXT NINE NINETEEN NINETEENTH NINETIETH NINETY NINTH ONCE ONE SECOND SEVEN SEVENTEEN SEVENTEENTH SEVENTH SEVENTIETH SEVENTY SIX SIXTEEN SIXTEENTH SIXTH SIXTIETH SIXTY TEN TENTH THIRD THIRTEEN THIRTEENTH THIRTIETH THIRTY THOUSAND THOUSANDTH THREE THRICE TWELFTH TWELVE TWENTIETH TWENTY TWICE TWO".lower().split(" "))
		self.adverbs = Set("AGAIN AGO ALMOST ALREADY ALSO ALWAYS ANYWHERE BACK ELSE EVEN EVER EVERYWHERE FAR HENCE HERE HITHER HOW HOWEVER NEAR NEARBY NEARLY NEVER NOT NOW NOWHERE OFTEN ONLY QUITE RATHER SOMETIMES SOMEWHERE SOON STILL THEN THENCE THERE THEREFORE THITHER THUS TODAY TOMORROW TOO UNDERNEATH VERY WHEN WHENCE WHERE WHITHER WHY YES YESTERDAY YET".lower().split(" "))
		self.modals = Set("can may will shall could might would should must".lower().split(" "))
		self.auxiliaries = Set("AM ARE AREN'T BE BEEN BEING CAN CAN'T COULD COULDN'T DID DIDN'T DO DOES DOESN'T DOING DONE DON'T GET GETS GETTING GOT HAD HADN'T HAS HASN'T HAVE HAVEN'T HAVING HE'D HE'LL HE'S I'D I'LL I'M IS I'VE ISN'T IT'S MAY MIGHT MUST MUSTN'T OUGHT OUGHTN'T SHALL SHAN'T SHE'D SHE'LL SHE'S SHOULD SHOULDN'T THAT'S THEY'D THEY'LL THEY'RE WAS WASN'T WE'D WE'LL WERE WE'RE WEREN'T WE'VE WILL WON'T WOULD WOULDN'T YOU'D YOU'LL YOU'RE YOU'VE".lower().split(" "))
		self.prepositions = Set("ABOUT ABOVE AFTER ALONG ALTHOUGH AMONG AND AROUND AS AT BEFORE BELOW BENEATH BESIDE BETWEEN BEYOND BUT BY DOWN DURING EXCEPT FOR FROM IF IN INTO NEAR NOR OF OFF ON OR OUT OVER ROUND SINCE SO THAN THAT THOUGH THROUGH TILL TO TOWARDS UNDER UNLESS UNTIL UP WHEREAS WHILE WITH WITHIN WITHOUT".lower().split(" "))
		self.conjunctions = Set("and but after when as because if what where which how than or so before since while although though who whose".lower().split(" "))
		self.determiners = Set("the some this that every all both one first other next many much more most several no a an any each no half twice two second another last few little less least own".lower().split(" "))
		self.pronouns = Set("I you he me her him my mine her hers his myself himself herself anything everything anyone everyone ones such it we they us them our ours their theirs itself ourselves themselves something nothing someone".lower().split(" "))

		self.auxiliaries.update(self.modals)

		def updateSetFromFile(myset, path):
			return myset.update([word.strip("\n") for word in open(path).readlines() if not word.startswith("//")])

		updateSetFromFile(self.auxiliaries, "function_words/EnglishAuxiliaryVerbs.txt")
		updateSetFromFile(self.conjunctions, "function_words/EnglishConjunctions.txt")
		updateSetFromFile(self.determiners, "function_words/EnglishDeterminers.txt")
		updateSetFromFile(self.prepositions, "function_words/EnglishPrepositions.txt")
		updateSetFromFile(self.pronouns, "function_words/EnglishPronouns.txt")
		updateSetFromFile(self.quantifiers, "function_words/EnglishQuantifiers.txt")

		self.words={}
		self.words["quantifiers"]=self.quantifiers
		self.words["adverbs"]=self.adverbs
		self.words["modals"]=self.modals
		self.words["auxiliaries"]=self.auxiliaries # includes modals
		self.words["prepositions"]=self.prepositions #includes (some?) conjunctions
		self.words["conjunctions"]=self.conjunctions
		self.words["determiners"]=self.determiners
		self.words["pronouns"]=self.pronouns

		self.phrasewords = [] #e.g. "have to"
		self.phrasewords_fixed = [] #e.g. have_to"
		for wordset in self.words:
			for word in wordset:
				if len(word.split(" ")) > 1:
					self.phrasewords.append(word)
					word.replace(" ","_")
					self.phrasewords_fixed.append(word)
	def POS(self, word):
		if word in self.quantifiers or word in self.adverbs: 
			return "A"
		elif word in self.modals or word in self.auxiliaries:
			return "V"
		elif word in self.prepositions:
			return "P"
		elif word in self.conjunctions:
			return "C"
		elif word in self.determiners:
			return "D"
		elif word in self.pronouns:
			return "N"
		else:
			return None


class TreeNode(object):
	def __init__(self, label, children=[], sentence=None):
		self.usedIndices = Set()
		self.sentence = sentence
		self.label = label #string
		if not isinstance(children, list):
			children = [children,]
		self.children = children #list of len 0,1,2
	def __str__(self):
		if(len(self.children)>0):
			return "[" + self.label + " " + ", ".join(map(str, self.children)) + "]"
		elif(len(self.children)==1):
			return "[" + self.label + ": " + str(self.children[0]) 
		return self.label
	def append(self, node):
		if isinstance(node, TreeNode):
			if self.sentence:
				node.sentence = self.sentence
			else:
				node.sentence = self
		self.children.append(node)
	# def setSentence(self, sentence):
	# 	self.sentence = sentence
	# 	for child in self.children:
	# 		if isinstance(child, TreeNode):
	# 			child.setSentence(sentence)

class NP(TreeNode):
	def __init__(self, label="NP", children=[], sentence=None, index=""):
		super(NP,self).__init__(label, children, sentence)

		#set default index to next unused index
		index_try = "i"
		while index=="":
			if index_try in self.sentence.usedIndices:
				index_try=chr(ord(index_try)+1)
			else:
				index = index_try
		self.index = index
		self.sentence.usedIndices.add(index)
	def __str__(self):
		return TreeNode.__str__(self) + self.index

class Test(object):
	tests = {
		"I see." : "[S [NP [N I]]i, [VP [V see]]]",
		"Jack will jump." : "[S [NP [N Jack]] [VP [V will], [V jump]]]",
		"The bunny hops." : "[S [NP [D The], [N bunny]]i [VP [V hops]]]"
	}

#main
closed = Closed()

def makeTree(sentence):
	tree = TreeNode("S")
	#split conjunctions
	# sentence.replace("I'm","I am")
	# sentence.replace("I've","I have")
	# sentence.replace("I'll","I will")
	# sentence.replace("I'd","I would")
	# sentence.replace("He'd","He would")
	# sentence.replace("He's","He is")
	# sentence.replace("She's","She is")
	# sentence.replace("She'd","She would")
	# sentence.replace("She'd","She would")
	#combine phrase words
	for phraseword, fixed in zip(closed.phrasewords, closed.phrasewords_fixed):
		sentence.replace(phraseword, fixed)

	#Find first NP
	words = sentence.strip(".").split(" ")
	labels = ["" for word in words]
	for i in range(0,len(words)):
		pos = closed.POS(words[i].lower())
		if pos:
			labels[i]=pos
		else:
			labels[i]=""

	# simplest sentences
	if len(words)==2:
		tree.append(NP("NP", [TreeNode("N", [words[0]], tree)], tree))
		tree.append(TreeNode("VP", [TreeNode("V", [words[1]], tree)], tree))

	# auxiliaries as cue for VP
	

	#... 

	return tree



print "Running tests.."
tester = Test()
for test in tester.tests:
	print test
	a = makeTree(test)
	if str(a)==tester.tests[test]:
		print "PASS"
	else:
		print "FAIL: "+str(a)+" should be "+tester.tests[test]
