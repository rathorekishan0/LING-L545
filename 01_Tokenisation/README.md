# Segmentation and tokenisation
----

## Segmentation
For the given practical I chose Hindi to test the segmentation tool [indic_nlp_library](https://github.com/anoopkunchukuttan/indic_nlp_library/tree/master). This library is specially made for many indian langues and can be used for other nlp operations. In our case I used their library `indicnlp.tokenize.sentence_tokenize`. Their method for segmentation is a rule based approach in which they apply different regular expressions to segment text into multiple sentences. 

You can find the source code [here](https://github.com/anoopkunchukuttan/indic_nlp_library/blob/master/indicnlp/tokenize/sentence_tokenize.py). The code looks for different conditions in which a setence could end like `।` which is typically used in hindi to end a sentences. Funnily call it as "danda" in their code which literally means stick but the actual name for this punctuation mark in "Purna Viram" which means Full Stop. But apart from that also made sure to look for different condtions in which a sentence could end like full stop or if there is a new line or too many spaces. Their code is written in python and to run it would need to install their library `indic-nlp-library`.

## Evaluation
### Quantitive Evaluation
To evaluate it performance I took 10 random paragraphs from wiki dump which had 133 sentences. Using the tool I was able to extract out 142 sentences from the text out of which only 108 were correct giving it an accuracy of 81%.

### Qualitative Evaluation
By looking at the segmented sentences the tool worked great for sentences which had full stops both in hindi and english. But since the given data of paragraph was not clean the segmentation could not handle how to treat empty lines or sentences that have qoutes `"` after the full stop. The data also had some random characters in between like `]]` or `)'` since the data was not cleaned. But a cleaned data it can give a better accuarcy. 

  
<br>
<br>

---
---

# Tokenization

The code for maxmatch is present in `maxmatch.py` file 
To run the program you would have to pass the text and the dictionary file in this format:
`echo '多くの女性が生理のことで悩んでいます。' | python maxmatch.py dictionary-file`
The program will take the text and dictionary file and generate tokens in file `output_token`

If you want to generate a dictionary file for a different language you can run the `tokenization.ipynb` notebook in which you'll have to pass the Conll-u file in it and then it will generate the dictionary file.

To evaluate it performance you will have to text the original tokens in a file and use `wer.py` to check the word accuracy rate. I ran it for two random sentence and it gave me an error rate of 30.77% and 25% respectively 

```
REF: 多く の 女性 が 生理   の こと で 悩ん で い  ます 。 
HYP: 多く の 女性 が 生  理 の こと で 悩ん で いま す  。 
EVA:           S  I             S  S    
WER: 30.77%
```
```
REF: なん だ よ なん だ よぉ                               ~ , わが 署 に 来 た の なら    て くれ よぉ                               ~ 。 
HYP: なん だ よ なん だ よ  なんだよなんだよぉ~,わが署に来たのなら教えてくれよぉ~。 ~ , わが 署 に 来 た の なら 教え て くれ よ  なんだよなんだよぉ~,わが署に来たのなら教えてくれよぉ~。 ~ 。 
EVA:             S  I                                                 I       S  I                                 
WER: 25.00%
```

This means that the tokenizer differed by 30.77% and 25% from the original tokens.
