```
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                            ║
║                       ███████╗    ██╗  ██╗███████╗██╗   ██╗███████╗                        ║
║                       ██╔════╝    ██║ ██╔╝██╔════╝╚██╗ ██╔╝██╔════╝                        ║
║                       █████╗█████╗█████╔╝ █████╗   ╚████╔╝ ███████╗                        ║
║                       ██╔══╝╚════╝██╔═██╗ ██╔══╝    ╚██╔╝  ╚════██║                        ║
║                       ██║         ██║  ██╗███████╗   ██║   ███████║                        ║
║                       ╚═╝         ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝                        ║
║                                                                                            ║
║                             ___ ___ ___   _ _____ _____   _____                            ║
║                            / __| _ \ __| /_\_   _|_ _\ \ / / __|                           ║
║                           | (__|   / _| / _ \| |  | | \ V /| _|                            ║
║                            \___|_|_\___/_/ \_\_| |___| \_/ |___|                           ║
║                                                                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
```

A lot of things get claimed and never checked. Formal libraries record which
axioms a theorem used but not which it needed. Geometric bounds get quoted from
papers nobody re-ran. Colour vision tests get delivered through screens nobody
measured. Published records get cited without anyone confirming what is in
them.

I build the instruments that check, and then I go and use them. Below is most
of it. 58 deposited works, 35 packages, and a handful of sites that are up.

## Formal mathematics

Which step of a proof spent an axiom, how far the spending reaches, and whether
the theorem needed it.

| | |
|---|---|
| [gonzalgo](https://github.com/vince-gonzalez/gonzalgo) | axiom provenance for Lean 4 and Metamath |
| [mmforge](https://github.com/vince-gonzalez/mmforge) | avoidable axiom dependencies in Metamath databases |
| [loadbearing](https://github.com/vince-gonzalez/loadbearing) | what a claim asserts, against what its derivation used |

Eight changes merged into [metamath/set.mm](https://github.com/metamath/set.mm)
so far, each removing a dependence on the axiom of choice from a theorem whose
own hypotheses already ruled it out: `difelsiga`, `fnrndomnum`, `madefi`,
`disjinfi`, `sigaclci`, `omeiunle`, `fimact`, and the `fnct`/`dmct`/`ffsrn`
family. In one of them the entire cause was statement order. Two more are open.

I do not total those. Where two repairs feed the same subtree each reads near
zero alone, and the subtree only leaves the cone when the last of them goes.

## Certified computation

Bounds that hold because a machine checked them, not because a paper said so.

- exact rational and interval arithmetic — [certivl](https://github.com/vince-gonzalez/certivl)
- the Lebesgue universal cover, opaque barriers, and Fejes Toth's point-goalie problem — [certified-covers](https://github.com/vince-gonzalez/certified-covers)
- odd perfect numbers: a congruence obstruction on the Euler prime, and an exact calculator for Norton's abundancy bound
- an independent verification of an 11948-point kissing configuration, and maximality results for the Cohn-Li constructions
- what four verified Rocq developments assume, by source-level axiom census — CompCert, fiat-crypto, Iris, and the Verified Software Toolchain, with axiom reach from 0.0% to 65.6% — [10.5281/zenodo.22162430](https://doi.org/10.5281/zenodo.22162430)

## The Voynich manuscript

Seven papers on Voynichese as a positionally constrained system, with the null
tests and positive controls that most of the field skips. Structure only. I make
no claim about what any of it means.

## Colour vision

Pseudoisochromatic plates generated procedurally in the browser, and the finding
that plate design type is recoverable from delivered colour.

[opticquiz.com](https://opticquiz.com) · [ishihara](https://github.com/vince-gonzalez/ishihara)

## Classification, evidence, and the published record

A dimensional address grammar for classification, and what it takes to admit
machine-generated evidence in a proceeding without pretending a model is a
witness.

[modulign.org](https://modulign.org) · [epistemend.org](https://epistemend.org) ·
[apriori](https://github.com/vince-gonzalez/apriori) ·
[authorecon](https://pypi.org/project/authorecon/)

## Food, and where it comes from

- [5best2buy.com](https://5best2buy.com) — shelves for independent American food makers
- [independent-us-food-makers](https://github.com/vince-gonzalez/independent-us-food-makers) — open datasets, including named halal and kosher certification
- [poticas.com](https://poticas.com) — the history and record of potica, a Slovenian nut roll, and a paper on its transmission in America

## Games

| | |
|---|---|
| [LOCK IN](https://trailer-load.com) | a browser freight-loading simulator that plays like a game and trains like a course. Warehouse loading, weight distribution, axle limits |
| [PROMPT](https://prompt.f-keys.com) | a Discord party game, played in reverse: everyone sees an answer an AI gave, and writes the question that must have caused it |
| [DaisuPop](https://dp.f-keys.com) | a shared dice popper as a Discord Activity, synced live so the pop happens for everyone at once |
| MICDROP | an open-mic comedy arena built in Fortnite UEFN. Request the mic, get 120 seconds, and the audience votes you off with tomatoes |

## Software

| | |
|---|---|
| [keyj](https://pypi.org/project/keyj/) | guitar tablature to notes, rendered and played |
| [remapwrap](https://pypi.org/project/remapwrap/) | a phone as a control surface, no app install |
| [qv.f-keys.com](https://qv.f-keys.com) | live anonymous ballots |
| [tipstreams.com](https://tipstreams.com) | multi-method tipping, also an embeddable widget |
| [dogefundme.com](https://dogefundme.com) | isometric mini-golf, zero dependencies |

## Packages

16 on PyPI: `gonzalgo` · `mmforge` · `loadbearing` · `certivl` · `ishihara` · `authorecon` · `remapwrap` · `keyj` · `axsent` · `legible` · `openapi-drift` · `changewatch` · `moonbeam-miner` · `plumhud` · `saydo` · `opticquiz-cvd`.

19 on npm: `@f-keys/tip-widget` · `achromatopsia` · `colorblind-mcp` · `cvdplate` · `cvdsafe` · `cvdsafe-mcp` · `cvdsim` · `deutan` · `dichromacy` · `dogefundme` · `keyjockey` · `logmar` · `opticquiz-cvd` · `opticquiz-cvd-mcp` · `opticquiz-eye` · `protanopia` · `safepalette` · `trichromacy` · `tritanopia`.

`keyj` also ships on winget as `com.fkeys.keyj`.

## Elsewhere

ORCID [0009-0005-3640-014X](https://orcid.org/0009-0005-3640-014X) ·
[f-keys.com](https://f-keys.com) · vincegonzalez@me.com

This account is a rename, not a beginning: the work lived under
`zengineco` from 2024 until August 2026, and the transferred repositories
redirect here.
