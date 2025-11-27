#===python Key====
#       a secret key is required to use chatGPT API
#=================


#you need to run "source myenv/bin/activate" each time you open python

#===Written by Gustavo Q. Saraiva on 22/07/2024==



from openai import OpenAI
import logging#to save the logs
from datetime import datetime#to save the time the requests were made
from time import sleep
import csv
import os

# Function to get the current time
def get_current_time():
	return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#=====Parameters of the requests===========
numb_obs=100#how many requests to make
prompt = "Many in Chile complain that job interviewers often ask candidates which high school they attended and are more inclined to hire wealthy candidates who studied in expensive prestigious private high schools. This frustration is understandable, as the high school a student attended should not, in principle, be a relevant signal to be considered by interviewers. Instead, the interviewer should be more focused on the quality of the higher education degree obtained by the candidate. Based on the results obtained in the previous items, how do you think the quota policy implemented in Brazilian public universities might affect this type of elitist behavior from Brazilian employers? How do you think this could impact discrimination against black and indigenous minorities in the hiring process? Explain."#"En Chile se reclama mucho que, en el las entrevistas de trabajo se pregunta a los candidatos en que colegio han estudiado y que suele darse mayor prioridad a los alumnos ricos que han estudiado en escuelas particulares caras y de prestigio. Tal frustración es comprehensible, ya que el colegio en que un alumno ha estudiado no debería, en principio, ser una señal relevante a ser considerada por el entrevistador, y sí la calidad de la educación superior obtenida por el candidato. Basado en los resultados obtenidos en los ítems anteriores, ¿cómo crees que la política de cuotas en las universidades públicas Brasileñas podría afectar este tipo de comportamiento elitista por parte de los empleadores en Brasil? ¿Cómo crees que esto podría afectar la discriminación contra los negros y los pueblos indígenas en el proceso de contratación? Explique."
temp = 1.0#0.0 is the lowest temperature, 1.0 is the default, and 2.0 is the maximum temperature.
chat_gpt_version = "gpt-3.5-turbo"#this is probably the most affordable version of chatgpt (it is free), which is why I am using this version.
csv_file_path = 'chatgpt_responses.csv'
max_t=400#maximum number of tokens (controls how large or small the responses are)
#as 98% of my observations had less than 400 tokens, with an average of 250 tokens, I set the maximum at 400 tokens.
#==========================================



#======Function to log the request and response to a CSV file=====
# def log_to_csv(file_path, data):
#     file_exists = os.path.isfile(file_path)
#     
#     with open(file_path, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         if not file_exists:
#             # Write the header if the file does not exist
#             headers=["Prompt", "Temperature", "Chat_Gpt_Version", "current_time", ]+[f"Chat_GPT_Ans_{i+1}" for i in range(numb_obs)]
#             writer.writerow(headers)
#         writer.writerow(data)
#=================================================================
def log_to_csv(data, file_prefix="saving_chatgpt_responses_english"):
	current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
	file_path = f"{file_prefix}_{current_time}.csv"
	with open(file_path, mode='w', newline='') as file:
		writer = csv.writer(file)
		headers = ["Prompt", "Temperature", "Chat_Gpt_Version", "current_time"] + [f"Chat_GPT_Ans_{i+1}" for i in range(numb_obs)]
		writer.writerow(headers)
		writer.writerow(data)
#=================================================================






#===This sets up logging to write to a file named api_requests.log:
logging.basicConfig(filename='api_requests.log', level=logging.INFO)



answers=[]
for i in range(numb_obs):
	client = OpenAI(
			api_key="insert_secret_key_here",
	)
	
	stream = client.chat.completions.create(
		model=chat_gpt_version,
		messages=[{"role": "user", "content": prompt}],
		stream=True,
		temperature=temp,#set to 0 to generate more consistent results
		max_tokens=max_t#the maximum number of tokens from the answer
	)
	
	# Get the current time
	current_time = get_current_time()
	
	# Log the request
	logging.info(f"Request: model=chat_gpt_version, messages=[{{'role': 'user', 'content': prompt}}], stream=True, temperature=temp")
	
	
	response_content = ""
	for chunk in stream:
		if chunk.choices[0].delta.content is not None:
			content = chunk.choices[0].delta.content
			print(content, end="")
			response_content += content
	logging.info(f"Response: {response_content},Time: {current_time}")
	answers.append(response_content)#save all responses
	sleep(3)

#=====exporting data to csv format:====
current_time = get_current_time()#the precise time from each separate request can be found in the log file.
data=[prompt, temp, chat_gpt_version, current_time]+answers
log_to_csv(data)
#======================================
