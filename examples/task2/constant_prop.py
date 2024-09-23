import sys
import json
import cfg
from form_blocks import form_blocks

not_const = "not_const"

# in/out dict is map of {var_name, const_val/not_const}

FOLDABLE_OPS = {
    'add': lambda a, b: a + b,
    'mul': lambda a, b: a * b,
    'sub': lambda a, b: a - b,
    'div': lambda a, b: a // b,
    'gt': lambda a, b: a > b,
    'lt': lambda a, b: a < b,
    'ge': lambda a, b: a >= b,
    'le': lambda a, b: a <= b,
    'ne': lambda a, b: a != b,
    'eq': lambda a, b: a == b,
    'or': lambda a, b: a or b,
    'and': lambda a, b: a and b,
    'not': lambda a: not a
}

def can_fold(instr, constant_dict):
    if 'op' not in instr or 'args' not in instr:
        return False
    
    op = instr['op']
    argvars = instr.get('args', [])
    
    if op not in FOLDABLE_OPS:
        return False
    
    for var in argvars:
        if var not in constant_dict or constant_dict[var] == not_const:
            return False
    
    return True

def fold_constant(instr, constant_dict):
    op = instr['op']
    argvars = instr.get('args', [])
    if op in FOLDABLE_OPS:
        const_args = [constant_dict[var] for var in argvars]
        const_val = FOLDABLE_OPS[op](*const_args)
        instr.update({
            'op': 'const',
            'value': const_val,
        })
        del instr['args']
        return const_val
    else:
        return not_const

def propagate_constant_in_blk(block, in_dict):
    out_dict = in_dict.copy()
    for instr in block:
        if 'dest' in instr:
            dest = instr['dest']
            if instr['op'] == 'const':
                out_dict[dest] = instr['value']
            elif instr['op'] == 'id':
                out_dict[dest] = out_dict.get(instr['args'][0], not_const)
                if out_dict[dest] != not_const:
                    instr.update({
                        'op': 'const',
                        'value': out_dict[dest],
                    })
                    del instr['args']
            elif can_fold(instr, out_dict):
                out_dict[dest] = fold_constant(instr, out_dict)
            else:
                out_dict[dest] = not_const

    out_dict_filtered = {key: value for key, value in out_dict.items() if value != not_const}
    return out_dict_filtered


def constant_propagation(fn):
    # Construct CFG
    blocks = cfg.block_map(form_blocks(fn['instrs']))
    cfg.add_terminators(blocks)

    pred, succ = cfg.edges(blocks)

    # Forward analysis
    in_ = {list(blocks.keys())[0]: {}}
    out = {blk: {} for blk in blocks}

    worklist = list(blocks.keys())
    while worklist:
        blk = worklist.pop(0)

        in_set = set()
        for p in pred[blk]:
            # intersection
            in_set &= (out[p]).items()
        
        in_[blk] = dict(in_set)

        out_dict = propagate_constant_in_blk(blocks[blk], in_[blk])

        if out_dict != out[blk]:
            out[blk] = out_dict
            worklist += succ[blk]

if __name__ == "__main__":
    prog = json.load(sys.stdin)
    for fn in prog["functions"]:
        constant_propagation(fn)
    json.dump(prog, sys.stdout, indent=2)