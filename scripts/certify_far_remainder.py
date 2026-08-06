#!/usr/bin/env python3
"""Certificate for the analytic n=1 remainder on z >= 8."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.certification.far_remainder import global_remainder_bounds
from src.certification.far_profile import dominant_global_positive_certificate


def main():
    import argparse
    p=argparse.ArgumentParser(); p.add_argument('--precision',type=int,default=256); p.add_argument('--output',default='artifacts/certificates/far_asymptotic_profile.json')
    a=p.parse_args(); b=global_remainder_bounds(a.precision)
    phi_lower=20-b['L2_bound']
    t_lower=288-9*b['weighted_B_D2R']-32*b['weighted_B_DR']-2*b['L1_bound']*b['L2_bound']-b['L3_bound']
    ok=phi_lower.lower()>0 and t_lower.lower()>2
    artifact={'status':'PROVED_OUTWARD_ROUNDED_ON_[z>=8]' if ok else 'INCONCLUSIVE',
      'threshold_z':'8','equivalent_x_range':'[1/2,infinity)','precision_bits':a.precision,
      'formula_version':'far-remainder-v1','source_commit':subprocess.run(['git','rev-parse','--short','HEAD'],capture_output=True,text=True).stdout.strip(),
      'dominant_certificate':dominant_global_positive_certificate(),
      'B_R':str(b['B_R']),'B_DR':str(b['B_DR']),'B_D2R':str(b['B_D2R']),'B_D3R':str(b['B_D3R']),
      'weighted_B_DR':str(b['weighted_B_DR']),'weighted_B_D2R':str(b['weighted_B_D2R']),
      'L1_bound':str(b['L1_bound']),'L2_bound':str(b['L2_bound']),'L3_bound':str(b['L3_bound']),
      'Phi_second_lower':str(phi_lower),'T_lower':str(t_lower),
      'ratio_bounds':{str(k):str(v) for k,v in b['ratio_bounds'].items()},
      'monotonicity_certificate':'a/z-2b/(2z-3)-c<0 for a<=4,z>=8,c>=3'}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(artifact,indent=2)+'\n')
    print(json.dumps({'status':artifact['status'],'Phi_second_lower':artifact['Phi_second_lower'],'T_lower':artifact['T_lower']},indent=2))
    raise SystemExit(0 if ok else 2)
if __name__=='__main__': main()
