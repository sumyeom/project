import gensim
import os
import collections
import smart_open
import random
import string
import glob
import sys



i=0

files_name = [[0]*10 for i in range(len(sys.argv)-1)]

for i in range(2, len(sys.argv)) :
   files_name[i-2] = sys.argv[i]

# Preprocess a number of files
for i  in range(len(sys.argv)-2) :
      files_name2 = str(files_name[i]) 
      f = open('/home/seobin/Desktop/copybreaker/Form/uploads/'+ files_name2, 'r')
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
    with smart_open.smart_open(fname, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if tokens_only:
                yield gensim.utils.simple_preprocess(line)
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line), [i])

train_corpus = list(read_corpus(train_file))


model = gensim.models.doc2vec.Doc2Vec(size=300, min_count=5, dm=0, iter=800)
model.build_vocab(train_corpus)
model.train(train_corpus, total_examples=model.corpus_count, epochs=model.iter)

doc_id=0
sims=[]

for doc_id in range(len(train_corpus)):
    inferred_vector = model.infer_vector(train_corpus[doc_id].words)
    sims.append(model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs)))

# Compare and print the most/median/least similar documents from the train corpus
index=0
doc_id=0
result=open('/home/seobin/Desktop/copybreaker/Form/views/result2.ejs','w')
pairs=[]
sim_pair=[[[0 for x in range(2) ]for y in range(len(sys.argv))] for z in range (len(sys.argv))]
 
pair_c=0

flag=0
temp_index=0
result.write("<html><head><title>result</title><link rel='stylesheet' href='/stylesheets/style.css' /></head><body>") 
result.write("<h1> Similarity Pair </h1>") 


##for doc_id in range(0, len(train_corpus)):

for doc_id in range(len(sims)):

   print('Query Document ({}):«{}»\n'.format(doc_id,' '.join(train_corpus[doc_id].words)))

   for index in range( len(sims[doc_id])):

        sims_f = float(sims[doc_id][index][1])
        ##if sims_f > 0.85 and doc_id != int(sims[doc_id][index][0]):
        if doc_id != int(sims[doc_id][index][0]):
            print(u'similirity : %s : «%s»\n' % (sims[doc_id][index], ' '.join(train_corpus[sims[doc_id][index][0]].words)))
            flag=0
            if pair_c==0:
               sim_pair[doc_id][index]=sims[doc_id][index]
            else:
               for i in range(len(sim_pair)):
                  for j in range(len(sim_pair[i])):
                    
                     if sim_pair[i][j][0]==doc_id and i==int(sims[doc_id][index][0]):
                        #i=len(sim_pair)
                        #temp_index=index
                        #index=len(sim_pair[doc_id])
                        flag=1
                        break
                  if flag==1:
                     break
            if flag==1:
              flag=0
              #index=temp_index
            else: 
              sim_pair[doc_id][index]=sims[doc_id][index]         
              pair_c=pair_c+1
           

if pair_c!=0:
   result.write("<table class=\"type12\"><tr><th>file1</th><th>file2</th><th>Similarity</tr>")
for doc_id in range (len(sim_pair)):
   for index in range(len(sim_pair[doc_id])):
    if sim_pair[doc_id][index][1]!=0:
      result.write("<tr><td>%s</td>"%files_name[doc_id])
      result.write("<td>%s</td>"%(files_name[sim_pair[doc_id][index][0]]))
      result.write("<td>%s</td></tr>"%sim_pair[doc_id][index][1])   

if pair_c==0:
   result.write("<h1><font color=\'red\'>No  Similarity Pair</font><h1>")

result.write("</tr></table></body></html>")
result.close()
   





