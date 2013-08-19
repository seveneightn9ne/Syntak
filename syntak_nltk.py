import nltk, sys

def collect_data()
def analyze(sentence):
	""" Main function which performs analysis and displays results """
	text = nltk.word_tokenize(sentence)
	post = nltk.pos_tag(text)
	print post
	for word, tag in post:


if __name__ == "__main__":
	if len(sys.argv == 2):
		analyze(sys.argv[1])
	else:
		while True:
			sentence = raw_input("Sentence: ")
			analyze(sentence)