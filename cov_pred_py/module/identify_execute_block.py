import json
import pickle
from collections import OrderedDict
from sortedcontainers import SortedSet

class IdentifyExecuteBlock:

    def __init__(self, block_range, database, signature):
        self.block_range = block_range  
        self.execution_path = database.get_execution_trace(signature)
        self.signature = signature
        self.executed_block = None
    
    def get_executed_block(self):
        return self.executed_block
    
    def create_vector(self):
        self.identify_execute_block()
        vector = [item for key in self.executed_block for item in self.executed_block[key]]
        return vector
    
    def create_vector_with_executed_block(self, another_executed_block):
        self.identify_execute_block()
        ans_executed_block = {}
        for path, executed_block in another_executed_block.items():
            if path in self.executed_block.keys():
                ans_executed_block[path] = executed_block
            else:
                ans_executed_block[path] = [0] * len(executed_block)
        vector = [item for key in ans_executed_block for item in ans_executed_block[key]]
        return vector


    def identify_execute_block(self):
        executed_line = self.identify_execute_line()
        executed_block = {}
        for method_id in executed_line.keys():
            file_name = method_id.split(":")[0]
            method_name = method_id.split(":")[-1]
            executed_block[method_id] = []
            
            if file_name not in self.block_range.keys():
                continue
            elif method_name not in self.block_range[file_name] :
                continue

            if self.block_range[file_name][method_name] == []:
                continue

            for block in self.block_range[file_name][method_name]:
                exec_flag = False
                block_start = block[0]
                block_end = block[1]
                for line in executed_line[method_id]:
                    if block_start < int(line) < block_end:
                        executed_block[method_id].append(1)
                        exec_flag = True
                        break
                if exec_flag:
                    continue
                else:
                    executed_block[method_id].append(0)
        self.executed_block = OrderedDict(executed_block)


    def identify_execute_line(self):
        executed_line = {}
        
        for line in self.execution_path:
            if (not "src/test" in line[1]):
                executed = line[1]
                file_name = executed.split(";")[0]
                class_name = executed.split(";")[1].split('#')[0].split('.')[-2]
                method_name = executed.split(";")[1].split('#')[0].split('.')[-1]
                line_number = executed.split('@')[-1]
                if method_name == "<init>":
                    method_name = class_name
                
                method_id = file_name + ":" + class_name + ":" + method_name

                if method_id in executed_line.keys():
                    executed_line[method_id].add(line_number)
                else:
                    executed_line[method_id] = SortedSet([line_number])
        
        return executed_line
