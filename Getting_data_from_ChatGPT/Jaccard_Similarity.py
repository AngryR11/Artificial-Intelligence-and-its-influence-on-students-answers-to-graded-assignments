#Written by Gustavo Saraiva on 22 of July of 2024
#== python3 Jaccard_Similarity.py

#You need to run "source myenv/bin/activate" each time you open python

#====importing required packages====
from nltk.tokenize import RegexpTokenizer#for word similarity
from datasketch import MinHash #to compute the estimated Jacart Similarity
import pandas as pd
import numpy as np
import time
import datetime
#===================================

start_time = time.time()
#==========Jaccard Similarity============================================
tokenizer = RegexpTokenizer(r'[\w\'\-]+')#Remove certain types of characters

# Read the CSV file into a DataFrame
file_path = "chatgpt_responses.csv"
df = pd.read_csv(file_path)

# Function to extract row i from variables Chat_GPT_Ans_1 till Chat_GPT_Ans_100
def extract_answers_row(df, row_index):#The row index determines the temperature from chatgpt
	# Generate the column names from Chat_GPT_Ans_1 to Chat_GPT_Ans_100
	columns = [f"Chat_GPT_Ans_{i}" for i in range(1, 101)]

	# Ensure the DataFrame has these columns
	existing_columns = [col for col in columns if col in df.columns]

	# Extract the specified row for the existing columns
	if row_index < len(df):
		extracted_row = df.loc[row_index, existing_columns].tolist()
		return extracted_row
	else:
		raise IndexError("Row index out of range")
reviews=extract_answers_row(df, 0)#corresponds to all the answers given by chatgpt




#==============
WBW=[]#word by word
for i in range(0,len(reviews)):
	WBW.append(tokenizer.tokenize(reviews[i]))



shingle_size=4#Size of Shingles
def create_shingles(wbw,n):
	shingle=[]#Shingles from a review
	for j in range(0,len(wbw)-n-1):
		shingle.append(''.join(wbw[j:j+n]))#Shingles from each review 
	return(shingle)



shingles=[]
for i in range(0,len(WBW)):
	shingles.append(create_shingles(WBW[i],shingle_size))#Shingles from all reviews


#==This hashing process speeds up computation:==
A=[]
n=len(reviews)#np.shape(shingles)[0]#number of reviews
l=np.zeros( n )#matrix to store estimated Jaccard similarity
for i in range(0, n):
	mi = MinHash(num_perm=200)
	for d in shingles[i]: 
		mi.update(d.encode('utf8'))
	A.append(mi)




def jaccard_similarity(text):
	#==hashing the answer from each participant====
	word_by_word=tokenizer.tokenize(text)
	answer_shingle=create_shingles(word_by_word,shingle_size)
	
	hashed_shingles = MinHash(num_perm=200)
	for d in answer_shingle: 
		hashed_shingles.update(d.encode('utf8'))
	#===================================
	print('hashed_shingles',hashed_shingles)

	#Computing the estimated Jacarta similarity:
	JS=np.zeros(n)
	for j in range(0,n):
		JS[j]=hashed_shingles.jaccard(A[j])#matrix with estimated Jaccard similarity (it is symmetric)
	max_jaccard_similarity=np.amax(JS,axis=0)#print(l.max(axis=0)) #maximum similarity: latent variable to measure whether a review has been copied or not    
	#print("--- %s seconds ---" % (time.time() - start_time))
	return(max_jaccard_similarity)


#=====example (delete later)======
# text='Antes de la política de cuotas la educación universitaria pública de alta calidad se consideraba algo privilegiado y al alcance de solo aquellos alumnos que habían tenido una educación privada, lo que contribuía a mantener una percepción elitista de la educación superior. La política de cuotas permite que un gran número de alumnos de escuelas públicas y de minorías accedan a una educación superior de prestigio. Esto ayuda a que los entrevistadores tengan candidatos de muchos colegios diferentes pero con la misma educación universitaria aplicando al mismo puesto de trabajo. A medida que estos estudiantes, de diferentes contextos, se gradúan y entran al mercado laboral, los empleadores se encuentran con un grupo más diverso de candidatos bien calificados, lo que debería disminuir fuertemente la discriminación contra estos grupos en el proceso de contratación. Gracias a esta política ya no se puede contratar a alguien de un colegio privado y saber que su desempeño será mejor que un alumno de un colegio público ya que ambos pueden haber asistido a la misma universidad y por lo tanto, tuvieron la misma educación superior, la que los hace igual de calificados para este trabajo. Además, desde el punto de vista de los graduados pertenecientes a los grupos discriminados, esta política aumenta sus posibilidades de estudiar en mejores universidades públicas, lo que abre sus fronteras de empleos y da la oportunidad de que ellos participen en mercados laborales que antes estaban reservados para alumnos que habían tenido una educación escolar privada y universitaria buena. Esta forma también muestra como disminuirá la discriminación contra los negros y los pueblos indígenas en el proceso de contratación.'
# print("Max Jaccard Similarity:", jaccard_similarity(text))


# Read the CSV file into a DataFrame
file_path = "path_to/combined_data.csv"
combined_df = pd.read_csv(file_path)

vector_jaccard_similarity=np.zeros(len(combined_df['lista']))
for i in range(len(combined_df['lista'])):
	text=combined_df['answer_1_c'][i]
	vector_jaccard_similarity[i]=jaccard_similarity(text)

combined_df['jaccard_similarity']=100*vector_jaccard_similarity

# Save the DataFrame to a new CSV file
combined_df.to_csv('combined_data_with_jaccard_similarity.csv', index=False)

