import sys
import json
import cfg

if __name__ == "__main__":
    prog = json.load(sys.stdin)
    cnt = 0
    for fn in prog["functions"]:
        for instr in fn['instrs']:
            if 'op' in instr and instr['op'] == 'load':
                cnt += 1
    # json.dump(prog, sys.stdout, indent=2)
    sys.stderr.write(f"total_load_inst: {cnt}\n")
