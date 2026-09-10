#!/usr/bin/env python3
"""Build the static HTML review dashboard for the three paper variants."""

from __future__ import annotations

from pathlib import Path


HERE = Path(__file__).resolve().parent

PDFS = {
    "master": "variant-master-table.pdf",
    "narrative": "variant-narrative-gallery.pdf",
    "audit": "variant-audit-checklist.pdf",
}

PAGES = {
    "master": 10,
    "narrative": 11,
    "audit": 10,
}


def check_assets() -> None:
    for key, pdf in PDFS.items():
        pdf_path = HERE / pdf
        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)
        print(f"found {pdf}: {pdf_path.stat().st_size // 1024} KB")
        for page in range(1, PAGES[key] + 1):
            image = HERE / "pages" / key / f"page-{page:02d}.png"
            if not image.exists():
                raise FileNotFoundError(image)
        print(f"found {PAGES[key]} rendered pages for {key}")


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paper variant review - cost sampling</title>
<style>
  :root {
    --bg: #f4f6f8;
    --panel: #ffffff;
    --ink: #202a37;
    --muted: #667085;
    --line: #d9e0e8;
    --dark: #111827;
    --master: #2563eb;
    --narrative: #059669;
    --audit: #c026d3;
    --shared: #b45309;
    --hit: #fff7db;
    --hit-line: #f1c75b;
    --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; min-height: 100%; }
  body {
    font-family: var(--sans);
    color: var(--ink);
    background: var(--bg);
    font-size: 14px;
    line-height: 1.45;
  }
  header {
    background: var(--dark);
    color: #fff;
    padding: 16px 20px 14px;
  }
  h1 { margin: 0; font-size: 19px; letter-spacing: .1px; }
  header p { margin: 5px 0 0; color: #cbd5e1; font-size: 12.5px; max-width: 1160px; }
  .badges { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 10px; }
  .badge {
    font-size: 11px;
    color: #dbe4ef;
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 999px;
    padding: 2px 8px;
  }
  .toolbar {
    position: sticky;
    top: 0;
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    background: var(--panel);
    border-bottom: 1px solid var(--line);
    box-shadow: 0 1px 2px rgba(15, 23, 42, .05);
  }
  .toolbar .group { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
  .toolbar .label {
    margin-right: 2px;
    color: var(--muted);
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: .5px;
  }
  .toolbar .spacer { flex: 1; }
  .hint { color: var(--muted); font-size: 11.5px; }
  button, .open-link {
    font: inherit;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: #fff;
    color: var(--ink);
    padding: 5px 10px;
    cursor: pointer;
    text-decoration: none;
  }
  button:hover, .open-link:hover { background: #f1f5f9; }
  button.active { background: var(--dark); color: #fff; border-color: var(--dark); }
  .layout {
    display: grid;
    grid-template-columns: 360px minmax(0, 1fr);
    min-height: calc(100vh - 110px);
  }
  aside {
    position: sticky;
    top: 48px;
    height: calc(100vh - 48px);
    overflow: auto;
    background: var(--panel);
    border-right: 1px solid var(--line);
    padding: 14px;
  }
  aside h2 {
    margin: 4px 0 8px;
    color: var(--muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .6px;
  }
  .legend { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px; }
  .chip {
    display: inline-flex;
    gap: 6px;
    align-items: center;
    border: 1px solid var(--line);
    border-radius: 999px;
    background: #fbfcfe;
    color: #334155;
    font-size: 10.5px;
    padding: 2px 8px;
  }
  .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
  .dot.master { background: var(--master); }
  .dot.narrative { background: var(--narrative); }
  .dot.audit { background: var(--audit); }
  .dot.shared { background: var(--shared); }
  .subhead {
    margin: 15px 0 7px;
    color: var(--muted);
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: .6px;
  }
  .feature {
    width: 100%;
    text-align: left;
    display: block;
    margin: 0 0 8px;
    padding: 10px;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: #fff;
    transition: border-color .15s, box-shadow .15s, background .15s;
  }
  .feature:hover {
    border-color: #b9c3d0;
    box-shadow: 0 3px 11px rgba(15, 23, 42, .08);
  }
  .feature.selected {
    border-color: var(--dark);
    background: #fbfcff;
    box-shadow: 0 3px 14px rgba(15, 23, 42, .14);
  }
  .feature .title {
    display: flex;
    align-items: center;
    gap: 7px;
    font-weight: 700;
    font-size: 13px;
  }
  .kind {
    color: #fff;
    border-radius: 999px;
    padding: 1px 6px;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .5px;
  }
  .kind.distinct { background: #4338ca; }
  .kind.shared { background: var(--shared); }
  .feature .desc { color: var(--muted); font-size: 12px; margin-top: 5px; }
  .pages { display: flex; gap: 5px; flex-wrap: wrap; margin-top: 7px; }
  .pill {
    border: 1px solid var(--line);
    background: #fbfcfe;
    border-radius: 7px;
    padding: 1px 7px;
    font-size: 10.5px;
    color: #344054;
  }
  .pill.master { border-color: #b9cdfd; }
  .pill.narrative { border-color: #a7e6cf; }
  .pill.audit { border-color: #ecc3f4; }
  main { min-width: 0; }
  .columns {
    display: flex;
    gap: 10px;
    padding: 10px;
  }
  .columns.focus .column { display: none; }
  .columns.focus-master #col-master,
  .columns.focus-narrative #col-narrative,
  .columns.focus-audit #col-audit { display: flex; }
  .column {
    min-width: 0;
    flex: 1 1 0;
    display: flex;
    flex-direction: column;
    background: #fff;
    border: 1px solid var(--line);
    border-radius: 13px;
    overflow: hidden;
  }
  .column.master { border-top: 4px solid var(--master); }
  .column.narrative { border-top: 4px solid var(--narrative); }
  .column.audit { border-top: 4px solid var(--audit); }
  .column-head {
    padding: 10px 11px;
    border-bottom: 1px solid var(--line);
    min-height: 94px;
  }
  .variant-name { display: flex; align-items: center; gap: 7px; font-size: 13px; font-weight: 800; }
  .swatch { width: 10px; height: 10px; border-radius: 3px; }
  .master .swatch { background: var(--master); }
  .narrative .swatch { background: var(--narrative); }
  .audit .swatch { background: var(--audit); }
  .variant-subtitle { color: var(--muted); font-size: 11px; margin-top: 3px; line-height: 1.3; }
  .variant-meta { color: #8a93a1; font-size: 10.5px; margin-top: 4px; }
  .banner {
    border-bottom: 1px solid var(--line);
    background: #fbfcfe;
    color: var(--muted);
    font-size: 11.5px;
    padding: 6px 10px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .banner.hit {
    background: var(--hit);
    color: #76540e;
    border-bottom-color: var(--hit-line);
    font-weight: 700;
  }
  .page-scroll {
    height: calc(100vh - 265px);
    min-height: 560px;
    overflow: auto;
    background: #e8edf3;
    padding: 12px;
  }
  .page-wrap {
    position: relative;
    width: min(100%, 900px);
    margin: 0 auto;
    background: #fff;
    box-shadow: 0 1px 5px rgba(15, 23, 42, .18);
  }
  .page-img { display: block; width: 100%; height: auto; }
  .mark {
    position: absolute;
    border: 3px solid var(--hit-line);
    background: rgba(255, 247, 219, .18);
    box-shadow: 0 0 0 1px rgba(118, 84, 14, .2);
    pointer-events: none;
  }
  .mark-label {
    position: absolute;
    left: -3px;
    top: -28px;
    max-width: 92%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    background: #111827;
    color: #fff;
    border-radius: 7px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 700;
  }
  .matrix {
    margin: 0 10px 16px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 13px;
    overflow: hidden;
  }
  .matrix h2 { margin: 0; padding: 12px 14px; font-size: 14px; border-bottom: 1px solid var(--line); }
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  th, td { border-bottom: 1px solid var(--line); border-right: 1px solid var(--line); padding: 8px 10px; vertical-align: top; text-align: left; }
  th:last-child, td:last-child { border-right: 0; }
  tr:last-child th, tr:last-child td { border-bottom: 0; }
  thead th { color: var(--muted); background: #f3f6fa; text-transform: uppercase; letter-spacing: .45px; font-size: 10.5px; }
  th.aspect { width: 130px; color: var(--muted); background: #fbfcfe; }
  td.master { border-top: 2px solid var(--master); }
  td.narrative { border-top: 2px solid var(--narrative); }
  td.audit { border-top: 2px solid var(--audit); }
  code { font-family: var(--mono); font-size: .95em; }
  footer { padding: 14px 18px 18px; color: var(--muted); font-size: 11.5px; }
  @media (max-width: 1180px) {
    .layout { grid-template-columns: 1fr; }
    aside { position: static; height: auto; border-right: 0; border-bottom: 1px solid var(--line); }
    .columns { flex-direction: column; }
    .page-scroll { height: 78vh; }
  }
</style>
</head>
<body>
<header>
  <h1>Paper variant review: rendered PDFs with labelled differences</h1>
  <p>
    The panes below show Poppler-rendered pages from the three compiled PDFs.
    Click a feature to jump all variants to the relevant page and highlight
    the differentiating element. Use the PDF links in each pane for the full
    native document.
  </p>
  <div class="badges">
    <span class="badge">Master table: 10 pages</span>
    <span class="badge">Narrative gallery: 11 pages, refs only on p.11</span>
    <span class="badge">Audit checklist: 10 pages</span>
    <span class="badge">Static folder, no network</span>
  </div>
</header>

<div class="toolbar">
  <div class="group">
    <span class="label">View</span>
    <button class="active" data-mode="all">3-up</button>
    <button data-mode="master">Master</button>
    <button data-mode="narrative">Narrative</button>
    <button data-mode="audit">Audit</button>
  </div>
  <div class="group">
    <span class="label">Page</span>
    <button id="prev">Prev</button>
    <button id="next">Next</button>
    <button id="reset">All p.1</button>
  </div>
  <div class="spacer"></div>
  <div class="hint">Feature cards apply per-variant page numbers and draw highlight boxes.</div>
</div>

<div class="layout">
  <aside>
    <h2>Labelled differences</h2>
    <div class="legend">
      <span class="chip"><span class="dot master"></span>master</span>
      <span class="chip"><span class="dot narrative"></span>narrative</span>
      <span class="chip"><span class="dot audit"></span>audit</span>
      <span class="chip"><span class="dot shared"></span>shared fix</span>
    </div>
    <div class="subhead">Distinct features</div>
    <div id="feature-list"></div>
    <div class="subhead">Shared review fixes</div>
    <div id="shared-list"></div>
  </aside>

  <main>
    <section class="columns" id="columns"></section>
    <section class="matrix">
      <h2>Diff matrix</h2>
      <table>
        <thead>
          <tr>
            <th class="aspect">Aspect</th>
            <th>Master-table variant</th>
            <th>Narrative-gallery variant</th>
            <th>Audit-checklist variant</th>
          </tr>
        </thead>
        <tbody id="matrix-body"></tbody>
      </table>
    </section>
  </main>
</div>

<footer>
  Generated from the three <code>codex/icse-variant-*</code> worktrees. The
  page image assets and PDFs are local files in this folder, so the dashboard
  works from <code>file://</code> without a server or network access.
</footer>

<script>
const variants = {
  master: {
    name: "Master-table",
    columnTitle: "Variant 1 - Master evidence table",
    subtitle: "Evidence-first paper: a cross-family table answers what changes when count is replaced by measured cost.",
    meta: "Branch codex/icse-variant-master-table - 10 pages",
    filename: "variant-master-table.pdf",
    pages: 10
  },
  narrative: {
    name: "Narrative-gallery",
    columnTitle: "Variant 2 - Mechanism narrative",
    subtitle: "Mechanism-first paper: the measured-cost gallery explains why the proxy fails before the aggregate synthesis.",
    meta: "Branch codex/icse-variant-narrative - 11 pages, references continue to p.11",
    filename: "variant-narrative-gallery.pdf",
    pages: 11
  },
  audit: {
    name: "Audit-checklist",
    columnTitle: "Variant 3 - Reporting audit",
    subtitle: "Methodology-first paper: an audit checklist makes the construct-validity claim directly reviewable.",
    meta: "Branch codex/icse-variant-audit - 10 pages",
    filename: "variant-audit-checklist.pdf",
    pages: 10
  }
};

const features = [
  {
    kind: "distinct",
    title: "Centerpiece feature in Results",
    desc: "Same early Results slot, three different papers: evidence table, mechanism figure, or audit checklist.",
    pages: { master: 6, narrative: 6, audit: 6 },
    labels: {
      master: "Table II: decision summary by family",
      narrative: "Figure 3: four mechanism panels",
      audit: "Table II: measured-cost audit checklist"
    },
    marks: {
      master: { x: 6, y: 26, w: 88, h: 24 },
      narrative: { x: 13, y: 29, w: 74, h: 37 },
      audit: { x: 6, y: 31, w: 88, h: 20 }
    }
  },
  {
    kind: "distinct",
    title: "How RQ2 is framed",
    desc: "The 538/1,666 decision audit is shared; the support shifts from table to mechanism to audit lens.",
    pages: { master: 6, narrative: 7, audit: 6 },
    labels: {
      master: "RQ2 begins under the family summary table",
      narrative: "RQ2 follows the mechanism gallery",
      audit: "RQ2 is tied to auditable checks"
    },
    marks: {
      master: { x: 50, y: 72, w: 43, h: 18 },
      narrative: { x: 5, y: 11, w: 90, h: 24 },
      audit: { x: 50, y: 72, w: 43, h: 18 }
    }
  },
  {
    kind: "distinct",
    title: "Validity-condition explanation",
    desc: "RQ3 reads differently depending on whether the preceding feature is a table, gallery, or audit.",
    pages: { master: 7, narrative: 7, audit: 7 },
    labels: {
      master: "regime synthesis after evidence table",
      narrative: "gallery becomes mechanism evidence",
      audit: "audit table makes RQ3 operational"
    },
    marks: {
      master: { x: 6, y: 50, w: 88, h: 28 },
      narrative: { x: 6, y: 45, w: 88, h: 30 },
      audit: { x: 6, y: 50, w: 88, h: 28 }
    }
  },
  {
    kind: "distinct",
    title: "Reviewer takeaway",
    desc: "Which one-sentence memory the paper leaves: evidence map, failure mechanisms, or reusable check.",
    pages: { master: 9, narrative: 10, audit: 9 },
    labels: {
      master: "best for big empirical map",
      narrative: "best for story clarity",
      audit: "best for actionable methodology"
    },
    marks: {
      master: { x: 6, y: 25, w: 88, h: 35 },
      narrative: { x: 6, y: 9, w: 43, h: 42 },
      audit: { x: 6, y: 25, w: 88, h: 35 }
    }
  },
  {
    kind: "distinct",
    title: "Reference footprint",
    desc: "The narrative figure costs space; its references continue to page 11, still inside the 10+2 rule.",
    pages: { master: 10, narrative: 11, audit: 10 },
    labels: {
      master: "references fit on p.10",
      narrative: "references continue on p.11",
      audit: "references fit on p.10"
    },
    marks: {
      master: { x: 6, y: 6, w: 88, h: 76 },
      narrative: { x: 6, y: 6, w: 43, h: 44 },
      audit: { x: 6, y: 6, w: 88, h: 76 }
    }
  }
];

const sharedFeatures = [
  {
    kind: "shared",
    title: "Construct-validity gap moved up front",
    desc: "The intro now states that the gap is the missing validity check for the effort axis itself.",
    pages: { master: 1, narrative: 1, audit: 1 },
    labels: { master: "shared intro fix", narrative: "shared intro fix", audit: "shared intro fix" },
    marks: {
      master: { x: 5, y: 29, w: 43, h: 28 },
      narrative: { x: 5, y: 29, w: 43, h: 28 },
      audit: { x: 5, y: 29, w: 43, h: 28 }
    }
  },
  {
    kind: "shared",
    title: "Decision audit promoted",
    desc: "The 538/1,666 number appears in the abstract/intro and at the start of RQ2.",
    pages: { master: 1, narrative: 1, audit: 1 },
    labels: { master: "shared headline number", narrative: "shared headline number", audit: "shared headline number" },
    marks: {
      master: { x: 51, y: 24, w: 43, h: 26 },
      narrative: { x: 51, y: 24, w: 43, h: 26 },
      audit: { x: 51, y: 24, w: 43, h: 26 }
    }
  },
  {
    kind: "shared",
    title: "Cost model definitions tightened",
    desc: "Normalized objective, min-max scope, Linux resource cost, and acquisition-vs-target wording are explicit.",
    pages: { master: 3, narrative: 3, audit: 3 },
    labels: { master: "shared cost model", narrative: "shared cost model", audit: "shared cost model" },
    marks: {
      master: { x: 5, y: 35, w: 90, h: 24 },
      narrative: { x: 5, y: 35, w: 90, h: 24 },
      audit: { x: 5, y: 35, w: 90, h: 24 }
    }
  },
  {
    kind: "shared",
    title: "Deployable strategies separated from oracles",
    desc: "Diagnostic cheap/expensive oracles are framed as bounds, not deployable recommendations.",
    pages: { master: 4, narrative: 4, audit: 4 },
    labels: { master: "shared strategy-panel caveat", narrative: "shared strategy-panel caveat", audit: "shared strategy-panel caveat" },
    marks: {
      master: { x: 51, y: 10, w: 43, h: 24 },
      narrative: { x: 51, y: 10, w: 43, h: 24 },
      audit: { x: 51, y: 10, w: 43, h: 24 }
    }
  },
  {
    kind: "shared",
    title: "Artifact paragraph added",
    desc: "The paper states the replayable fields needed to recompute TrainCost, Ratio, flips, and Pareto fronts.",
    pages: { master: 5, narrative: 5, audit: 5 },
    labels: { master: "shared artifact paragraph", narrative: "shared artifact paragraph", audit: "shared artifact paragraph" },
    marks: {
      master: { x: 51, y: 26, w: 43, h: 25 },
      narrative: { x: 51, y: 26, w: 43, h: 25 },
      audit: { x: 51, y: 26, w: 43, h: 25 }
    }
  },
  {
    kind: "shared",
    title: "Discussion and related work compressed",
    desc: "The ending now focuses on four claims and a tighter related-work gap.",
    pages: { master: 8, narrative: 9, audit: 8 },
    labels: { master: "shared compression", narrative: "shared compression", audit: "shared compression" },
    marks: {
      master: { x: 5, y: 47, w: 90, h: 35 },
      narrative: { x: 5, y: 25, w: 90, h: 34 },
      audit: { x: 5, y: 47, w: 90, h: 35 }
    }
  }
];

const matrixRows = [
  {
    aspect: "Best use",
    master: "Use if the paper needs to look empirically exhaustive immediately.",
    narrative: "Use if the paper needs to teach the failure modes and be easier to remember.",
    audit: "Use if the paper should sell a reusable validity-check method."
  },
  {
    aspect: "Signature object",
    master: "Table II summarizes ordering, calibration, top-choice changes, Pareto changes, and lesson for every family.",
    narrative: "Figure 3 shows same-size cost gaps, similar-MRE cost gaps, larger-sample cheaper cases, and same-budget separations.",
    audit: "Table II turns the review concerns into checks: construct, spread, calibration, decision impact, artifact trace."
  },
  {
    aspect: "Tradeoff",
    master: "Most compact and reviewer-friendly, but less visual intuition.",
    narrative: "Most explanatory, but costs one extra reference page.",
    audit: "Most actionable, but less immediately empirical than the master table."
  },
  {
    aspect: "Results opening",
    master: "Evidence table first, then RQ1/RQ2/RQ3 prose.",
    narrative: "Mechanism gallery first, then RQ1/RQ2/RQ3 prose.",
    audit: "Audit checklist first, then RQ1/RQ2/RQ3 prose."
  },
  {
    aspect: "Recommendation",
    master: "Likely safest ICSE submission if reviewers want breadth and concrete numbers.",
    narrative: "Likely best if the concern is reader intuition and story clarity.",
    audit: "Likely best if the paper should become a method/checklist contribution."
  }
];

const state = { master: 1, narrative: 1, audit: 1, feature: null };

function pagePath(key, page) {
  return `pages/${key}/page-${String(page).padStart(2, "0")}.png`;
}

function renderColumns() {
  const holder = document.getElementById("columns");
  holder.innerHTML = Object.keys(variants).map(key => {
    const v = variants[key];
    return `
      <article class="column ${key}" id="col-${key}">
        <div class="column-head">
          <div class="variant-name"><span class="swatch"></span>${v.columnTitle}</div>
          <div class="variant-subtitle">${v.subtitle}</div>
          <div class="variant-meta">${v.meta} · <a class="open-link" href="${v.filename}" target="_blank">Open PDF</a></div>
        </div>
        <div class="banner" id="banner-${key}">Rendered page 1</div>
        <div class="page-scroll" id="scroll-${key}">
          <div class="page-wrap">
            <img class="page-img" id="img-${key}" src="${pagePath(key, 1)}" alt="${v.name} page 1">
            <div class="overlay" id="overlay-${key}"></div>
          </div>
        </div>
      </article>`;
  }).join("");
}

function pagePills(feature) {
  return Object.keys(variants).map(key => {
    const page = feature.pages[key];
    return `<span class="pill ${key}"><b>${variants[key].name}</b> p.${page}</span>`;
  }).join("");
}

function renderFeatureList(list, targetId) {
  const holder = document.getElementById(targetId);
  holder.innerHTML = list.map((feature, index) => `
    <button class="feature" data-list="${targetId}" data-index="${index}">
      <div class="title"><span class="kind ${feature.kind}">${feature.kind}</span>${feature.title}</div>
      <div class="desc">${feature.desc}</div>
      <div class="pages">${pagePills(feature)}</div>
    </button>
  `).join("");
}

function renderMatrix() {
  const body = document.getElementById("matrix-body");
  body.innerHTML = matrixRows.map(row => `
    <tr>
      <th class="aspect">${row.aspect}</th>
      <td class="master">${row.master}</td>
      <td class="narrative">${row.narrative}</td>
      <td class="audit">${row.audit}</td>
    </tr>
  `).join("");
}

function clearMark(key) {
  document.getElementById("overlay-" + key).innerHTML = "";
}

function drawMark(key, rect, label) {
  const overlay = document.getElementById("overlay-" + key);
  overlay.innerHTML = "";
  if (!rect) return;
  const mark = document.createElement("div");
  mark.className = "mark";
  mark.style.left = rect.x + "%";
  mark.style.top = rect.y + "%";
  mark.style.width = rect.w + "%";
  mark.style.height = rect.h + "%";
  mark.innerHTML = `<div class="mark-label">${label}</div>`;
  overlay.appendChild(mark);
}

function setPage(key, page, label, mark) {
  const safePage = Math.max(1, Math.min(page, variants[key].pages));
  state[key] = safePage;
  const img = document.getElementById("img-" + key);
  img.src = pagePath(key, safePage);
  img.alt = `${variants[key].name} page ${safePage}`;
  const banner = document.getElementById("banner-" + key);
  banner.textContent = `${variants[key].name}: p.${safePage} - ${label || "rendered page"}`;
  banner.className = label ? "banner hit" : "banner";
  drawMark(key, mark, label || `Page ${safePage}`);
  document.getElementById("scroll-" + key).scrollTop = 0;
}

function selectFeature(feature, button) {
  state.feature = feature;
  document.querySelectorAll(".feature").forEach(el => el.classList.remove("selected"));
  button.classList.add("selected");
  Object.keys(variants).forEach(key => {
    setPage(key, feature.pages[key], feature.labels[key] || feature.title, feature.marks[key]);
  });
}

function turnPage(delta) {
  state.feature = null;
  document.querySelectorAll(".feature").forEach(el => el.classList.remove("selected"));
  Object.keys(variants).forEach(key => {
    clearMark(key);
    setPage(key, state[key] + delta, null, null);
  });
}

function resetPages() {
  state.feature = null;
  document.querySelectorAll(".feature").forEach(el => el.classList.remove("selected"));
  Object.keys(variants).forEach(key => setPage(key, 1, null, null));
}

function wireFeatures() {
  document.querySelectorAll(".feature").forEach(button => {
    button.addEventListener("click", () => {
      const list = button.dataset.list === "feature-list" ? features : sharedFeatures;
      selectFeature(list[Number(button.dataset.index)], button);
    });
  });
}

function wireToolbar() {
  document.querySelectorAll("[data-mode]").forEach(button => {
    button.addEventListener("click", () => {
      document.querySelectorAll("[data-mode]").forEach(el => el.classList.remove("active"));
      button.classList.add("active");
      const mode = button.dataset.mode;
      const columns = document.getElementById("columns");
      columns.className = "columns" + (mode === "all" ? "" : " focus focus-" + mode);
    });
  });
  document.getElementById("prev").addEventListener("click", () => turnPage(-1));
  document.getElementById("next").addEventListener("click", () => turnPage(1));
  document.getElementById("reset").addEventListener("click", resetPages);
}

renderColumns();
renderFeatureList(features, "feature-list");
renderFeatureList(sharedFeatures, "shared-list");
renderMatrix();
wireFeatures();
wireToolbar();
</script>
</body>
</html>
"""


def main() -> None:
    check_assets()
    out = HERE / "index.html"
    out.write_text(HTML, encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
