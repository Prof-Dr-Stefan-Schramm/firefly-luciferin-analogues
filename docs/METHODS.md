# Methods, how this dataset was compiled

This note records how the compilation was built, checked and normalised, so the
numbers can be judged and reused with confidence.

## Scope

The dataset covers **synthetic analogues of the firefly substrate D-luciferin**
- compounds designed to be turned over by firefly (or beetle) luciferase, or to
probe that reaction. It records their **optical properties** (absorption,
fluorescence), their **bioluminescence** (emission maximum, light output,
absolute quantum yield, spectral distribution), and the **enzyme kinetics** of
their turnover (Km, Vmax, kcat, inhibition constants), together with a few
physicochemical and derived quantities.

Out of scope, and listed separately in `not_included.csv`: oxyluciferin
(emitter) models, adenylate intermediates, bare heterocyclic fragments and
binding-site probes, nitrile precursors, and compounds whose structure could
not be established from the primary literature.

## Sources

Values were compiled from the primary literature, 77 sources, listed in
`references.csv` / `references.bib`. Every DOI was verified against the Crossref
record (`doi_verified_via_crossref`). A handful of sources are cited in the
chapter for context but contribute no number to the dataset; they are marked
`used_for_a_value = FALSE`.

## Extraction and verification

- Each value was read from its source and recorded with the luciferase, the
  assay conditions, the comparison basis, and a locator (table, figure or page).
- Each value was then checked against the source text; the outcome is in
  `verification_status`. Where the working record and the source disagreed, the
  value was corrected to the source (`corrected`) or, if it could not be
  resolved, flagged (`provisional`, `not_found`).
- Structures were checked against the characterisation in each source's
  experimental section or supporting information, and against the configuration
  the source states; the outcome is in `structure_verified`. SMILES were
  round-tripped through RDKit, and systematic names, where given, were parsed
  independently (OPSIN) and compared.

A large curation and audit pass reconciled duplicate records, split values that
had been merged, and corrected mis-attributions; values first surfaced or
recovered in that pass are marked `new` in `verification_status`.

## Normalisation, the points that matter scientifically

**Emission maxima are substrate + enzyme + pH.** A bioluminescence emission
maximum is not a property of the substrate alone. Every emission value carries
its luciferase (`enzyme`, and a coarse `enzyme_class`) and a `ph_regime`,
because the maximum shifts red as pH falls and as the enzyme changes. Values for
one compound with different enzymes are kept as separate rows and must not be
averaged.

**Relative light output is not one quantity.** Reports use peak intensity,
integrated photon flux, specific activity, or in-vivo signal, against different
references and in different settings. Rather than force these onto one scale,
each value keeps four fields that make its meaning explicit, `direction`,
`denominator`, `setting`, `basis`. The polarity was normalised so that
"weaker than", "N-fold fewer", "% of" and specific-activity reports are all
readable consistently through `direction`. Comparisons must be made within one
consistent combination of these fields.

**Absolute vs relative quantum yield.** Absolute bioluminescence quantum yield
is held in its own property, separate from relative output; only seven compounds
have one. Relative *fluorescence* quantum yields (against 6′-aminoluciferin = 1)
are likewise held separately from absolute fluorescence quantum yields.

**Kinetics.** Km values are recorded for the luciferin substrate; values
obtained with enzyme mutants are labelled through `enzyme` and were not mixed
with wild-type Km when a wild-type figure was needed. Vmax and kcat are
instrument-referenced unless the source gives absolute units, and are labelled
as such.

**Stereochemistry.** Firefly luciferase turns over only the D-enantiomer.
Racemates are flagged (`stereochemistry = racemate`); at a nominal concentration
they present roughly half that concentration of usable substrate, which matters
when comparing outputs.

## What was removed for this public release

Two kinds of content in the working record are **not** published:

1. **Verbatim source text.** Each value in the working file carried a
   verification quote copied from the cited paper, and several free-text fields
   held further quoted sentences. None of that is in the released files; a short,
   non-verbatim `source_locator` points to where the value sits in the paper.
2. **Internal editorial remarks.** The working record kept the audit trail in
   plain language (notes on what was corrected, cross-checks, and so on). These
   are notes to the compiler, not data, and were stripped.

The released files therefore contain the facts and the pointers to the sources,
not the sources' wording, figures or tables. For those, follow the DOI.

## Reproducing the analysis

`scripts/reproduce_statistics.py` reads the released data and recomputes the
headline statistics reported in the chapter: the compound and measurement
counts, the per-class table, the most-studied compounds, and the Pareto front of
emission red-shift against in-vitro light output. It writes
`data/analysis_summary.json`. It runs on the published files alone; nothing in
it needs the internal working record.

The wild-type/engineered split used in some of those statistics is derived here
from the coarse `enzyme_class` heuristic, so a few enzyme-conditioned figures are
approximate; the chapter's exact figures use the fully canonicalised enzyme
assignments in `enzyme`.
