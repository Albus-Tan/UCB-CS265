
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

    preds, succs = cfg.edges(blocks)

    # Backwards analysis
    in_ = {list(blocks.keys())[-1]: set()}
    out = {blk: set() for blk in blocks}

    worklist = list(blocks.keys())
    while worklist:
        blk = worklist.pop(0)

        inval = set()
        for n in succs[blk]:
            inval |= out[n]
        
        in_[blk] = inval

        predefined, generated = get_predefs_and_defs(blocks[blk])
        outval = predefined.union(inval - generated)

        if outval != out[blk]:
            out[blk] = outval
            worklist += preds[blk]

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