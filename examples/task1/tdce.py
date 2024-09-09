import json
import sys

def is_pure(instr):
    return instr["op"] not in ["call", "print", "alloc"]

def trivial_dead_code_elimination(func):
    
    instrs = func["instrs"]
    converged = False
    while not converged:
        used = set()
        new_instrs = []
        for instr in instrs:
            used.update(instr.get("args", []))

        for instr in instrs:
            if ("dest" in instr) and (instr["dest"] not in used and is_pure(instr)):
                # remove this instruction
                continue
            else:
                new_instrs.append(instr)
        
        converged = (len(new_instrs) >= len(instrs))
        instrs = new_instrs
    
    return instrs


if __name__ == "__main__":
    prog = json.load(sys.stdin)
    for fn in prog["functions"]:
        fn["instrs"] = trivial_dead_code_elimination(fn)
    json.dump(prog, sys.stdout, indent=2)
