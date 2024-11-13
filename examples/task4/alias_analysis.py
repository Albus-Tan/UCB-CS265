import sys
import json
import cfg
from form_blocks import form_blocks
from functools import reduce

class MemLocation:
    def __init__(self, allocated_block_name: str, allocated_line_no : int):
        self.allocated_block_name = allocated_block_name
        self.allocated_line_no = allocated_line_no

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        if self.allocated_line_no != -1:
            return f"[MemLocation] block {self.allocated_block_name}, line {self.allocated_line_no}"
        else:
            return f"[MemLocation] all location"
    
    @classmethod
    def alloc(cls, blk_name: str, line_no: int):
        return cls(blk_name, line_no)

    @classmethod
    def all(cls):
        return cls("ALL_MEM_LOCATION", -1)
    
    def __eq__(self, other):
        if isinstance(other, MemLocation):
            return (self.allocated_line_no == other.allocated_line_no) and (self.allocated_block_name == other.allocated_block_name)
        return False

    def __hash__(self):
        return hash((self.allocated_line_no, self.allocated_block_name))


ALL_MEM_LOCATION = MemLocation.all()

class MemLocationSet(set):
    def __init__(self, *args):
        super().__init__(*args)

    def add(self, element):
        if isinstance(element, MemLocation):
            if element == ALL_MEM_LOCATION:
                super().clear()
                super().add(ALL_MEM_LOCATION)
            else:
                super().add(element)
        elif isinstance(element, MemLocationSet):
            new_set = self.__class__.union(self, element)
            super().clear()
            super().update(new_set)
        else:
            raise TypeError("Only MemLocation instances can be added to the set.")

    def insert(self, element):
        self.add(element)

    @classmethod
    def common_alias(cls, set1, set2):
        if not isinstance(set1, MemLocationSet) or not isinstance(set2, MemLocationSet):
            raise TypeError(f"Alias can only be performed between two MemLocationSet, currently {type(set1)} and {type(set2)}.")
        
        if ALL_MEM_LOCATION in set1 or ALL_MEM_LOCATION in set2:
            return True
        else:
            return not set1.isdisjoint(set2)

    @classmethod
    def union(cls, set1, set2):
        if not isinstance(set1, MemLocationSet) or not isinstance(set2, MemLocationSet):
            raise TypeError(f"Union can only be performed between two MemLocationSet, currently {type(set1)} and {type(set2)}.")

        result_set = MemLocationSet()

        # Check if AllMemLocation is in either set
        if ALL_MEM_LOCATION in set1 or ALL_MEM_LOCATION in set2:
            result_set.add(ALL_MEM_LOCATION)
        else:
            # Add all other MemLocation instances
            result_set.update(set1)
            result_set.update(set2)

        return result_set

def transfer(blk_name, block, in_dict):
    out_dict = in_dict.copy()
    for line_no, instr in enumerate(block, start=1):
        if 'dest' in instr:
            dest = instr['dest']
            
            def update_dest(location):
                s = out_dict.get(dest, MemLocationSet())
                s.add(location)
                out_dict[dest] = s

            if instr['op'] == 'alloc':
                new_loc = MemLocation.alloc(blk_name, line_no)
                update_dest(new_loc)
            elif instr['op'] == 'id' or instr['op'] == 'ptradd':
                loc = out_dict.get(instr['args'][0])
                if loc is not None:
                    update_dest(loc)
                # Skip if the key does not exist
            elif instr['op'] == 'load':
                update_dest(ALL_MEM_LOCATION)

    return out_dict

def union_mem_location_maps(pred, out):
    result = {}

    # Iterate over the keys in the first map
    for key in out:
        if key in pred:
            # If the key exists in both maps, perform union
            result[key] = MemLocationSet.union(out[key], pred[key])
        else:
            # If only in out, keep it
            result[key] = out[key]

    # Iterate over the keys in the second map that are not in the first
    for key in pred:
        if key not in out:
            # If only in pred, keep it
            result[key] = pred[key]

    return result

