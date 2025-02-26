import torch
from transformers import RobertaTokenizer, RobertaModel

class VectorizeLog:
    def __init__(self, device):
        self.tokenizer = RobertaTokenizer.from_pretrained('microsoft/codebert-base')
        self.model = RobertaModel.from_pretrained('microsoft/codebert-base')
        self.model.to(device)
        self.device = device

    def vectorize(self, logs):
        print("Vectorizing logs...")
        formatted_logs = self.format_logs(logs)
        joined_logs = " </s> ".join(formatted_logs)
        input_text = "<s> " + joined_logs + " </s>"
        inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        outputs = self.model(**inputs)
        last_hidden_state = outputs.last_hidden_state
        sequence_embedding = last_hidden_state[:, 0, :].detach()

        return sequence_embedding
        
    
    def format_logs(self, logs):
        formatted_logs = []
        for log in logs:
            formatted_logs.append(log[0])
        return formatted_logs