from sklearn.model_selection import train_test_split
import torch
import numpy as np
from sklearn.metrics import precision_score, recall_score

class Trainer:
    def __init__(self, classifier, data, optimizer, criterion):
        self.classifier = classifier
        self.data = data
        self.optimizer = optimizer
        self.criterion = criterion

    
    def format_data(self):
        formatted_data = []
        for signature, vectorized_log in self.data.logs.items():
            labels = self.data.labels[signature]
            formatted_data.append((vectorized_log, labels))
        return formatted_data
    
    def train(self):
        print("Start training")
        formatted_data = self.format_data()
        train_data, val_data = train_test_split(formatted_data, test_size=0.2)
        for epoch in range(3):
            self.classifier.train()
            total_train_loss = 0.0
            for vectorized_log, labels in train_data:
                self.optimizer.zero_grad()
                logits = self.classifier(vectorized_log)
                labels = torch.tensor(labels)
                loss = self.criterion(logits, labels)
                loss.backward()
                self.optimizer.step()
                total_train_loss += loss.item()

            avg_train_loss = total_train_loss / len(train_data)

            # Validation
            self.classifier.eval()
            total_val_loss = 0.0
            all_true_labels = []
            all_pred_labels = []
            with torch.no_grad():
                for vectorized_log, labels in val_data:
                    logits = self.classifier(vectorized_log)
                    labels = torch.tensor(labels)
                    loss = self.criterion(logits, labels)
                    total_val_loss += loss.item()
                    all_true_labels.extend(labels)
                    all_pred_labels.extend(logits.argmax(dim=1))
            
            avg_val_loss = total_val_loss / len(val_data) if len(val_data) > 0 else 0.0
            all_true_labels = np.array(all_true_labels)
            all_pred_labels = np.array(all_pred_labels)
            precision = precision_score(all_true_labels, all_pred_labels, average='macro', zero_division=0)
            recall = recall_score(all_true_labels, all_pred_labels, average='macro', zero_division=0)
            
            print(f"Epoch {epoch+1}, Train Loss: {avg_train_loss:.4f}, Val Loss: {avg_val_loss:.4f}, "
                f"Precision: {precision:.4f}, Recall: {recall:.4f}")


