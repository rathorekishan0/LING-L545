import sys
text = sys.stdin.read()
dictionary_form_path = sys.argv[1]
dictionary_form = set()
with open(dictionary_form_path,'r') as f:
    lines = f.readlines()

for line in lines:
    dictionary_form.add(line.strip())

text = text.strip()
tokens = []
i=0
while i<len(text):
    match= False
    for j in range(len(text),i,-1):
        curr = text[i:j]
        if curr in dictionary_form:
            tokens.append(curr)
            i=j
            match=True
            break
    if not match:
        tokens.append(text)
        i+=1
with open('output_token', 'w') as f:
    f.write(' '.join(tokens))
