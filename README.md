```
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                            ║
║             ██████╗  ██████╗ ███╗   ██╗███████╗ █████╗ ██╗     ███████╗███████╗            ║
║            ██╔════╝ ██╔═══██╗████╗  ██║╚══███╔╝██╔══██╗██║     ██╔════╝╚══███╔╝            ║
║            ██║  ███╗██║   ██║██╔██╗ ██║  ███╔╝ ███████║██║     █████╗    ███╔╝             ║
║            ██║   ██║██║   ██║██║╚██╗██║ ███╔╝  ██╔══██║██║     ██╔══╝   ███╔╝              ║
║            ╚██████╔╝╚██████╔╝██║ ╚████║███████╗██║  ██║███████╗███████╗███████╗            ║
║             ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝            ║
║                                                                                            ║
║                           axiom provenance for formal libraries                            ║
║                                                                                            ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝
```

`#print axioms` will tell you that a theorem depends on the axiom of choice. It
will not tell you whether the theorem needed it.

I build tools that answer the second question, then go and fix the answers I
don't like.

## set.mm

Five changes merged into [metamath/set.mm](https://github.com/metamath/set.mm)
since 17 August 2026. Each removes a dependence on the axiom of choice from a
theorem whose own hypotheses already ruled it out.

- [#5442](https://github.com/metamath/set.mm/pull/5442) `difelsiga` — a sigma-algebra is closed under class difference. The proof went through countable intersection, where choice enters, because pairwise union happened to be stated *after* it in the file. Statement order was the whole cause.
- [#5443](https://github.com/metamath/set.mm/pull/5443) `fnrndomnum` — the well-orderable-domain form of `fnrndomg`. The library had the equivalent for `fodomg` and nothing for this one.
- [#5445](https://github.com/metamath/set.mm/pull/5445) `madefi` — the set in question is finite, and the proof had already proved it finite a few steps earlier.
- [#5447](https://github.com/metamath/set.mm/pull/5447) `sigaclci` — reached the general countability lemma instead of the one for an indexed family.
- [#5448](https://github.com/metamath/set.mm/pull/5448) `omeiunle` — indexes over an upper integer set, which is countable without assuming anything.

I am not going to total those. Where two repairs feed the same subtree each one
reads near zero alone, and the subtree only leaves the cone when the last of
them goes, so a sum is wrong in both directions. The number that means anything
is the counterfactual over the whole set at once.

## Tools

| | | |
|---|---|---|
| [gonzalgo](https://github.com/vince-gonzalez/gonzalgo) | axiom provenance for Lean 4 and Metamath: which step of a proof introduced an axiom | [PyPI](https://pypi.org/project/gonzalgo/) |
| [mmforge](https://github.com/vince-gonzalez/mmforge) | avoidable axiom dependencies in Metamath databases | [PyPI](https://pypi.org/project/mmforge/) |
| [loadbearing](https://github.com/vince-gonzalez/loadbearing) | what a claim asserts, against what its derivation actually used | [PyPI](https://pypi.org/project/loadbearing/) |
| [certivl](https://github.com/vince-gonzalez/certivl) | exact rational and certified interval arithmetic | [PyPI](https://pypi.org/project/certivl/) |

## Elsewhere

ORCID [0009-0005-3640-014X](https://orcid.org/0009-0005-3640-014X) ·
[f-keys.com](https://f-keys.com) · vincegonzalez@me.com
