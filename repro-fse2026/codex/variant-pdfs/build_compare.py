#!/usr/bin/env python3
"""Build a standalone HTML tool to compare the three ICSE paper variants.

Every page of every variant is rendered to a grayscale PNG (PyMuPDF) and
embedded as base64, so the page is fully self-contained, works offline, and
needs no PDF plugin. Two modes:

  * Browse   : three columns of page images; click a feature to jump+flash it.
  * Pixel diff: pick a pair of variants; per page index it shows A | diff | B,
               with the diff computed in-browser (red/cyan overlay, or
               "highlight changed regions" with an adjustable threshold) and a
               %-changed figure. Note: prose reflows between variants, so the
               diff shows both genuine content changes (titles, abstracts,
               tables/boxes) and shifted-but-identical text.

Run:  python3 build_compare.py    Out:  compare-variants.html
"""
import base64, io, json, pathlib
import fitz
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
FILES = {
    "validity": "variant1-construct-validity.pdf",
    "decision": "variant2-decision-impact-master-table.pdf",
    "audit":    "variant3-cost-proxy-audit.pdf",
}
ZOOM = 1.4

def render(path):
    out = []
    for pg in fitz.open(path):
        pix = pg.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), alpha=False, colorspace=fitz.csGRAY)
        im = Image.frombytes("L", [pix.width, pix.height], pix.samples)
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        out.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    return out

PAGES = {}
for k, f in FILES.items():
    PAGES[k] = render(HERE / f)
    print(f"  {f}: {len(PAGES[k])} pages")
