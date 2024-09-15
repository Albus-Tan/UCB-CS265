import sys
import json
from form_blocks import form_blocks, flatten

def ldce(function):
    while True:
        changed = tdce(function)
        changed |= elimate_dead_store(function)
        if not changed:
            break

def is_pure(instr):
    return instr["op"] not in ["call", "print", "alloc"]

def tdce(function):
    blocks = list(form_blocks(function['instrs']))
    
    used_vars = set()
    for block in blocks:
        for instr in block:
            used_vars.update(instr.get('args', []))
    
    modified = False
    for block in blocks:
        new_block = []
        for instr in block:
            dest = instr.get('dest')
            if dest and (dest not in used_vars) and is_pure(instr):
                # remove this instruction
                continue
            new_block.append(instr)
        if len(new_block) != len(block):
            modified = True
            block[:] = new_block
    
    function['instrs'] = flatten(blocks)
    return modified

def elimate_dead_store(function):
    """Removes instructions whose results are overwritten before being used."""
    modified = False
    blocks = list(form_blocks(function['instrs']))
    for block in blocks:
        if elimate_dead_store_in_block(block):
            modified = True
    function['instrs'] = flatten(blocks)
    return modified

def elimate_dead_store_in_block(block):
    """Removes dead assignments within a block."""
    modified = False
    # {var: inst}
    unused = {}
    to_remove = set()
    
    for idx, instr in enumerate(block):
        # Remove variables from unused if they are used
        for arg in instr.get('args', []):
            if arg in unused:
                del unused[arg]
        
        # Check for definitions
        if 'dest' in instr:
            var = instr['dest']
            if var in unused:
                # Previous assignment is dead
                to_remove.add(unused[var])
            unused[var] = idx
    
    if to_remove:
        block[:] = [instr for idx, instr in enumerate(block) if idx not in to_remove]
        modified = True
    
    return modified

if __name__ == '__main__':
    prog = json.load(sys.stdin)
    for fn in prog["functions"]:
        ldce(fn)
    json.dump(prog, sys.stdout, indent=2)
