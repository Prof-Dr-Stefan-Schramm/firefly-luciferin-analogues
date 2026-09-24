# Codebook

Every column in every table, its meaning and its controlled vocabulary. The
same fields appear in `firefly_luciferin_analogues.json` (as `compounds`,
`measurements`, `references`, `not_included`).

Missing values are written as an empty cell. An empty cell means *not reported
in the cited source*; it does not mean the property was never measured anywhere.

---

## compounds.csv, one row per compound (195 rows)

| column | meaning |
|---|---|
| `compound_id` | Stable internal identifier (e.g. `NAT01`, `AM21`). Used as the join key to `measurements.csv` and as the record name in `structures.sdf`. |
| `name` | Preferred name of the compound. |
| `aliases` | Other names and per-paper labels, `; `-separated. |
| `structural_class` | Full label of the structural class. |
| `class_key` | Short key for the class (see the class list below). |
| `subfamily` | Finer grouping within a class where one applies. |
| `ring_of_the_acid` | The ring bearing the carboxylic acid (thiazoline in the natural series, and its replacements). |
| `smiles` | Isomeric SMILES; stereochemistry as stated in the source. |
| `inchikey` | Standard InChIKey. |
| `iupac_name` | IUPAC name where established from the source. |
| `molecular_formula` | Molecular formula. |
| `mw` | Molecular weight (g mol⁻¹). |
| `stereochemistry` | `D_enantiomer`, `racemate`, `unknown`, or empty. Firefly luciferase turns over only the D-enantiomer; a racemate at nominal concentration *c* presents roughly *c*/2 of substrate. |
| `structure_confidence` | Compiler's confidence in the structure assignment (`high`, or empty). |
| `structure_verified` | Whether the structure was re-checked against the source: `confirmed`, `corrected`, `unverified`, or empty. |
| `n_measurements` | Number of measurement rows for this compound. |

Two compounds have no usable SMILES (structure not established from the primary
literature) and so are absent from `structures.sdf`.

---

## measurements.csv, one row per reported value (2103 rows), the main table

### Identity of the value

| column | meaning |
|---|---|
| `compound_id`, `compound_name`, `structural_class`, `subfamily` | The compound this value belongs to (denormalised for convenience). |
| `property` | What was measured. Vocabulary: *bioluminescence emission maximum; relative light output; fluorescence emission maximum; absorption maximum; fluorescence quantum yield; relative fluorescence quantum yield (6′-aminoluciferin = 1); absolute bioluminescence quantum yield; non-enzymatic chemiluminescence; pKa; pH optimum; spectral distribution fraction; optical band gap (E0-0); Stokes shift; molar absorptivity; physicochemical property; calculated property (not a measurement);* and, for enzyme kinetics, the specific parameter name (*Km for the luciferin; Vmax (instrument-referenced); kcat (instrument-referenced); inhibition constant; …*). |
| `quantity` | For kinetic and derived rows, a more specific description of the quantity. |
| `unit` | Unit of `value_num`. `nm`, `uM`, `%`, `eV`, `M-1 cm-1`, `mM`, `-` (dimensionless), or `see basis`/`see unit`/`nm or text` where the value is described in `value_reported`. |

### The number

| column | meaning |
|---|---|
| `value_num` | Numeric core of the value, parsed for plotting. Empty when the value is non-numeric or is a description. |
| `uncertainty` | Reported ± uncertainty on `value_num`, if any. |
| `range_low`, `range_high` | Endpoints when the source gives a range rather than a point. |
| `value_reported` | The fuller reported form in words (paraphrased, never a verbatim quote), including multi-value or qualitative reports that do not reduce to a single number. |

### How to read a relative or conditional value

