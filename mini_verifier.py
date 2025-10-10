#!/usr/bin/env python3
import json, sys, glob, os

def load_json(p):
    with open(p,"r") as f: return json.load(f)

def sign_of_ball(j):
    lo = float(j["mid"]) - float(j["rad"])
    hi = float(j["mid"]) + float(j["rad"])
    if hi < 0: return "neg"
    if lo > 0: return "pos"
    return "unknown"

def check_zero_cert(path):
    J = load_json(path)
    ok = True; msgs = []
    if J.get("type") != "zero_bracket_cert":
        return False, ["wrong type"]
    for key in ["bracket","Z(a)","Z(b)","sign_change","Zprime_lower_bound_abs","bisection_root_estimate"]:
        if key not in J: ok=False; msgs.append(f"missing {key}")
    sa = sign_of_ball(J["Z(a)"]); sb = sign_of_ball(J["Z(b)"])
    if J["Z(a)"].get("sign") != sa: msgs.append("Z(a) sign mismatch"); ok=False
    if J["Z(b)"].get("sign") != sb: msgs.append("Z(b) sign mismatch"); ok=False
    if J["Zprime_lower_bound_abs"] <= 0 and J.get("unique_and_simple", False):
        msgs.append("|Z'| lower bound <=0 but unique_and_simple=True"); ok=False
    return ok, msgs

def check_block_cert(path):
    J = load_json(path)
    ok = (J.get("type")=="block_count_cert")
    msgs = [] if ok else ["wrong type"]
    for key in ["T1","T2","mode","count"]:
        if key not in J: msgs.append(f"missing {key}"); ok=False
    return ok, msgs

def main():
    if len(sys.argv)<2:
        print("Usage: python mini_verifier.py <cert_or_dir> [more ...]")
        sys.exit(1)
    overall_ok = True
    for arg in sys.argv[1:]:
        paths = []
        if os.path.isdir(arg): 
            paths = glob.glob(os.path.join(arg,"*.json"))
        else: 
            paths = [arg]
        for p in paths:
            J = load_json(p)
            if J.get("type")=="zero_bracket_cert":
                ok, msgs = check_zero_cert(p)
            elif J.get("type")=="block_count_cert":
                ok, msgs = check_block_cert(p)
            else:
                ok=False; msgs=["unknown type"]
            print(f"[{ 'OK' if ok else 'FAIL' }] {p}")
            for m in msgs: print("  -", m)
            overall_ok = overall_ok and ok
    sys.exit(0 if overall_ok else 2)

if __name__=="__main__":
    main()
