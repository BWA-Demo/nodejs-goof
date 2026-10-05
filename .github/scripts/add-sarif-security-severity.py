#!/usr/bin/env python3
"""Add GitHub Code Scanning security severities to Snyk SARIF files, in place.

GitHub shows Critical/High/Medium/Low only when a SARIF rule carries a numeric
`security-severity` property and a "security" tag; otherwise alerts fall back to
the generic error/warning/note. Snyk Open Source/Container already emit the
score; Snyk Code, IaC and Secrets do not, so this fills the gap:

  1. keep an existing numeric `security-severity`
  2. else use `properties.problem.severity` (IaC)
  3. else use the highest result `level` for the rule (Code, Secrets)

GitHub bands: >=9.0 critical, 7.0-8.9 high, 4.0-6.9 medium, 0.1-3.9 low.
"""
import json
import sys

SEVERITY_SCORE = {"critical": 9.5, "high": 8.0, "medium": 5.5, "low": 2.0}
LEVEL_SEVERITY = {"error": "high", "warning": "medium", "note": "low"}
LEVEL_RANK = {"note": 0, "warning": 1, "error": 2}


def score_to_level(score):
    return "error" if score >= 7.0 else "warning" if score >= 4.0 else "note"


def has_score(props):
    try:
        float(props.get("security-severity"))
        return True
    except (TypeError, ValueError):
        return False


def process_run(run):
    driver = run.get("tool", {}).get("driver", {})
    rules = driver.get("rules", [])
    top_level = {}
    for res in run.get("results", []):
        rid = res.get("ruleId")
        lvl = res.get("level")
        if rid and lvl in LEVEL_RANK and LEVEL_RANK[lvl] >= LEVEL_RANK.get(top_level.get(rid), -1):
            top_level[rid] = lvl

    updated = 0
    for rule in rules:
        props = rule.setdefault("properties", {})
        tags = props.setdefault("tags", [])
        if "security" not in tags:
            tags.append("security")
        if has_score(props):
            continue
        severity = (props.get("problem") or {}).get("severity")
        if severity not in SEVERITY_SCORE:
            lvl = top_level.get(rule.get("id")) or (rule.get("defaultConfiguration") or {}).get("level")
            severity = LEVEL_SEVERITY.get(lvl, "medium")
        score = SEVERITY_SCORE[severity]
        props["security-severity"] = str(score)
        rule.setdefault("defaultConfiguration", {})["level"] = score_to_level(score)
        updated += 1
    return len(rules), updated


def main(paths):
    for path in paths:
        with open(path) as f:
            sarif = json.load(f)
        total = updated = 0
        for run in sarif.get("runs", []):
            t, u = process_run(run)
            total += t
            updated += u
        with open(path, "w") as f:
            json.dump(sarif, f)
        print(f"{path}: {updated}/{total} rules given a security-severity")


if __name__ == "__main__":
    main(sys.argv[1:])
