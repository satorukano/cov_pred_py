import json

from module.identify_execute_block import IdentifyExecuteBlock
from db.database import Database

def main():
    db = Database()
    json_open = open("block_range.json", 'r')
    block_range = json.load(json_open)
    trace_ids = db.get_trace_ids(1)
    ans_id = 1
    ans_ieb = IdentifyExecuteBlock(block_range, db, ans_id)
    ans_labels = {}
    ans_vector = ans_ieb.create_vector()
    executed_block = ans_ieb.get_executed_block()
    ans_labels[ans_id] = ans_vector
    for trace_id in trace_ids:
        if trace_id[0] == ans_id:
            continue
        ieb = IdentifyExecuteBlock(block_range, db, trace_id[0])
        ans_labels[trace_id] = ieb.create_vector_with_executed_block(executed_block)
    print(ans_labels)

main()