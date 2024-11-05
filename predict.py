from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

# Load tokenizer and model
model_dir = "C:/Users/Umesh S/Desktop/TS-react/SummarEase/backend/model/pegasus-samsum-model"
token_dir ="C:/Users/Umesh S/Desktop/TS-react/SummarEase/backend/model/tokenizer"
tokenizer = PegasusTokenizer.from_pretrained(token_dir)
model = PegasusForConditionalGeneration.from_pretrained(model_dir)

# Sample text to summarize
text = """
summarEase is a novel web-based tool that employs cutting-edge natural language processing (NLP) techniques to ease the text summary process. The primary goal of this project is to provide a user-friendly platform that allows users to enter text, either directly or by uploading text files, and then obtain short, logical summaries created by a fine-tuned Pegasus model. This model, known for its abstractive summarizing skills, has been fine-tuned using the SAMSum dataset to excel at conversation summarization tasks. SummarEase's principal goal is to give meeting summaries or dialogue conversation summaries for clients in an online support center for corporate usage. By concentrating on dialogue summary, the program meets the unique demands of enterprises looking to expedite communication and improve client relations. SummarEase also provides conventional summarizing for common users, making it a useful tool for a variety of text summary applications. The Pegasus model has been fine-tuned using the SAMSum dataset, a vast collection of conversations with matching summaries, to guarantee that it is particularly effective at summarizing conversational material. This fine-tuning procedure improves the model's capacity to extract the substance of dialogues and create accurate and coherent summaries. Users benefit from the model's excellent capacity to extract the most important information from lengthy conversations and condense it into concise summaries, enhancing productivity and understanding.
The program seamlessly integrates a Flask-based backend and a dynamic frontend built using HTML, CSS, and JavaScript. The frontend interface is intended to be user-friendly, with a simple slider allowing users to enter their content and alter the length of the summary accordingly. JavaScript manages the interactions, guaranteeing a pleasant user experience through asynchronous connection with the backend via AJAX requests. This enables real-time text processing without requiring page reloads, hence increasing user engagement and happiness. On the backend, the Flask framework is used to process requests and provide web pages. 




"""

# Tokenize the input text
inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")

# Generate the summary
summary_ids = model.generate(inputs.input_ids, num_beams=4, max_length=1024,min_length=100,length_penalty=2.0, early_stopping=True)

# Decode the summary
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

clean_summary = summary.replace("<n>", " ")

# Print the summary
print("Summary:", summary)



