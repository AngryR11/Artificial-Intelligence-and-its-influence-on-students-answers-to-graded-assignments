# Data and code used in "*Artificial Intelligence-and-its-influence-on-students-answers-to-graded-assignments*" by Gustavo Q. Saraiva

- The main file is *Regressions.R*, which runs the main regressions of the paper.

- The original datasets are:
  - *anonymized_data_1.csv*
  - *anonymized_data_2.csv*

- I removed students' names and anonymized their list number using a one-way hash function: their list number corresponds to the order in which they appear in the University platform (variable "list"), which is based on alphabetical order.

- I then merged these two datasets (each dataset corresponds to the data from one section) into the file:
  - *shuffled_combined_data.csv*

- The subfolder *Getting_data_from_ChatGPT* contains:
  1) The python algorithm used to collect samples of ChatGPT responses using ChatGPT's API (file Generate_Chat_GPT_responses.py). To get these requests, one must pay a subscription (the 5 dollars subscription is more than enough) and use a secrete key that can be created for the project.
  2) ChatGPT responses (file "chatgpt_responses.csv")
  3) A python code used to compute the Jaccard similarity index between students' responses and the ones from ChatGPT (file "Jaccard_Similarity.py"). This file uses the MiniHash function to speed up computation.
  4) The log file *api_requests.log* from the requests (only useful for audit purposes).

# Referencies

- When using this dataset, please cite the corresponding working paper "*Artificial Intelligence and its influence on students’ answers to graded assignments*" by Gustavo Q. Saraiva.
