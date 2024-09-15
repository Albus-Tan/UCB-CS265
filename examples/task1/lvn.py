
import sys
import json
import copy
from typing import Tuple, Dict, List
from form_blocks import form_blocks, flatten

# Value/Expression class used in LVN table
class Value:

    def __init__(self, op = None, args: List[int] = None):
        # if op is None, the Value is defined somewhere out side the block
        self.op = op
        # sequential storage of all op's parameters (use #id in LVN table)
        self.args = args

    # Judge whether two Value/Expression class are identically same
    def __eq__(self, other):
        if not isinstance(other, Value):
            raise ValueError(f"{type(other)} type cannot conduct equal operation (==) with {type(self)}!")
        
        if self.op is None or other.op is None:
            return False

        if self.op != other.op:
            return False

        # For operator satisfies the commutative law
        if self.op in ['add', 'mul']:
            # Both are binary op
            return (self.args[0] == other.args[0] and self.args[1] == other.args[1]) or (self.args[0] == other.args[1] and self.args[1] == other.args[0])
        else:
            return self.args == other.args
    
    # for debug
    def __str__(self):
        if self.op is None:
            return "(def in prev blk)"

        s = self.op
        argstr = ", ".join('#{}'.format(arg) for arg in self.args)
        return '{}({})'.format(s, argstr)

class LVNTable:
    def __init__(self, block):
        # List, LVN table that record (#id, Value/Expression, Var)
        self.num2var: Dict[int, Tuple[Value | None, str]] = {}
        self.next_id: int = 1

        # Dict, key var name, value #id
        self.var2num: Dict[str, int] = {}

        self._init_table(block)

    def _init_table(self, block):

        # Get all predefined vars (function args, or defined in previous blocks)
        read = set()
        written = set()

        for instr in block:
            args = instr.get('args', [])
            for arg in args:
                if arg not in written:
                    read.add(arg)
            
            dest = instr.get('dest')
            if dest is not None:
                written.add(dest)

        for var in read:
            id = self._add_val_in_num2var(Value(),var)
            self.var2num[var] = id
        
    def lookup_var_in_num2var(self, id : int):
        if id in self.num2var:
            return self.num2var[id][1]
        return None

    def _lookup_val_in_num2var(self, target_value : Value):
        for key, (val, var) in self.num2var.items():
            if val == target_value:
                # print(f"eq {val}, {target_value}")
                return key, var
        return None, None
    
    def _add_val_in_num2var(self, value: Value, var: str):
        id = self.next_id
        self.num2var[id] = (value, var)
        self.next_id += 1
        return id
        
    def lookup_var_id_in_var2num(self, var: str):
        return self.var2num.get(var, None)

    def add_instruction(self, instr):
        
        # ignore instruction not having dest, since it does not produce new value
        if not instr.get('dest'):
            return
        
        if instr["op"] == 'id':
            if self.lookup_var_id_in_var2num(instr.get("args")[0]):
                self.var2num[instr.get('dest')] = self.var2num[instr.get("args")[0]]
            return

        # canonicalize the instruction's arguments by getting the 
        # value numbers currently held by those vars
        args = []
        if instr["op"] == 'const':
            args.append(instr.get("value"))
        else:
            for arg in instr.get('args', []):
                id = self.lookup_var_id_in_var2num(arg)
                if id is not None:
                    args.append(id)
                else:
                    raise RuntimeError(f"var {arg} not defined before")

        # create a new value by packaging this instruction with 
        # the value numbers of its arguments
        value = Value(instr["op"], args)

        # look up the value number of this value
        num, var = self._lookup_val_in_num2var(value)

        if num is None:
            # we've never seen this value before
            num = self._add_val_in_num2var(value, instr.get('dest'))

            # if instr will be overwritten later:
            #     dest = fresh variable name
            #     instr.dest = dest
            # else:
            #     dest = instr.dest

            for arg_pos, arg in enumerate(instr.get('args', [])):
                id = self.lookup_var_id_in_var2num(arg)
                if id is not None:
                    src_arg = self.lookup_var_in_num2var(id)
                    # replace arg with table[var2num[a]].var
                    instr["args"][arg_pos] = src_arg
        else:
            instr.update({
                'op': 'id',
                'args': [var],
            })

        self.var2num[instr.get('dest')] = num

def lvn(function):
    blocks = list(form_blocks(function['instrs']))
    for block in blocks:
        lvn_table = LVNTable(block)
        for instr in block:
            lvn_table.add_instruction(instr)
    function['instrs'] = flatten(blocks)

if __name__ == '__main__':
    prog = json.load(sys.stdin)
    for fn in prog["functions"]:
        lvn(fn)
    json.dump(prog, sys.stdout, indent=2)