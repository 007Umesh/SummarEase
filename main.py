from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

# # Load tokenizer and model
model_dir = "C:/Users/Umesh S/Desktop/TS-react/SummarEase/backend/model/pegasus-samsum-model"
token_dir ="C:/Users/Umesh S/Desktop/TS-react/SummarEase/backend/model/tokenizer"


# class Pegasus_samsum:
#     def __init__(self, model_dir,token_dir):
#         self.tokenizer = PegasusTokenizer.from_pretrained(token_dir)
#         self.model = PegasusForConditionalGeneration.from_pretrained(model_dir)
    

#     def summarize(self,text,length=80):
#         length=max(80,min(512,length))
#         inputs = self.tokenizer(text, max_length=length, truncation=True, return_tensors="pt")
#         summary_ids = self.model.generate(inputs.input_ids, num_beams=4, max_length=length,length_penalty=2.0,min_length=50, early_stopping=True)
#         summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#         return summary.replace("<n>"," ")
class Pegasus_samsum:
    def __init__(self, model_dir, token_dir):
        self.tokenizer = PegasusTokenizer.from_pretrained(token_dir)
        self.model = PegasusForConditionalGeneration.from_pretrained(model_dir)
    
    def summarize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        input_length = inputs.input_ids.shape[1]
        
        # Set summary length constraints based on input length
        if input_length <= 150:
            max_length = None  # Let the model decide
            min_length = 0
        elif 151 <= input_length <= 300:
            max_length = 120
            min_length = 75
        elif 301 <= input_length <= 512:
            max_length = 180
            min_length = 150
        else:
            max_length = 512
            min_length = 150

        # Generate summary
        summary_ids = self.model.generate(
            inputs.input_ids,
            num_beams=8,
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            early_stopping=True
        )
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary.replace("<n>", " ")
