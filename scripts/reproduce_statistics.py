#!/usr/bin/env python3
"""Reproduce the headline statistics of the chapter from the PUBLIC data.

Run:  python reproduce_statistics.py
Reads data/firefly_luciferin_analogues.json (or the CSV files) and writes
data/analysis_summary.json, printing the numbers the chapter reports so a
reader can check them against the text.

Nothing here needs the internal working record; it runs on the released files
alone. That is the point: the analysis is reproducible from what is published.
"""
import json, os, csv, statistics
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE) if os.path.basename(HERE) == 'scripts' else HERE
DATA = os.path.join(ROOT, 'data')


def load():
    p = os.path.join(DATA, 'firefly_luciferin_analogues.json')
    if os.path.exists(p):
        b = json.load(open(p))
        return b['compounds'], b['measurements'], b['references']
    # CSV fallback
    def rd(n):
        return list(csv.DictReader(open(os.path.join(DATA, n), encoding='utf-8')))
    return rd('compounds.csv'), rd('measurements.csv'), rd('references.csv')


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def is_wt(m):
    return m.get('enzyme_class') == 'wild-type firefly luciferase'


def main():
    comp, meas, refs = load()
    by_id = {c['compound_id']: c for c in comp}

    # ---- totals
    n_struct = sum(1 for c in comp if c.get('smiles'))
    bl = [m for m in meas if m['property'] == 'bioluminescence emission maximum']
    bl_wt = [m for m in bl if is_wt(m)]   # wild-type by the coarse enzyme_class flag
    totals = {
        'compounds_in_scope': len(comp),
        'measurements': len(meas),
        'references': len(refs),
        'references_used_for_a_value':
            sum(1 for r in refs if str(r.get('used_for_a_value')).upper() in ('TRUE', '1')),
        'structures_with_smiles': n_struct,
        'bl_max_values': len(bl),
        'bl_max_wildtype_values (heuristic split)': len(bl_wt),
        'compounds_with_any_bl_max': len({m['compound_id'] for m in bl}),
        'racemates': sum(1 for c in comp if c.get('stereochemistry') == 'racemate'),
    }

    # ---- per-class table
    classes = {}
    for c in comp:
        classes.setdefault(c['class_key'], {'label': c['structural_class'],
                                            'ids': [], 'bl_wt': []})
        classes[c['class_key']]['ids'].append(c['compound_id'])
    for m in bl_wt:
        v = num(m['value_num'])
        ck = by_id.get(m['compound_id'], {}).get('class_key')
        if v is not None and ck in classes:
            classes[ck]['bl_wt'].append(v)
    class_table = []
    for ck, d in classes.items():
        w = d['bl_wt']
        class_table.append({
            'class_key': ck, 'class_label': d['label'],
            'n_compounds': len(d['ids']),
            'n_measurements': sum(1 for m in meas
                                  if by_id.get(m['compound_id'], {}).get('class_key') == ck),
            'wt_bl_max_median': round(statistics.median(w), 1) if w else None,
            'wt_bl_max_min': min(w) if w else None,
            'wt_bl_max_max': max(w) if w else None,
            'wt_bl_max_n': len(w)})
    class_table.sort(key=lambda r: -r['n_compounds'])

    # ---- most-studied
    per = defaultdict(lambda: {'n': 0, 'refs': set(), 'enz': set()})
    for m in meas:
        cid = m['compound_id']
        per[cid]['n'] += 1
        if m.get('citation_key'):
            per[cid]['refs'].add(m['citation_key'])
        if m.get('enzyme'):
            per[cid]['enz'].add(m['enzyme'])
    most = sorted(({'compound_id': cid, 'name': by_id[cid]['name'],
                    'class_key': by_id[cid]['class_key'],
                    'n_measurements': v['n'], 'n_references': len(v['refs']),
                    'n_enzymes': len(v['enz'])}
                   for cid, v in per.items() if cid in by_id),
                  key=lambda r: -r['n_measurements'])[:10]

    # ---- Pareto: median wild-type BL max vs median in-vitro output vs D-luciferin
    out = defaultdict(list)
    wl = defaultdict(list)
    for m in meas:
        if (m['property'] == 'relative light output'
                and m.get('setting') == 'in vitro'
                and m.get('direction') == 'brighter_is_larger'
                and str(m.get('denominator', '')).lower().startswith('d-luciferin')):
            v = num(m['value_num'])
            if v is not None:
                out[m['compound_id']].append(v)
    for m in bl_wt:
        v = num(m['value_num'])
        if v is not None:
            wl[m['compound_id']].append(v)
    pts = []
    for cid in set(out) & set(wl):
        pts.append({'compound_id': cid, 'name': by_id[cid]['name'],
                    'class_key': by_id[cid]['class_key'],
                    'wt_bl_max_median': round(statistics.median(wl[cid]), 1),
                    'output_median_vs_dluc': round(statistics.median(out[cid]), 1)})
    front = []
    for p in sorted(pts, key=lambda r: (-r['wt_bl_max_median'], -r['output_median_vs_dluc'])):
        if all(not (q['wt_bl_max_median'] >= p['wt_bl_max_median']
                    and q['output_median_vs_dluc'] > p['output_median_vs_dluc'])
               and not (q['output_median_vs_dluc'] >= p['output_median_vs_dluc']
                        and q['wt_bl_max_median'] > p['wt_bl_max_median'])
               for q in pts if q['compound_id'] != p['compound_id']):
            front.append(p)
    front.sort(key=lambda r: r['wt_bl_max_median'])

    summary = {'totals': totals, 'classes': class_table,
               'most_studied': most,
               'pareto_front_redshift_vs_output': front}
    json.dump(summary, open(os.path.join(DATA, 'analysis_summary.json'), 'w'),
              indent=1, ensure_ascii=False)

    print('=== Totals ===')
    for k, v in totals.items():
        print(f'  {k:38s} {v}')
    print('\n=== Classes (by number of compounds) ===')
    print(f'  {"class":13s} {"n":>3s} {"meas":>5s} {"WT median":>10s} {"range":>12s}')
    for r in class_table:
        rng = (f'{r["wt_bl_max_min"]:.0f}-{r["wt_bl_max_max"]:.0f}'
               if r['wt_bl_max_min'] is not None else '-')
        print(f'  {r["class_key"]:13s} {r["n_compounds"]:3d} '
              f'{r["n_measurements"]:5d} '
              f'{("-" if r["wt_bl_max_median"] is None else r["wt_bl_max_median"]):>10} {rng:>12}')
    print('\n=== Most-studied compounds ===')
    for r in most[:6]:
        print(f'  {r["compound_id"]:6s} {r["name"][:36]:36s} '
              f'{r["n_measurements"]:4d} values, {r["n_references"]:2d} refs')
    print('\n=== Pareto front (median WT BL max vs median in-vitro output) ===')
    for r in front:
        print(f'  {r["compound_id"]:6s} {r["name"][:34]:34s} '
              f'{r["wt_bl_max_median"]:6.1f} nm  {r["output_median_vs_dluc"]:7.1f} '
              f'(D-luc=100)')
    print('\nWrote data/analysis_summary.json')


if __name__ == '__main__':
    main()
