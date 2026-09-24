# Changelog

All notable changes to this dataset are recorded here. Versions follow
[semantic versioning](https://semver.org/) adapted for data: the major number
changes when the schema or the meaning of existing fields changes, the minor
number when compounds, values or sources are added, and the patch number for
corrections that do not add records.

## [Unreleased]

- Removed the `figures/` folder. The analysis figures appear in the book
  chapter and are not part of the dataset. Data files are unchanged.
- README: noted the use of AI assistance in compiling the dataset.

## [1.0.0] (2026-09-24)

First public release.

- Archived on Zenodo: version DOI https://doi.org/10.5281/zenodo.22933437; concept DOI https://doi.org/10.5281/zenodo.22933436
- 195 compounds in scope; 19 out-of-scope compounds listed with reasons.
- 2103 measurement rows across 77 sources; every DOI verified against Crossref.
- 193 structures (SMILES, InChI, InChIKey) exported to SDF.
- Data in CSV and JSON (primary) and XLSX (convenience copy).
- `reproduce_statistics.py` regenerates the chapter's headline statistics from
  the released files.
- Verbatim source text and internal editorial remarks removed for public
  release (see `docs/METHODS.md`).
- Data licensed CC BY 4.0; scripts licensed MIT.
