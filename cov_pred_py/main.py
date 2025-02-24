import json
import pickle

from module.identify_execute_block import IdentifyExecuteBlock
from db.database import Database

def main():
    db = Database()
    signatures = db.get_signatures(1)
    json_open = open("block_range.json", 'r')
    block_range = json.load(json_open)
    ans_signature = signatures[0][0]
    ans_ieb = IdentifyExecuteBlock(block_range, db, ans_signature)
    ans_labels = {}
    ans_vector = ans_ieb.create_vector()
    executed_block = ans_ieb.get_executed_block()
    ans_labels[ans_signature] = ans_vector
    for signature in signatures:
        if signature[0] == ans_signature:
            continue
        ieb = IdentifyExecuteBlock(block_range, db, signature[0])
        ans_labels[signature] = ieb.create_vector_with_executed_block(executed_block)
    path_file = 'labels.pkl'
    pickle.dump(ans_labels, open(path_file, 'wb'))

main()