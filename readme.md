ollama 

llama index

pathway


Huggin Face:
	Transformers
	Hub
	Datasets
	Pipeline

https://www.youtube.com/watch?v=QEaBAZQCtwE&ab_channel=AssemblyAI


tokenization

embeddings


Package manager
	pip
	Git
	
==================================================================================================


Med‐PaLM 2


 ChatDoctor (an open‐source Chatbotfor health care) was based on LLaMA and used 100,000 patient‐physician conversations to fine‐tune[28]; this model showed significant improvements inunderstanding patients' needs and providing accurate advice.

 https://www.chatdoctor.com/
 https://github.com/Kent0n-Li/ChatDoctor/tree/main



 Similarly, Baize‐health care [29] is another open‐source Chatbot for health care based on LLaMA,which has been fine‐tuned using MedQuAD data set[30] (including 46,867 medical dialogues) and per-formed well in multi‐turn conversations. These models will facilitate the further development of conversation models in health care.


 performance of PaLM in medical questions was optimized through instruction prompt tuning to develop Med‐PaLM [26] (ChatGPT‐like ChatBot forHealth care). Subsequent development at Google has resulted in the production of Med‐PaLM 2 [27], whichreportedly achieves state‐of‐the‐art performance inUnited States Medical Licensing Examinations(USMLE) questions, exceeding the performance ofChatGPT [20].

GatorTron:
ClinicalBERT was created based upon BERT and BioBERT architectures [14] and trained on the MIMIC‐III data set [24]. MIMIC‐III comprises demo graphics,vital signs, laboratory tests, procedures, medications,clinical notes, investigation reports, and mortality datacorresponding to over 40,000 critical care patients—arich source of domain‐specific information [24]. Clin-icalBERT attained superior performance to BERT andBioBERT across a range of medical NLP tasks, demon-strating the promise of using clinical corpora to fine‐tuneLLMs to optimize domain‐specific performance [14]. Inaddition, GatorTron, the largest clinical language modelavailable, was trained from scratch using over 90 billionwords of text from the deidentified clinical notes ofUniversity of Florida Health, PubMed articles andWikipedia [25]. This model increases the parametercount of LLMs within the clinical domain from 110million (ClinicalBERT) to 8.9 billion. It has achievedcompetitive performance across multiple downstreamclinical tasks, demonstrating the advantage of using large“Transformer” models.


===============

Run: 
	uvicorn app:app --host 0.0.0.0 --port 5963

==============
Https:

	uvicorn app:app --host 0.0.0.0 --port 8000 --ssl-keyfile="M:/SJ/AWS machine learning engineer/Project/SympAI-Medical-Chatbot/sympai-backend/cert/key.pem" --ssl-certfile="M:/SJ/AWS machine learning engineer/Project/SympAI-Medical-Chatbot/sympai-backend/cert/cert.pem"


======================
Docker
	Build:
		docker build -t sympai-api .   


	Run: 
		docker run -e AWS_ACCESS_KEY_ID=<your_aws_access_key> -e AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key> -e AWS_REGION=us-east-1 -p 8000:8000 sympai-api