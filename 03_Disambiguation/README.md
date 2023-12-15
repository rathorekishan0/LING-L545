# Morphological disambiguation

## Tagger comparison

### Process Description

For comparing Part of speech taggers I chose [UDPipe](https://github.com/ufal/udpipe), [machamp](https://github.com/machamp-nlp/machamp)  and [spaCy](https://github.com/explosion/spaCy) for Spanish language.

I downloaded treebank for spanish from https://github.com/UniversalDependencies/UD_Spanish-AnCora which has train ,dev and test Conll-u file. I trained the POS tagger for UDPipe and machamp using the train and dev files and for spacy I used their pre trained model for spanish [es_core_news_sm](https://spacy.io/models/es).

Training for UDPipe and machamp were similar as I just had to pass training data to UDPipe and training and dev data to machamp. A good thing about these 2 models are that they are language agnositic, they onky require the UD treebank data to train. But training takes lot of time for systems without gpu. 

After training the models all I had to do was pass the test treebank Conll-u file as an input and they were able to generate the POS tags for all the sentences. For spaCy I had to give individual sentences to the model to generate POS tags and then converted them in CoNLL-U format.

```
import spacy
from spacy_conll import ConllFormatter

nlp = spacy.load("es_core_news_sm")

def pos_tag_sentence(sentence):
    doc = nlp(sentence)
    return [(token.text, token.pos_) for token in doc]

def process_conll_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    output_lines = []
    current_sent_id = None
    current_text = []

    for line in lines:
        if line.startswith("# sent_id"):
            current_sent_id = line.split('=')[1].strip()
        elif line.startswith("# text"):
            current_text = line.split('=')[1].strip()
        elif line == '\n':
            if current_sent_id and current_text:
                output_lines.append(f"# sent_id = {current_sent_id}\n# text = {current_text}")
                tagged_sentence = pos_tag_sentence(current_text)
                for i, (word, pos) in enumerate(tagged_sentence, start=1):
                    output_lines.append(f"{i}\t{word}\t0\t{pos}\t0\t0\t0\t0\t0\t0")
                output_lines.append('\n')
            current_sent_id = None
            current_text = []
        else:
            continue
            # output_lines.append(line.rstrip())

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(output_lines))

input_file_path = 'es_ancora-ud-test.conllu'
output_file_path = 'spacy_output.conllu'

process_conll_file(input_file_path, output_file_path)
```

### Evaluation
To evaluate the performance I used `conll17_ud_eval.py` to compare the metrics.

Here are the metrics results for all 3 taggers:

#### UDPipe

```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     98.27 |     98.27 |     98.27 |     98.27
XPOS       |     94.98 |     94.98 |     94.98 |     94.98
Feats      |     97.99 |     97.99 |     97.99 |     97.99
AllTags    |     94.60 |     94.60 |     94.60 |     94.60
Lemmas     |     98.24 |     98.24 |     98.24 |     98.24
UAS        |    100.00 |    100.00 |    100.00 |    100.00
LAS        |    100.00 |    100.00 |    100.00 |    100.00
```

#### machamp

```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     98.49 |     98.49 |     98.49 |     98.49
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     98.49 |     98.49 |     98.49 |     98.49
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |    100.00 |    100.00 |    100.00 |    100.00
LAS        |    100.00 |    100.00 |    100.00 |    100.00
```

#### spaCy

```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |     99.91 |     99.89 |     99.90 |
Sentences  |      0.03 |      0.06 |      0.04 |
Words      |     97.69 |     95.54 |     96.60 |
UPOS       |     95.50 |     93.40 |     94.44 |     97.76
XPOS       |      0.00 |      0.00 |      0.00 |      0.00
Feats      |      0.00 |      0.00 |      0.00 |      0.00
AllTags    |      0.00 |      0.00 |      0.00 |      0.00
Lemmas     |      0.00 |      0.00 |      0.00 |      0.00
UAS        |      3.26 |      3.18 |      3.22 |      3.33
LAS        |      0.00 |      0.00 |      0.00 |      0.00
```

From the above metrics we can see that out of all machamp performed better but UDpipe also is very close to machamp in terms of the accuracies. Evem spaCy performance is also good giving precision, recall and F1-score more than 90%. 
