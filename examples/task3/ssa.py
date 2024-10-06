import sys
import json
import cfg
from form_blocks import form_blocks
from collections import defaultdict

def intersect(sets):
    sets = list(sets)
    if not sets:
        return set()
    out = set(sets[0])
    for s in sets[1:]:
        out &= s
    return out

def compute_dominators(blocks):
    pred, succ = cfg.edges(blocks)

    dom = {v: set(blocks) for v in succ}

    changed = True
    while changed:

        changed = False

        for blk in blocks:

            # TODO: Optimize by reverse postorder
            # intersection
            dom_set = intersect(dom[p] for p in pred[blk])
            dom_set.add(blk)

            if dom[blk] != dom_set:
                dom[blk] = dom_set
                changed = True

    return dom

def compute_dominance_frontiers(dom, blocks):
    _, succ = cfg.edges(blocks)

    dom_inv = {key: [] for key in dom}
    for p, ss in dom.items():
        for s in ss:
            dom_inv[s].append(p)


    frontiers = {}
    for block in dom:
        # Find all successors of dominated blocks.
        dominated_succs = set()
        for dominated in dom_inv[block]:
            dominated_succs.update(succ[dominated])

        # You're in the frontier if you're not strictly dominated by the
        # current block.
        frontiers[block] = [b for b in dominated_succs
                                if b not in dom_inv[block] or b == block]

    return frontiers
    
def def_blocks(blocks):
    m = defaultdict(set)
    for name, block in blocks.items():
        for instr in block:
            if 'dest' in instr:
                m[instr['dest']].add(name)
    return dict(m)


def place_phis(blocks):
    dom = compute_dominators(blocks)
    dominance_frontiers = compute_dominance_frontiers(dom, blocks)
    
    # defs[v] = set of blocks that define variable v
    defs = def_blocks(blocks)

    phis = {b: set() for b in blocks}
    for v, v_def_blks in defs.items():
        v_def_blks_list = list(v_def_blks)
        for defining_block in v_def_blks_list:
            for block in dominance_frontiers[defining_block]:
                # Add a phi-node if not already there
                if v not in phis[block]:
                    phis[block].add(v)
                    if block not in v_def_blks_list:
                        v_def_blks_list.append(block)
    return phis, dom

def dom_tree(dom):
    # Get the blocks strictly dominated by a block strictly dominated by
    # a given block.
    dom_inv = {key: [] for key in dom}
    for p, ss in dom.items():
        for s in ss:
            dom_inv[s].append(p)

    dom_inv_strict = {a: {b for b in bs if b != a}
                      for a, bs in dom_inv.items()}
    dom_inv_strict_2x = {a: set().union(*(dom_inv_strict[b] for b in bs))
                         for a, bs in dom_inv_strict.items()}
    return {
        a: {b for b in bs if b not in dom_inv_strict_2x[a]}
        for a, bs in dom_inv_strict.items()
    }

def ssa_rename(blocks, phis, domtree, args):
    
    _, succ = cfg.edges(blocks)

    # stack of names for each variable (dict maps var names to stack of SSA names, first is most recent name)
    stack = defaultdict(list, {v: [v] for v in args})
    phi_args = {b: {p: [] for p in phis[b]} for b in blocks}
    phi_dests = {b: {p: None for p in phis[b]} for b in blocks}
    counters = defaultdict(int)

    def _new_fresh(var):
        fresh = '{}.{}'.format(var, counters[var])
        counters[var] += 1
        return fresh

    def _rename(block):
        # remember the stack
        old_stack = {k: list(v) for k, v in stack.items()}

        # Rename phi-node destinations.
        for p in phis[block]:
            fresh = _new_fresh(p)
            stack[p].insert(0, fresh)
            phi_dests[block][p] = fresh

        for instr in blocks[block]:
            if 'args' in instr:
                instr['args'] = [stack[arg][0] for arg in instr['args']]
            if 'dest' in instr:
                fresh =_new_fresh(instr['dest'])
                stack[instr['dest']].insert(0, fresh)
                instr['dest'] = fresh

        # Rename phi-node arguments (in successors).
        for s in succ[block]:
            for p in phis[s]:
                if stack[p]:
                    phi_args[s][p].append((block, stack[p][0]))
                else:
                    # The variable is not var_defined on this path
                    phi_args[s][p].append((block, "__undefined"))

        for child in sorted(domtree[block]):
            _rename(child)

        # restore the stack
        stack.clear()
        stack.update(old_stack)

    entry = list(blocks.keys())[0]
    _rename(entry)

    return phi_args, phi_dests

def fill_phis(blocks, phi_args, phi_dests, types):
    for block, instrs in blocks.items():
        for dest, pairs in sorted(phi_args[block].items()):
            phi = {
                'op': 'phi',
                'dest': phi_dests[block][dest],
                'type': types[dest],
                'labels': [p[0] for p in pairs],
                'args': [p[1] for p in pairs],
            }
            instrs.insert(0, phi)

def get_types(func):
    types = {arg['name']: arg['type'] for arg in func.get('args', [])}
    for instr in func['instrs']:
        if 'dest' in instr:
            types[instr['dest']] = instr['type']
    return types

def to_ssa(fn):
    # Construct CFG
    blocks = cfg.block_map(form_blocks(fn['instrs']))
    cfg.add_entry(blocks)
    cfg.add_terminators(blocks)

    phis, dom = place_phis(blocks)

    original_types = get_types(fn)
    func_args = {arg['name'] for arg in fn['args']} if 'args' in fn else set()
    phi_args, phi_dests = ssa_rename(blocks, phis, dom_tree(dom), func_args)
    fill_phis(blocks, phi_args, phi_dests, original_types)

    fn['instrs'] = cfg.reassemble(blocks)

def from_ssa(func):
    # Construct CFG
    blocks = cfg.block_map(form_blocks(func['instrs']))
    cfg.add_entry(blocks)
    cfg.add_terminators(blocks)

    # Remove all phi functions
    for block in blocks.values():
        for instr in block:
            if instr.get('op') == 'phi':
                dest = instr['dest']
                type = instr['type']
                for i, label in enumerate(instr['labels']):
                    var = instr['args'][i]

                    if var != "__undefined":
                        # Insert a copy instruction at each of the arguments of the phi function
                        pred = blocks[label]
                        pred.insert(-1, {
                            'op': 'id',
                            'type': type,
                            'args': [var],
                            'dest': dest,
                        })

        # Remove all phis
        new_block = [i for i in block if i.get('op') != 'phi']
        block[:] = new_block

    func['instrs'] = cfg.reassemble(blocks)

def is_ssa(prog):
    for func in prog['functions']:
        var_defined = set()
        for instr in func['instrs']:
            if 'dest' in instr:
                if instr['dest'] in var_defined:
                    return False
                else:
                    var_defined.add(instr['dest'])
    return True


if __name__ == "__main__":
    prog = json.load(sys.stdin)
    
    for fn in prog["functions"]:
        to_ssa(fn)

    assert(is_ssa(prog))

    for fn in prog["functions"]:
        from_ssa(fn)
    
    json.dump(prog, sys.stdout, indent=2)
    
