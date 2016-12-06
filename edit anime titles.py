readfrom = 'animetitles.txt'
writeto = 'foo.txt'


with open(readfrom, "rt") as f:
        temp = f.read()
titles = temp.split('\n')

filtered = filter(lambda s: '|1|' in s, titles)
text = ""
for line in filtered:
	text += line
	text += '\n'


with open(writeto, "wt") as f:
    f.write(text)
