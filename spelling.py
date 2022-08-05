from textblob import TextBlob

def convert(s):
	li = list(s.split())

	return li

def spelling(s):
	s = s.lower()
	words = convert(s)

	correct_words = []
	score = []
	for i in words:
		res = str(TextBlob(i).correct())
		score.append(spelling_score(i, res))
		correct_words.append(res)

	return sum(score) / len(score)

def spelling_score(source: str, target: str):
	s_len = len(source)
	t_len = len(target)

	mat = [[0] * t_len for _ in range(s_len)]
	if source[0] != target[0]:
		mat[0][0] = 1

	for i in range(1,s_len):
		if source[i] == target[0]:
			mat[i][0] = mat[i-1][0]
		else:
			mat[i][0] = mat[i-1][0] + 1

	for i in range(1, t_len):
		if source[0] == target[i]:
			mat[0][i] = mat[0][i-1]
		else:
			mat[0][i] = mat[0][i-1] + 1

	for i in range(1,s_len):
		for j in range(1,t_len):
			cost = 0 if source[i] == target[j] else 1
			mat[i][j] = min(mat[i-1][j-1]+cost, mat[i][j-1]+1, mat[i-1][j]+1)

	return 1 - mat[-1][-1] / max(s_len, t_len)

if __name__ == "__main__":
	print(spelling("machine orageg"))