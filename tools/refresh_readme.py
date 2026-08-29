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
    names, frm = set(), 0
    while True:
        s = fetch("https://registry.npmjs.org/-/v1/search?"
                  f"text={urllib.parse.quote('maintainer:'+maintainer)}&size=250&from={frm}")
        objs = s.get("objects", [])
        for o in objs:
            nm = o["package"]["name"]
            # keep only packages this account actually maintains
            pub = o["package"].get("publisher", {}).get("username")
            maints = {m.get("username") for m in o.get("maintainers", [])}
            if pub == maintainer or maintainer in maints or nm.startswith("@f-keys/"):
                names.add(nm)
        if len(objs) < 250:
            break
        frm += 250
    if not names:
        raise RuntimeError("npm returned zero packages — refusing to write")
    return sorted(names)


def pypi_packages(listed):
    ok = []
    for name in listed:
        try:
            fetch(f"https://pypi.org/pypi/{name}/json")
            ok.append(name)
        except RuntimeError:
            raise RuntimeError(f"PyPI package '{name}' did not verify — refusing to write")
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
    def npm_link(n):
        return f"[`{n}`](https://www.npmjs.com/package/{n})"
    pypi_line = " · ".join(f"`{n}`" for n in pypi)
    npm_line = " · ".join(npm_link(n) for n in npm)
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
