import json, sys, time
from pathlib import Path
from load_case import load_case
from acdc_engine import run_acdc

here = Path(__file__).resolve().parent
grid = sys.argv[1]
out  = Path(sys.argv[2])
t0 = time.time()
case = load_case(here / grid)
res  = run_acdc(case)
el = time.time() - t0
keys = sorted(res.keys()) if isinstance(res, dict) else type(res).__name__
payload = {"grid": grid, "elapsed_s": round(el,2), "keys": keys, "result": res}
out.write_text(json.dumps(payload, default=str))
print(f"OK {grid}  {el:.1f}s  keys={keys}")
