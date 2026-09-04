#!/usr/bin/env python3
"""Recompute the README's counts and package list from live registries.

Sources, all public (no tokens): Zenodo (works, by ORCID), npm (packages, by
maintainer), PyPI (packages, from the verified list in readme_sources.json).

Design rule: if any source cannot be verified after retries, the script writes
nothing and exits non-zero. A run that cannot confirm a number must not print
one. Stdlib only, so the workflow needs no dependency install.
"""
import json, re, sys, time, urllib.request, urllib.parse, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "readme_sources.json"), encoding="utf-8"))
UA = "fkeys-readme-bot/1.0 (+https://github.com/vince-gonzalez)"


def fetch(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            last = e
            time.sleep(2 * (i + 1))
    raise RuntimeError(f"fetch failed after {tries}: {url}\n  {last}")


def npm_packages(maintainer):
    """Discover packages via the maintainer search, then CONFIRM each one against
    the registry's own maintainer list. Search relevance is not proof of ownership."""
    found, frm = set(), 0
    while True:
        s = fetch("https://registry.npmjs.org/-/v1/search?"
                  f"text={urllib.parse.quote('maintainer:'+maintainer)}&size=250&from={frm}")
        objs = s.get("objects", [])
        for o in objs:
            found.add(o["package"]["name"])
        if len(objs) < 250:
            break
        frm += 250
    owned = []
    for nm in sorted(found):
        doc = fetch("https://registry.npmjs.org/" + urllib.parse.quote(nm, safe=""))
        maints = {m.get("name") for m in (doc.get("maintainers") or [])}
        if maintainer in maints:
            owned.append(nm)
    if not owned:
        raise RuntimeError("npm returned zero owned packages — refusing to write")
    return owned


def pypi_packages(listed):
    """Verify each listed package both EXISTS and is OWNED by this account.
    Existence alone is not ownership — a common name can belong to a stranger."""
    markers = [m.lower() for m in CFG.get("ownership_markers", [])]
    for name in listed:
        info = fetch(f"https://pypi.org/pypi/{name}/json").get("info", {})
        blob = " ".join(str(info.get(k)) for k in
                        ("author", "author_email", "home_page", "project_urls", "maintainer")).lower()
        if markers and not any(m in blob for m in markers):
            raise RuntimeError(
                f"PyPI package '{name}' exists but does NOT appear to belong to this "
                f"account (no ownership marker in its metadata) — refusing to write")
    return listed  # preserve the curated order


def zenodo_works(orcid):
    q = urllib.parse.quote(f"creators.orcid:{orcid}")
    parents, page = set(), 1
    while True:
        j = fetch(f"https://zenodo.org/api/records?q={q}&size=25&page={page}")
        hits = j.get("hits", {}).get("hits", [])
        if not hits:
            break
        for h in hits:
            pid = (h.get("parent", {}) or {}).get("id") or h.get("conceptrecid") or h.get("id")
            parents.add(str(pid))
        if len(hits) < 25:
            break
        page += 1
        time.sleep(1.0)
    if not parents:
        raise RuntimeError("Zenodo returned zero works — refusing to write")
    return len(parents)


def build_packages_section(pypi, npm):
    pypi_line = " · ".join(f"`{n}`" for n in pypi)
    npm_line = " · ".join(f"`{n}`" for n in npm)
    n_p, n_n = len(pypi), len(npm)
    return (
        "## Packages\n\n"
        f"{_num(n_p).capitalize()} on PyPI: {pypi_line}.\n\n"
        f"{_num(n_n).capitalize()} on npm: {npm_line}.\n\n"
        "`keyj` also ships on winget as `com.fkeys.keyj`."
    )


def _num(n):
    words = {1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",
             8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve"}
    return words.get(n, str(n))


def main():
    pypi = pypi_packages(CFG["pypi"])
    npm = npm_packages(CFG["npm_maintainer"])
    works = zenodo_works(CFG["orcid"])
    packages = len(pypi) + len(npm)

    path = os.path.join(ROOT, "README.md")
    text = open(path, encoding="utf-8").read()
    orig = text

    text, n = re.subn(r"\d+ deposited works, \d+ packages",
                      f"{works} deposited works, {packages} packages", text, count=1)
    if n != 1:
        raise RuntimeError("could not find the 'N deposited works, M packages' line")

    text, n = re.subn(r"## Packages\n.*?(?=\n## )",
                      build_packages_section(pypi, npm) + "\n", text,
                      count=1, flags=re.DOTALL)
    if n != 1:
        raise RuntimeError("could not find the ## Packages section")

    if text == orig:
        print(f"no change (works={works}, packages={packages}, "
              f"pypi={len(pypi)}, npm={len(npm)})")
        return
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    print(f"updated: works={works}, packages={packages} "
          f"(pypi={len(pypi)}, npm={len(npm)})")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"refuse-to-write: {e}", file=sys.stderr)
        sys.exit(1)