def alias_analysis(fn):
    # Construct CFG
    blocks = cfg.block_map(form_blocks(fn['instrs']))
    cfg.add_terminators(blocks)

    pred, succ = cfg.edges(blocks)

    # Forward analysis
    # Initialize all function arguments pointing to all memory locations
    init_dict = {}
    if 'args' in fn:
        for arg in fn['args']:
            init_set = MemLocationSet()
            init_set.add(ALL_MEM_LOCATION)
            init_dict[arg['name']] = init_set

    in_ = {list(blocks.keys())[0]: init_dict}
    out = {blk: {} for blk in blocks}

    worklist = list(blocks.keys())
    while worklist:
        blk = worklist.pop(0)

        unioned_map = reduce(union_mem_location_maps, (out[p] for p in pred[blk]), {})
        in_[blk] = union_mem_location_maps(in_.get(blk, {}), unioned_map)

        out_dict = transfer(blk, blocks[blk], in_[blk])

        if out_dict != out[blk]:
            out[blk] = out_dict
            worklist += succ[blk]

    return in_

def store_to_load_forwarding(alias_map, fn):
    # Construct CFG
    blocks = cfg.block_map(form_blocks(fn['instrs']))
    cfg.add_terminators(blocks)

    for blk_name in list(blocks.keys()):
        new_blk = []
        block_alias_map = alias_map[blk_name].copy()
        # record pointer name and (stored value, line number) of "store" instr may be forwarded
        store_may_forward = {}
        cur_blk = blocks[blk_name]
        for line_no, instr in enumerate(cur_blk, start=1):
            if 'dest' in instr:
                dest = instr['dest']
                
                def update_dest(location):
                    s = block_alias_map.get(dest, MemLocationSet())
                    s.add(location)
                    block_alias_map[dest] = s

                if instr['op'] == 'alloc':
                    new_loc = MemLocation.alloc(blk_name, line_no)
                    update_dest(new_loc)
                elif instr['op'] == 'id' or instr['op'] == 'ptradd':
                    loc = block_alias_map.get(instr['args'][0])
                    if loc is not None:
                        update_dest(loc)
                    # Skip if the key does not exist
                elif instr['op'] == 'load':
                    ptr_name = instr['args'][0]
                    loc = block_alias_map.get(ptr_name)
                    
                    # instruction between last store to ptr_name 
                    # to current load from ptr_name
                    # should not alias with ptr
                    if ptr_name in store_may_forward:
                        store_line_no = store_may_forward[ptr_name][1] + 1
                        while store_line_no < line_no:
                            cur_instr = cur_blk[store_line_no-1]
                            if 'op' in cur_instr:
                                if cur_instr['op'] == 'store' or cur_instr['op'] == 'load':
                                    if MemLocationSet.common_alias(block_alias_map[cur_instr['args'][0]], block_alias_map[ptr_name]):
                                        break
                            store_line_no += 1
                        if store_line_no == line_no:
                            # Do store_to_load_forwarding
                            # TODO: Make sure value is constant (TODO: or not assigned between)
                            val_to_forward = store_may_forward[ptr_name][0]
                            instr.update({
                                'op': 'id',
                                'args': [val_to_forward],
                            })

                    update_dest(ALL_MEM_LOCATION)
            
            if 'op' in instr and instr['op'] == 'store':
                ptr_name = instr['args'][0]
                store_may_forward[ptr_name] = (instr['args'][1], line_no)
            
            new_blk.append(instr)
        blocks[blk_name] = new_blk

    fn['instrs'] = cfg.reassemble(blocks)

def print_alias_analysis_result(alias_map):
    print("Alias Analysis:")
    for k in list(alias_map.keys()):
        print(f"{k}: {alias_map[k]}")
    print("-----------------------")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python alias_analysis.py <input_file>")
    #     sys.exit(1)

    # input_file = sys.argv[1]

    # # Read JSON data from the specified file
    # with open(input_file, 'r') as f:
    #     prog = json.load(f)

    prog = json.load(sys.stdin)

    for fn in prog["functions"]:
        alias_map = alias_analysis(fn)
        # print_alias_analysis_result(alias_map)
        store_to_load_forwarding(alias_map, fn)
    json.dump(prog, sys.stdout, indent=2)