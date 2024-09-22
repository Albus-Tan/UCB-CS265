
import sys
import json
import cfg
from form_blocks import form_blocks

def get_predefs_and_defs(block):
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

    return read, written


def liveness_analysis(fn):
    # Construct CFG
    blocks = cfg.block_map(form_blocks(fn['instrs']))
    cfg.add_terminators(blocks)

    succ, pred = cfg.edges(blocks)

    # Backwards analysis
    in_ = {list(blocks.keys())[-1]: set()}
    out = {blk: set() for blk in blocks}

    worklist = list(blocks.keys())
    while worklist:
        blk = worklist.pop(0)

        in_set = set()
        for p in pred[blk]:
            in_set |= out[p]
        
        in_[blk] = in_set

        predefined, generated = get_predefs_and_defs(blocks[blk])
        out_set = predefined.union(in_set - generated)

        if out_set != out[blk]:
            out[blk] = out_set
            worklist += succ[blk]

    return blocks, in_


def global_dead_code_elimination(cfg_blks, live):
    for name, block in cfg_blks.items():
        live_set = live[name]
        new_block = []
        for instr in reversed(block):

            dest = instr.get('dest')
            if dest and (dest not in live_set):
                # remove this instruction
                pass
            else:
                new_block.append(instr)
            
            live_set.update(instr.get('args', []))

        if len(new_block) != len(block):
            block[:] = reversed(new_block)

if __name__ == "__main__":
    prog = json.load(sys.stdin)
    for fn in prog["functions"]:
        cfg_blks, live = liveness_analysis(fn)
        global_dead_code_elimination(cfg_blks, live)
        fn['instrs'] = cfg.reassemble(cfg_blks)
    json.dump(prog, sys.stdout, indent=2)