import json
import pickle
import torch
import torch.nn as nn
import torch.optim as optim

from module.identify_execute_block import IdentifyExecuteBlock
from db.database import Database
from module.vectorize_log import VectorizeLog
from module.Trainer import Trainer
from module.dnn_classifier import DNNClassifier

def main():
    print("start processing data.....")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("device:", device)
    db = Database()
    signatures = db.get_signatures(1)
    json_open = open("block_range.json", 'r')
    block_range = json.load(json_open)
    ans_signature = signatures[0][0]
    vectorizer = VectorizeLog(device)
    ans_ieb = IdentifyExecuteBlock(block_range, db, ans_signature)
    ans_labels = {}
    ans_labels[ans_signature] = ans_ieb.create_vector()
    labels_dim = len(ans_labels[ans_signature])
    logs = db.get_log(ans_signature, 1)
    vectorizer = VectorizeLog()
    target_vector = vectorizer.vectorize(logs)
    vectors = {}
    vectors[ans_signature] = target_vector

    ans_vector = ans_ieb.create_vector()
    executed_block = ans_ieb.get_executed_block()
    ans_labels[ans_signature] = ans_vector
    for signature in signatures:
        if signature[0] == ans_signature:
            continue
        ieb = IdentifyExecuteBlock(block_range, db, signature[0])
        ans_labels[signature] = ieb.create_vector_with_executed_block(executed_block)
        logs = db.get_log(signature[0], 1)
        vectorized_logs = vectorizer.vectorize(logs)
        vectors[signature] = vectorized_logs
    data = {}
    data.logs = vectors
    data.labels = ans_labels

    print("finish processing data.....")

    classifier = DNNClassifier(768, 512, labels_dim)
    classifier.to(device)
    criterion = nn.BCEWithLogitsLoss()  # 多ラベル分類用の損失関数
    optimizer = optim.Adam(classifier.parameters(), lr=2e-5)

    trainer = Trainer(classifier, data, optimizer, criterion)
    trainer.train() 

main()