| column | meaning |
|---|---|
| `scale` | `absolute`; `relative, 6'-aminoluciferin = 1 in the same solvent` (for `fl_rel_qy`); or empty. |
| `direction` | For light-output values, what "larger" means: `brighter_is_larger` (a relative brightness), `absolute_photon_flux`, `spectral_fraction`, `reduction_factor` (larger = dimmer), `percent_weaker`, `concentration_equivalence`. |
| `denominator` | The reference the value is expressed against, e.g. `D-luciferin = 100`, `Luc2 with D-luciferin = 100`, `aminoluciferin = 100`, `AkaLumine = 1`, `the same compound's emission with wild-type luciferase`, `a parent analogue, not D-luciferin`, `not stated`. |
| `setting` | `in vitro`, `live cell`, or `in vivo`. |
| `emission_band` | For multi-band emitters: `principal band`, `secondary or shoulder band`, `secondary, blue-shifted band`. |
| `bimodal` | `TRUE` if the emission spectrum for this value is bimodal. |

> To compare light outputs, first filter to **one** consistent combination, > for example `property = "relative light output"`, `setting = "in vitro"`,
> `direction = "brighter_is_larger"`, `denominator` starting `D-luciferin`.
> Comparing across different denominators or settings is meaningless.

### The measurement context

| column | meaning |
|---|---|
| `enzyme` | The luciferase, as described in the source (paraphrased). Empty for substrate-only properties (absorption, pKa, …). |
| `enzyme_class` | A coarse bucket for filtering: `wild-type firefly luciferase`, `engineered firefly luciferase`, `click-beetle luciferase`, `other`. This is a heuristic classification of the free-text `enzyme` string, provided for convenience; for careful work read `enzyme`. |
| `ph_regime` | `physiological or basic`, `acidic`, `pH series or pH independent`, or `unstated`. The bioluminescence maximum shifts red as pH falls, so this matters when comparing emission maxima. |
| `conditions` | Assay conditions in brief (buffer, concentrations, instrument), paraphrased from the source. |
| `basis` | What the value is the value *of*: the exact quantity and how it was obtained (e.g. "peak of the normalised BL spectrum"; "integrated photon flux over 2 min, PMT-corrected"). |

### Provenance

| column | meaning |
|---|---|
| `secondary` | `TRUE` = the value was quoted from a review or later paper, not read in the original report. |
| `provisional` | `TRUE` = flagged as provisional (source not fully verifiable). |
| `superseded` | `TRUE` = an earlier value later revised; kept for the record but not the primary value. |
| `source_locator` | Where the value sits in the cited paper: a table, figure or page (e.g. `Table S1`, `Figure 3c`). Non-verbatim. |
| `citation_key` | Key into `references.csv` / `references.bib` (first author + year). |
| `doi`, `url` | DOI and resolver URL of the source. |
| `verification_status` | Outcome of checking the value against the source: `confirmed`, `new` (added in the last curation pass), `corrected`, `secondary`, `wrong_enzyme`, `wrong_basis`, `misattributed`, `definitional`, `not_found`. |

---

## references.csv, the sources (77 rows)

| column | meaning |
|---|---|
| `citation_key` | First author + year (matches `measurements.citation_key` and the BibTeX keys). |
| `authors`, `title`, `journal`, `volume`, `issue`, `pages`, `year` | Bibliographic fields. |
| `doi`, `url` | DOI and resolver URL. |
| `doi_verified_via_crossref` | `TRUE` if the DOI was checked against the Crossref record. |
| `used_for_a_value` | `TRUE` if at least one value in `measurements.csv` comes from this source; `FALSE` for sources cited in the chapter but contributing no number to the dataset. |

## not_included.csv, out-of-scope compounds (19 rows)

Compounds found in the literature but deliberately excluded (heterocyclic
fragments and binding probes, nitrile precursors, oxyluciferin emitter models,
adenylates, unestablished structures). `reason` and `note` give the ground.

---

## The structural classes (`class_key`)

`natural`, `amino`, `cycluc`, `sulfonamide`, `sixprime`, `ringsubst`,
`thiazoline`, `corex`, `fused`, `piext_bt`, `piext_nobt`, `coumarin`,
`minimal`, `appendix`. Their full labels are in `structural_class`.

## structures.sdf

193 records, one per compound with a usable SMILES. Each carries SD properties
`compound_id`, `name`, `structural_class`, `subfamily`, `smiles`, `inchi`,
`inchikey`, `molecular_formula`, and, where known, `iupac_name` and
`stereochemistry`. 2D coordinates are computed with RDKit for depiction; they
are not experimental geometries.