total = sum(len(s) for v in PAGES.values() for s in v)
print(f"  embedded image base64 total ~{total//1024} KB")

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ICSE 2027 paper — variant comparison &amp; pixel diff</title>
<style>
  :root{
    --v:#2563eb; --d:#16a34a; --a:#db2777; --shared:#b45309;
    --bg:#f5f6f8; --panel:#ffffff; --ink:#1c2430; --muted:#5b6675; --line:#e2e6ec;
    --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{font-family:var(--sans);color:var(--ink);background:var(--bg);font-size:14px;line-height:1.45}
  header.top{padding:13px 20px;background:#0f172a;color:#fff}
  header.top h1{margin:0 0 3px;font-size:18px}
  header.top p{margin:0;color:#aeb8c7;font-size:12.5px}
  header.top .badges{margin-top:7px;display:flex;gap:8px;flex-wrap:wrap}
  .badge{font-size:11px;padding:2px 8px;border-radius:999px;background:#1e293b;color:#cbd5e1;border:1px solid #334155}
  .toolbar{position:sticky;top:0;z-index:30;display:flex;gap:10px;align-items:center;flex-wrap:wrap;
           padding:8px 16px;background:var(--panel);border-bottom:1px solid var(--line)}
  .toolbar .grp{display:flex;gap:6px;align-items:center}
  .toolbar .lab{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;margin-right:2px}
  .toolbar .sep{width:1px;height:22px;background:var(--line)}
  button.btn{font:inherit;font-size:12.5px;padding:5px 11px;border:1px solid var(--line);background:#fff;border-radius:7px;cursor:pointer;color:var(--ink)}
  button.btn:hover{background:#f0f3f7}
  button.btn.on{background:#0f172a;color:#fff;border-color:#0f172a}
  button.btn.v.on{background:var(--v);border-color:var(--v)} button.btn.d.on{background:var(--d);border-color:var(--d)} button.btn.a.on{background:var(--a);border-color:var(--a)}
  .toolbar input[type=range]{width:120px}
  .toolbar .spacer{flex:1}
  .toolbar .hint{font-size:11.5px;color:var(--muted)}
  .hidden{display:none !important}

  .layout{display:grid;grid-template-columns:330px 1fr;align-items:start}
  aside.side{position:sticky;top:49px;align-self:start;height:calc(100vh - 49px);overflow:auto;
             padding:13px;background:var(--panel);border-right:1px solid var(--line)}
  aside.side h2{font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);margin:4px 0 8px}
  .legend{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
  .chip{display:inline-flex;align-items:center;gap:6px;font-size:11px;padding:2px 8px;border-radius:999px;border:1px solid var(--line);background:#fbfcfe}
  .dot{width:9px;height:9px;border-radius:50%}
  .dot.v{background:var(--v)} .dot.d{background:var(--d)} .dot.a{background:var(--a)} .dot.s{background:var(--shared)}
  .feat{display:block;width:100%;text-align:left;border:1px solid var(--line);background:#fff;border-radius:10px;padding:9px 10px;margin-bottom:8px;cursor:pointer}
  .feat:hover{border-color:#c7d0db;box-shadow:0 2px 8px rgba(20,30,50,.06)}
  .feat.active{border-color:#0f172a;box-shadow:0 2px 10px rgba(20,30,50,.12)}
  .feat .ttl{font-weight:650;font-size:13px;display:flex;align-items:center;gap:7px}
  .feat .kind{font-size:9.5px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:1px 6px;border-radius:999px;color:#fff}
  .feat .kind.distinct{background:#4338ca} .feat .kind.shared{background:var(--shared)}
  .feat .desc{color:var(--muted);font-size:12px;margin:5px 0 6px}
  .feat .pv{display:flex;gap:5px;flex-wrap:wrap}
  .feat .pvi{font-size:10.5px;padding:1px 7px;border-radius:6px;border:1px solid var(--line);background:#fbfcfe;color:#374151}
  .feat .pvi.na{color:#9aa3af;text-decoration:line-through}
  .side .sub{font-size:11px;color:var(--muted);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.6px}

  /* Browse */
  .cols{display:flex;gap:10px;padding:10px}
  .col{flex:1 1 0;min-width:0;display:flex;flex-direction:column;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fff}
  .col .chead{padding:8px 11px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:6px}
  .col .chead .nm{font-weight:700;font-size:12.5px;display:flex;align-items:center;gap:7px}
  .col .chead .nm .sw{width:10px;height:10px;border-radius:3px}
  .col .chead a{font-size:11px;color:var(--muted);text-decoration:none;white-space:nowrap}
  .col .chead a:hover{color:var(--ink);text-decoration:underline}
  .col#col-validity{border-top:3px solid var(--v)} .col#col-validity .sw{background:var(--v)}
  .col#col-decision{border-top:3px solid var(--d)} .col#col-decision .sw{background:var(--d)}
  .col#col-audit{border-top:3px solid var(--a)}    .col#col-audit .sw{background:var(--a)}
  .scroller{position:relative;overflow:auto;height:calc(100vh - 49px - 86px);background:#eceef2;padding:10px}
  .pagewrap{position:relative;margin:0 auto 10px;width:100%;box-shadow:0 1px 5px rgba(20,30,50,.14);border-radius:2px;background:#fff}
  .pagewrap img{display:block;width:100%;height:auto;border-radius:2px}
  .pagewrap .pgno{position:absolute;right:6px;bottom:5px;font:600 10px/1 var(--mono);color:#94a3b8;background:#ffffffcc;padding:2px 5px;border-radius:5px}
  .pagewrap .ribbon{position:absolute;left:7px;top:7px;right:7px;font-size:11px;font-weight:650;color:#fff;padding:4px 8px;border-radius:7px;box-shadow:0 1px 4px rgba(0,0,0,.25);pointer-events:none}
  #col-validity .ribbon{background:var(--v)} #col-decision .ribbon{background:var(--d)} #col-audit .ribbon{background:var(--a)}
  .pagewrap.flash{animation:flash 1.7s ease}
  @keyframes flash{0%,55%{box-shadow:0 0 0 3px #f59e0b,0 1px 5px rgba(20,30,50,.14)}100%{box-shadow:0 1px 5px rgba(20,30,50,.14)}}

  /* Diff */
  #diff{padding:10px}
  .dnote{font-size:12px;color:var(--muted);background:#fbfcfe;border:1px solid var(--line);border-radius:8px;padding:8px 11px;margin-bottom:10px}
  .dnote b{color:var(--ink)}
  .drow{border:1px solid var(--line);border-radius:10px;background:#fff;margin-bottom:12px;overflow:hidden}
  .drow .dhead{display:flex;align-items:center;gap:10px;padding:6px 10px;border-bottom:1px solid var(--line);background:#fbfcfe;font-size:12px}
  .drow .dhead .pg{font-weight:700}
  .drow .dhead .pct{font:600 12px/1 var(--mono);padding:2px 7px;border-radius:6px;background:#eef2f7;color:#334155}
  .drow .dhead .pct.hi{background:#fdecef;color:#b4324a}
  .dgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;padding:8px}
  .dcell{display:flex;flex-direction:column}
  .dcell .cap{font-size:10.5px;color:var(--muted);text-align:center;margin-bottom:4px;text-transform:uppercase;letter-spacing:.4px}
  .dcell .cap.A{color:var(--cA)} .dcell .cap.B{color:var(--cB)}
  .dcell img,.dcell canvas{width:100%;height:auto;border:1px solid var(--line);border-radius:3px;background:#fff;display:block}
  .dcell.empty{display:flex;align-items:center;justify-content:center;min-height:120px;color:#9aa3af;font-size:12px;border:1px dashed var(--line);border-radius:6px}

  section.matrix{padding:18px;border-top:1px solid var(--line);background:var(--panel)}
  section.matrix h2{font-size:14px;margin:0 0 10px}
  table.mx{width:100%;border-collapse:collapse;font-size:12px}
  table.mx th,table.mx td{border:1px solid var(--line);padding:8px 9px;vertical-align:top;text-align:left}
  table.mx thead th{background:#f3f5f8;font-size:11px;text-transform:uppercase;letter-spacing:.4px}
  table.mx th.aspect{width:120px;background:#fbfcfe;color:var(--muted);font-weight:650}
  table.mx td.v{border-top:2px solid var(--v)} table.mx td.d{border-top:2px solid var(--d)} table.mx td.a{border-top:2px solid var(--a)}
  table.mx .em{color:#9aa3af;font-style:italic}
  footer.ft{padding:14px 18px;color:var(--muted);font-size:11.5px;border-top:1px solid var(--line);background:var(--bg)}
  @media (max-width:1080px){ .layout{grid-template-columns:1fr} aside.side{position:static;height:auto} .cols{flex-direction:column} .scroller{height:70vh} }
</style>
</head>
<body>
<header class="top">
  <h1>Sample Size &ne; Sampling Cost — three ICSE&nbsp;2027 variants: compare &amp; pixel-diff</h1>
  <p>Each variant applies <b>all</b> the review's universal fixes; they differ only in their headline <b>feature</b>. Original draft: 12&nbsp;pp (spilled to p.11, non-compliant).</p>
  <div class="badges">
    <span class="badge">V1 Construct-Validity · 10&nbsp;pp main</span>
    <span class="badge">V2 Decision-Impact · 10&nbsp;pp main</span>
    <span class="badge">V3 Cost-Proxy Audit · 10&nbsp;pp main</span>
  </div>
</header>

<div class="toolbar">
  <div class="grp"><span class="lab">Mode</span>
    <button class="btn on" id="mBrowse">Browse</button>
    <button class="btn" id="mDiff">Pixel diff</button>
  </div>
  <span class="sep"></span>
  <div class="grp" id="browseCtl"><span class="lab">View</span>
    <button class="btn on" data-mode="all">3-up</button>
    <button class="btn" data-mode="validity">V1</button>
    <button class="btn" data-mode="decision">V2</button>
    <button class="btn" data-mode="audit">V3</button>
  </div>
  <div class="grp hidden" id="diffCtl">
    <span class="lab">Pair</span>
    <button class="btn" data-pair="validity,decision">V1 &harr; V2</button>
    <button class="btn" data-pair="validity,audit">V1 &harr; V3</button>
    <button class="btn" data-pair="decision,audit">V2 &harr; V3</button>
    <span class="sep"></span>
    <span class="lab">Diff</span>
    <button class="btn on" data-style="overlay">Overlay (A red / B cyan)</button>
    <button class="btn" data-style="highlight">Highlight changes</button>
    <span class="sep"></span>
    <span class="lab">Thresh</span>
    <input type="range" id="thr" min="0" max="120" value="34"><span id="thrv" style="font:600 11px var(--mono);width:24px">34</span>
  </div>
  <div class="spacer"></div>
  <div class="hint" id="hint">Click a feature on the left to jump &amp; flash it.</div>
</div>

<main class="layout">
  <aside class="side">
    <h2>Differences by feature</h2>
    <div class="legend">
      <span class="chip"><span class="dot v"></span>V1</span>
      <span class="chip"><span class="dot d"></span>V2</span>
      <span class="chip"><span class="dot a"></span>V3</span>
      <span class="chip"><span class="dot s"></span>shared fix</span>
    </div>
    <div class="sub">Distinct features</div>
    <button class="feat" data-v="1" data-d="1" data-a="1"><div class="ttl"><span class="kind distinct">distinct</span>Title &amp; framing</div><div class="desc">One-line identity of each variant.</div><div class="pv"><span class="pvi">V1 validity·p1</span><span class="pvi">V2 misprices·p1</span><span class="pvi">V3 auditing·p1</span></div></button>
    <button class="feat" data-v="1" data-d="1" data-a="1"><div class="ttl"><span class="kind distinct">distinct</span>Abstract angle</div><div class="desc">How the pitch is framed.</div><div class="pv"><span class="pvi">V1 proxy valid?</span><span class="pvi">V2 price right?</span><span class="pvi">V3 when+how check</span></div></button>
    <button class="feat" data-v="2" data-d="2" data-a="2"><div class="ttl"><span class="kind distinct">distinct</span>Lead contribution</div><div class="desc">Which bullet comes first.</div><div class="pv"><span class="pvi">V1 formalize threat</span><span class="pvi">V2 538/1,666+table</span><span class="pvi">V3 derive audit</span></div></button>
    <button class="feat" data-v="9" data-d="6" data-a="9"><div class="ttl"><span class="kind distinct">distinct</span>&#9733; Centerpiece artifact</div><div class="desc">The signature element of each.</div><div class="pv"><span class="pvi">V1 claims table·p9</span><span class="pvi">V2 master table·p6</span><span class="pvi">V3 audit box·p9</span></div></button>
    <button class="feat" data-v="7" data-d="6" data-a="6"><div class="ttl"><span class="kind shared">added</span>RQ1 evidence figures</div><div class="desc">Cost-spread (CV, p90/p10) + same-n strategy-bias heatmap — added to fill the 10th page.</div><div class="pv"><span class="pvi">V1 p7</span><span class="pvi">V2 p6</span><span class="pvi">V3 p6</span></div></button>
    <button class="feat" data-v="6" data-d="0" data-a="0"><div class="ttl"><span class="kind distinct">distinct</span>Mechanism gallery</div><div class="desc">4-panel figure: kept or replaced.</div><div class="pv"><span class="pvi">V1 kept·p6</span><span class="pvi na">V2 removed</span><span class="pvi na">V3 removed</span></div></button>
    <button class="feat" data-v="10" data-d="10" data-a="10"><div class="ttl"><span class="kind distinct">distinct</span>Conclusion emphasis</div><div class="desc">Closing framing word.</div><div class="pv"><span class="pvi">V1 validity warn</span><span class="pvi">V2 validity warn</span><span class="pvi">V3 names Audit</span></div></button>
    <div class="sub">Shared review fixes</div>
    <button class="feat" data-v="1" data-d="1" data-a="1"><div class="ttl"><span class="kind shared">shared</span>Gap moved to intro front</div></button>
    <button class="feat" data-v="7" data-d="6" data-a="7"><div class="ttl"><span class="kind shared">shared</span>538/1,666 promoted</div></button>
    <button class="feat" data-v="3" data-d="3" data-a="3"><div class="ttl"><span class="kind shared">shared</span>Exact normalization def.</div></button>
    <button class="feat" data-v="3" data-d="3" data-a="3"><div class="ttl"><span class="kind shared">shared</span>Deployable vs. oracle</div></button>
    <button class="feat" data-v="3" data-d="3" data-a="3"><div class="ttl"><span class="kind shared">shared</span>Acquisition vs. resource cost</div></button>
    <button class="feat" data-v="8" data-d="7" data-a="8"><div class="ttl"><span class="kind shared">shared</span>Discussion&rarr;4 msgs · RW reordered</div></button>
    <span class="chip" style="margin-top:6px"><span class="dot s"></span>+ 10-page compression · reference pass (32 refs)</span>
  </aside>

  <section id="content">
    <div class="cols" id="browse">
      <div class="col" id="col-validity">
        <div class="chead"><div class="nm"><span class="sw"></span>V1 · Construct-Validity</div><a href="variant1-construct-validity.pdf" target="_blank">open PDF &#8599;</a></div>
        <div class="scroller" id="sc-validity"></div>
      </div>
      <div class="col" id="col-decision">
        <div class="chead"><div class="nm"><span class="sw"></span>V2 · Decision-Impact</div><a href="variant2-decision-impact-master-table.pdf" target="_blank">open PDF &#8599;</a></div>
        <div class="scroller" id="sc-decision"></div>
      </div>
      <div class="col" id="col-audit">
        <div class="chead"><div class="nm"><span class="sw"></span>V3 · Cost-Proxy Audit</div><a href="variant3-cost-proxy-audit.pdf" target="_blank">open PDF &#8599;</a></div>
        <div class="scroller" id="sc-audit"></div>
      </div>
    </div>

    <div id="diff" class="hidden">
      <div class="dnote"><b>Reading the diff.</b> Pages are aligned by number. The three variants share most body text but it <b>reflows</b> (different intro/abstract lengths), so a diff mixes <b>genuine content changes</b> (titles, abstracts, the centerpiece table/box) with <b>shifted-but-identical text</b>. In <b>Overlay</b>, ink unique to A is <span style="color:#c00">red</span>, unique to B is <span style="color:#0aa">cyan</span>, shared ink is dark. In <b>Highlight</b>, changed pixels are <span style="color:#b4324a">crimson</span> over a faded page. The %-changed figure counts pixels differing by more than the threshold.</div>
      <div id="diffRows"></div>
    </div>
  </section>
</main>

<section class="matrix">
  <h2>Diff matrix — the actual differing text</h2>
  <table class="mx">
    <thead><tr><th class="aspect">Aspect</th><th>V1 · Construct-Validity</th><th>V2 · Decision-Impact</th><th>V3 · Cost-Proxy Audit</th></tr></thead>
    <tbody>
      <tr><th class="aspect">Title</th>
        <td class="v">Sample Size Is Not Sampling Cost: <b>A Validity Study</b> of Performance Prediction for Configurable Systems</td>
        <td class="d">When Sample Size <b>Misprices</b> Sampling Cost in Configurable-System Performance Prediction</td>
        <td class="a"><b>Auditing the Effort Axis</b>: A Cost-Proxy Check for Sampling-Based Performance Prediction of Configurable Systems</td></tr>
      <tr><th class="aspect">Abstract opener</th>
        <td class="v">&ldquo;&hellip;a proxy for acquisition cost. <b>We test whether that proxy is valid.</b>&rdquo;</td>
        <td class="d">&ldquo;&hellip;which silently <b>prices</b> acquisition effort&hellip; <b>We ask whether that price is right.</b>&rdquo;</td>
        <td class="a">&ldquo;<b>When is that proxy safe, and how should authors check? We answer both.</b> &hellip;a three-step Cost-Proxy Audit&hellip;&rdquo;</td></tr>
      <tr><th class="aspect">Lead contribution</th>
        <td class="v">&ldquo;We <b>identify and formalize a construct-validity threat</b>&hellip;&rdquo;</td>
        <td class="d">&ldquo;We <b>quantify the decision impact</b>&hellip;538/1,666&hellip; a cross-family table (<b>Table&nbsp;II</b>)&hellip;&rdquo;</td>
        <td class="a">&ldquo;We <b>derive the Cost-Proxy Audit</b>: a three-step check + reporting checklist&hellip;&rdquo;</td></tr>
      <tr><th class="aspect">Centerpiece</th>
        <td class="v"><b>Table&nbsp;II &mdash; &ldquo;three cost claims&rdquo;</b> (Discussion, &asymp; p.8).</td>
        <td class="d"><b>Table&nbsp;II &mdash; master &ldquo;what changes&rdquo;</b> (Results, &asymp; p.6).</td>
        <td class="a"><b>Boxed 3-step &ldquo;Cost-Proxy Audit&rdquo;</b> + checklist (Discussion, &asymp; p.8).</td></tr>
      <tr><th class="aspect">Mechanism gallery</th>
        <td class="v">Kept (&asymp; p.6).</td><td class="d"><b>Removed</b> &rarr; replaced by master table.</td><td class="a"><b>Removed</b> &rarr; described in prose.</td></tr>
      <tr><th class="aspect">RQ1 evidence (added)</th><td class="v" colspan="3" style="border-top:none">Two new figures in all three: per-configuration cost spread (CV, $p_{90}/p_{10}$) and the same-$n$ strategy-bias heatmap &mdash; added so each paper fills the full 10th page.</td></tr>
      <tr><th class="aspect">Pages</th><td class="v">10 main + refs</td><td class="d">10 main + refs</td><td class="a">10 main + refs</td></tr>
      <tr><th class="aspect">Shared fixes</th><td class="v" colspan="3" style="border-top:none"><span class="em">Identical in all three:</span> 10-page compression · gap up front · 538/1,666 in abstract+intro+RQ2 · acquisition-vs-resource (Linux) · deployable-vs-oracle · exact min&ndash;max normalization · artifact paragraph · Discussion&rarr;4 messages · Related-Work reordered &amp; cut ~35% · reference pass (32 refs).</td></tr>
    </tbody>
  </table>
</section>
<footer class="ft">Self-contained: every page is an embedded grayscale image; the pixel diff is computed in your browser. &ldquo;open PDF&rdquo; links use the sibling PDF files. Branches <code>variant/validity</code> · <code>variant/decision</code> · <code>variant/audit</code>.</footer>

<script>
__PAGES_DATA__
var KEYS=["validity","decision","audit"];
var TAG={validity:"V1",decision:"V2",audit:"V3"};
var ACC={validity:"#2563eb",decision:"#16a34a",audit:"#db2777"};
var ANNOT={
  validity:{1:"Title & abstract — validity framing",6:"Mechanism gallery (kept)",7:"RQ1 evidence — cost spread & strategy-bias (added)",9:"◆ Centerpiece — Three cost claims table"},
  decision:{1:"Title & abstract — decision framing",6:"◆ Centerpiece — master what-changes table"},
  audit:{1:"Title & abstract — audit framing",6:"RQ1 evidence — cost spread & strategy-bias (added)",9:"◆ Centerpiece — Cost-Proxy Audit box"}
};
function el(t,c){var e=document.createElement(t);if(c)e.className=c;return e;}
function src(k,i){return "data:image/png;base64,"+PAGES[k][i-1];}

/* ---------- Browse ---------- */
function buildBrowse(){
  KEYS.forEach(function(k){
    var sc=document.getElementById("sc-"+k); sc.innerHTML="";
    for(var p=1;p<=PAGES[k].length;p++){
      var w=el("div","pagewrap"); w.dataset.page=p;
      var im=el("img"); im.loading="lazy"; im.src=src(k,p); im.alt=TAG[k]+" page "+p; w.appendChild(im);
      var n=el("div","pgno"); n.textContent="p."+p; w.appendChild(n);
      if(ANNOT[k]&&ANNOT[k][p]){var r=el("div","ribbon");r.textContent=ANNOT[k][p];w.appendChild(r);}
      sc.appendChild(w);
    }
  });
}
function jump(k,p){
  if(!p)return;
  var sc=document.getElementById("sc-"+k), w=sc.querySelector(".pagewrap[data-page='"+p+"']");
  if(!w)return;
  sc.scrollTo({top:w.offsetTop-8,behavior:"smooth"});
  w.classList.remove("flash"); void w.offsetWidth; w.classList.add("flash");
}

/* ---------- Pixel diff ---------- */
var IMG={};
function getImg(k,i){var key=k+":"+i; if(IMG[key])return IMG[key];
  IMG[key]=new Promise(function(res,rej){var im=new Image();im.onload=function(){res(im);};im.onerror=rej;im.src=src(k,i);});
  return IMG[key];}
var PAIR=["validity","decision"], STYLE="overlay", THR=34;
function lum(d,o){return 0.299*d[o]+0.587*d[o+1]+0.114*d[o+2];}
function diffTo(canvas,ia,ib){
  var w=Math.min(ia.naturalWidth,ib.naturalWidth), h=Math.min(ia.naturalHeight,ib.naturalHeight);
  var ca=el("canvas");ca.width=w;ca.height=h;var xa=ca.getContext("2d");xa.drawImage(ia,0,0);
  var cb=el("canvas");cb.width=w;cb.height=h;var xb=cb.getContext("2d");xb.drawImage(ib,0,0);
  var A=xa.getImageData(0,0,w,h).data, B=xb.getImageData(0,0,w,h).data;
  canvas.width=w;canvas.height=h;var cx=canvas.getContext("2d");var out=cx.createImageData(w,h),o=out.data;
  var changed=0,tot=w*h;
  for(var i=0;i<A.length;i+=4){
    var la=lum(A,i),lb=lum(B,i),dd=Math.abs(la-lb);
    if(dd>THR)changed++;
    if(STYLE==="overlay"){var ad=255-la,bd=255-lb;o[i]=255-bd;o[i+1]=255-ad;o[i+2]=255-ad;o[i+3]=255;}
    else{ if(dd>THR){o[i]=200;o[i+1]=24;o[i+2]=60;o[i+3]=255;}
          else{var g=255-(255-la)*0.22;o[i]=g;o[i+1]=g;o[i+2]=g;o[i+3]=255;} }
  }
  cx.putImageData(out,0,0);
  return changed/tot;
}
var dio=null;
function buildDiff(){
  var box=document.getElementById("diffRows"); box.innerHTML="";
  document.documentElement.style.setProperty("--cA",ACC[PAIR[0]]);
  document.documentElement.style.setProperty("--cB",ACC[PAIR[1]]);
  if(dio)dio.disconnect();
  dio=new IntersectionObserver(function(ents){ents.forEach(function(e){if(e.isIntersecting){fillRow(e.target);dio.unobserve(e.target);}});},{rootMargin:"400px 0px"});
  var maxp=Math.max(PAGES[PAIR[0]].length,PAGES[PAIR[1]].length);
  for(var p=1;p<=maxp;p++){
    var row=el("div","drow"); row.dataset.page=p;
    var hd=el("div","dhead"); hd.innerHTML='<span class="pg">Page '+p+'</span><span class="pct" id="pct-'+p+'">&hellip;</span>'+
      '<span style="color:var(--muted);font-size:11px">'+TAG[PAIR[0]]+' vs '+TAG[PAIR[1]]+'</span>';
    row.appendChild(hd);
    var g=el("div","dgrid"); g.id="grid-"+p; row.appendChild(g);
    box.appendChild(row); dio.observe(row);
  }
}
function cell(capCls,capTxt){var c=el("div","dcell");var cap=el("div","cap "+capCls);cap.textContent=capTxt;c.appendChild(cap);return c;}
function emptyCell(txt){var c=el("div","dcell");var e=el("div","empty");e.textContent=txt;c.appendChild(e);return c;}
function fillRow(row){
  var p=+row.dataset.page, g=row.querySelector(".dgrid"); g.innerHTML="";
  var A=PAIR[0],B=PAIR[1], hasA=p<=PAGES[A].length, hasB=p<=PAGES[B].length;
  // A
  if(hasA){var ca=cell("A",TAG[A]+" · p."+p);var im=el("img");im.src=src(A,p);ca.appendChild(im);g.appendChild(ca);} else g.appendChild(emptyCell(TAG[A]+" has no p."+p));
  // diff
  if(hasA&&hasB){var cd=cell("","diff");var cv=el("canvas");cd.appendChild(cv);g.appendChild(cd);
    Promise.all([getImg(A,p),getImg(B,p)]).then(function(r){var pct=diffTo(cv,r[0],r[1]);
      var s=row.querySelector(".pct");s.textContent=(pct*100).toFixed(1)+"% changed";if(pct>0.06)s.className="pct hi";});
  } else {var cd=cell("","diff");cd.appendChild(emptyCell("no counterpart page"));g.appendChild(cd);
    var s=row.querySelector(".pct");if(s){s.textContent="—";}}
  // B
  if(hasB){var cb=cell("B",TAG[B]+" · p."+p);var im2=el("img");im2.src=src(B,p);cb.appendChild(im2);g.appendChild(cb);} else g.appendChild(emptyCell(TAG[B]+" has no p."+p));
}

/* ---------- wiring ---------- */
function setMode(m){
  var br=m==="browse";
  document.getElementById("mBrowse").classList.toggle("on",br);
  document.getElementById("mDiff").classList.toggle("on",!br);
  document.getElementById("browse").classList.toggle("hidden",!br);
  document.getElementById("diff").classList.toggle("hidden",br);
  document.getElementById("browseCtl").classList.toggle("hidden",!br);
  document.getElementById("diffCtl").classList.toggle("hidden",br);
  document.getElementById("hint").textContent=br?"Click a feature on the left to jump & flash it.":"Pick a pair; scroll the page rows. Diff is computed in your browser.";
  if(!br&&!document.getElementById("diffRows").children.length)buildDiff();
}
function wire(){
  buildBrowse();
  document.getElementById("mBrowse").onclick=function(){setMode("browse");};
  document.getElementById("mDiff").onclick=function(){setMode("diff");};
  document.querySelectorAll("[data-mode]").forEach(function(b){b.onclick=function(){
    document.querySelectorAll("[data-mode]").forEach(function(x){x.classList.remove("on");});b.classList.add("on");
    var m=b.dataset.mode,cols=document.getElementById("browse");cols.className="cols"+(m==="all"?"":" focus focus-"+m);
    // focus via inline display
    KEYS.forEach(function(k){document.getElementById("col-"+k).style.display=(m==="all"||m===k)?"flex":"none";});
  };});
  document.querySelectorAll("[data-pair]").forEach(function(b){b.onclick=function(){
    document.querySelectorAll("[data-pair]").forEach(function(x){x.classList.remove("on");});b.classList.add("on");
    PAIR=b.dataset.pair.split(","); buildDiff();
  };});
  document.querySelectorAll("[data-style]").forEach(function(b){b.onclick=function(){
    document.querySelectorAll("[data-style]").forEach(function(x){x.classList.remove("on");});b.classList.add("on");
    STYLE=b.dataset.style; buildDiff();
  };});
  var thr=document.getElementById("thr");
  thr.oninput=function(){THR=+thr.value;document.getElementById("thrv").textContent=thr.value;};
  thr.onchange=function(){buildDiff();};
  document.querySelectorAll(".feat").forEach(function(b){b.onclick=function(){
    document.querySelectorAll(".feat").forEach(function(x){x.classList.remove("active");});b.classList.add("active");
    setMode("browse");
    document.querySelectorAll("[data-mode]").forEach(function(x){x.classList.toggle("on",x.dataset.mode==="all");});
    KEYS.forEach(function(k){document.getElementById("col-"+k).style.display="flex";});
    jump("validity",+b.dataset.v||0);jump("decision",+b.dataset.d||0);jump("audit",+b.dataset.a||0);
  };});
  // default pair button highlighted
  document.querySelector("[data-pair='validity,decision']").classList.add("on");
}
wire();
</script>
</body>
</html>
'''

pages_js = "var PAGES=" + json.dumps(PAGES) + ";"
html = TEMPLATE.replace("__PAGES_DATA__", pages_js)
out = HERE / "compare-variants.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}  ({len(html)//1024} KB)")
