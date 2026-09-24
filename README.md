# Firefly luciferin analogues, a compiled dataset

A curated, machine-readable compilation of the **optical, bioluminescence and
kinetic properties of 195 synthetic firefly D-luciferin analogues**, drawn from
the primary literature. It holds **2103 individual reported values** across
**77 sources**, each carrying the luciferase used, the assay conditions, the
comparison basis and the DOI of its source, together with the structures and
the scripts that reproduce the accompanying analysis.

The compilation is the quantitative basis for a chapter on the structural
diversity of synthetic firefly luciferins in a monograph on chemiluminescence
and bioluminescence. The book prints only the analysis; this repository is the
full underlying dataset, released so that others can find, reuse and cite it.

## How to cite

> Schramm, S. *Firefly luciferin analogues: a compiled dataset of optical,
> bioluminescence and kinetic properties* (version 1.0.0). Zenodo, 2026.
> https://doi.org/10.5281/zenodo.22933436

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22933436.svg)](https://doi.org/10.5281/zenodo.22933436)

This concept DOI always resolves to the newest version. To cite exactly
version 1.0.0, use its version DOI,
[10.5281/zenodo.22933437](https://doi.org/10.5281/zenodo.22933437). A
machine-readable citation is in `CITATION.cff`.

## What is in here

```
data/
  firefly_luciferin_analogues.json   the whole dataset in one structured file
  compounds.csv                      one row per compound (identity, class, structure)
  measurements.csv                   one row per reported value  ← the main table
  references.csv                     the 77 sources, with verified DOIs
  references.bib                     the same sources as BibTeX
  not_included.csv                   compounds found but left out of scope, with reasons
  structures.sdf                     193 structures with identifiers, for cheminformatics
  firefly_luciferin_analogues.xlsx   a convenience copy of the four CSV tables
  analysis_summary.json              headline statistics (written by the script below)
docs/
  CODEBOOK.md                        every column, its meaning and its vocabulary
  METHODS.md                         how the data were compiled, checked and normalised
scripts/
  reproduce_statistics.py            recomputes the chapter's headline numbers
  requirements.txt                   Python packages the scripts need
CHANGELOG.md
CITATION.cff  .zenodo.json
LICENSE (data, CC BY 4.0)   LICENSE-CODE (scripts, MIT)
```

**Primary format:** the CSV and JSON files. **`measurements.csv` is the table
to filter and plot from.** The XLSX is a convenience copy only.

## Quick start

```bash
pip install -r scripts/requirements.txt
python scripts/reproduce_statistics.py     # prints the headline numbers, writes analysis_summary.json
```

Read any table with pandas:

```python
import pandas as pd
m = pd.read_csv("data/measurements.csv")
# median wild-type emission maximum per structural class:
bl = m[(m.property == "bioluminescence emission maximum") &
       (m.enzyme_class == "wild-type firefly luciferase")]
print(bl.groupby("structural_class").value_num.median().sort_values())
```

## Reading the data correctly, three things that matter

The compilation is built to prevent the usual mistakes made with luciferin data.
Please keep these in mind:

1. **A bioluminescence emission maximum belongs to the substrate *and* the
   enzyme together.** Every value names its luciferase (`enzyme`, and a coarse
   `enzyme_class`). Do **not** average or compare values for one compound across
   different luciferases as if they were one number.

2. **"Relative light output" is not one quantity.** Across the literature it is
   reported as peak intensity, integrated photon flux, specific activity or an
   in-vivo signal, against different references. Each value therefore carries
   `direction`, `denominator`, `setting` and `basis`. Filter to a single,
   consistent combination before comparing, and do not compare raw numbers
   across studies without checking these fields.

3. **Absolute bioluminescence quantum yield is kept separate** from relative
   output (`property = "absolute bioluminescence quantum yield"`); only seven
   compounds have one.

`docs/CODEBOOK.md` explains every field; `docs/METHODS.md` explains how the
values were extracted, verified and normalised.

## Provenance and verification

- Every value was read from, and checked against, its cited source; the outcome
  is in `verification_status`. `source_locator` points to the table, figure or
  page it sits in.
- Every DOI in `references.csv` was verified against the Crossref record
  (`doi_verified_via_crossref`).
- **Verbatim text from the source papers is not reproduced here.** The dataset
  contains facts (numbers, identifiers, paraphrased conditions) and pointers to
  the sources, not their wording, figures or tables. For those, follow the DOI.
- Use of AI: the large language model Claude Opus 5 (Anthropic) assisted in
  mining the source papers, extracting and compiling the values, and running the
  analysis. The author directed the work and checked the results.

## Licence

- **Data** (`data/`): **CC BY 4.0**, reuse freely, with attribution. See `LICENSE`.
- **Scripts** (`scripts/`): **MIT**. See `LICENSE-CODE`.

## Contact

Stefan Schramm, HTW Dresden (stefan.schramm@htw-dresden.de)

Corrections and additions are welcome as GitHub issues or pull requests. Please
include the DOI and the table or figure your value comes from.
