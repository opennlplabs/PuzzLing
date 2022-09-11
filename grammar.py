from happytransformer import HappyTextToText, TTSettings
from spelling import dp

happy_tt = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
args = TTSettings(num_beams=5, min_length=1)

def grammar_text(sentence: str):
	result_text = happy_tt.generate_text('grammar: ' + sentence, args=args).text
	return result_text


def grammar_score(source: str, target: str):
	return dp(source.lower().split(), target.lower().split())


def grammar(sentence: str, result_text=None):
	if result_text == None:
		result_text = grammar_text(sentence)

	return grammar_score(sentence, result_text)


if __name__ == "__main__":
	print(grammar('this sentence has a bad grammar'))