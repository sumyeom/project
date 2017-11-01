# -*- coding: utf-8 -*-
import gensim
import os
import sys
import collections
import smart_open
import random
import string
import glob

i=0

files_name = [[0]*10 for i in range(10)]
#for i in range(2) :
files_name[0] = sys.argv[1]
files_name[1] = sys.argv[2]

#console.log(files_name)
# Preprocess a number of files
for i in range(2):
   f = open('~/Desktop/copybreaker/Form/uploads/'+ files_name[i], 'r')
   s = f.read()
   new = s.replace("\n", ' ')
   f.close()
   if i == 0 :
      f=open('./input.txt','w')
   else:
      f=open('./input.txt','a')
      f.write("\n")
   f.write(new)
   
   f.close()
   ##final enter processing!

# Set file names for train and test data
train_file = './input.txt'

def read_corpus(fname, tokens_only=False):
    with smart_open.smart_open(fname, encoding="utf-8") as f: #utf-8, iso-8859-15
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

train_corpus = list(read_corpus(train_file))


model = gensim.models.doc2vec.Doc2Vec(size=50, min_count=2, iter=55)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count) #, epochs=model.iter

doc_id=0
sims=[]

for doc_id in range(len(train_corpus)):
    inferred_vector = model.infer_vector(train_corpus[doc_id].words)
    sims.append(model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs)))

# Compare and print the most/median/least similar documents from the train corpus
index=0
doc_id=0
result=open('../result1.ejs','w')

result.write("<!DOCTYPE html><html><head><title>result</title><link rel='stylesheet' href='/stylesheets/style.css' /></head><body><h1><%=title%></h1>") 
result.write("<h1><font color=\"RED\"> Similarity:%s </font></h1>"%sims[doc_id][index+1][1])
result.write("<table class=\"type13\"><tr><th> %s </th>"%files_name[0])
result.write("<th> %s </th></tr>"%files_name[1]) 
   

print('Test Document ({}): «{}»\n'.format(doc_id,' '.join(train_corpus[doc_id].words)))
sims_f = float(sims[doc_id][index][1])
result.write("<tr><td> %s </td>"%(' '.join(train_corpus[doc_id].words)))
print(u'Similirity : %s : «%s»\n' % (sims[doc_id][index+1], ' '.join(train_corpus[sims[doc_id][index+1][0]].words)))
result.write("<td>%s:</td>"%' '.join(train_corpus[sims[doc_id][index+1][0]].words))
result.write("</tr></table></body></html>")
result.close()
   



