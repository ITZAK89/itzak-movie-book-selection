"""Generate a COMPLETELY NEW index.html from data files.
Only dependencies: batch*.json, grammar_study.json, grammar_quiz.json
Output: index_fresh.html — test this first, then rename to index.html"""
import json, os

# ── Load vocabulary ──
vocab = []
for b in sorted([f for f in os.listdir('.') if f.startswith('batch') and f.endswith('.json')]):
    with open(b) as f:
        vocab.extend(json.load(f))
print(f"Vocab: {len(vocab)} words")

# ── Load grammar ──
with open('grammar_study.json') as f:
    grammar = json.load(f)
with open('grammar_quiz.json') as f:
    grammar_quiz = json.load(f)
print(f"Grammar: {len(grammar)} study + {len(grammar_quiz)} quiz")

# ── Build JS data arrays ──
def build_words_js(words):
    lines = []
    for w in words:
        zh = json.dumps(w.get('zh',[]), ensure_ascii=False)
        if 'senses' in w:
            sp = []
            for s in w['senses']:
                sp.append('{label:"'+s['label']+'",defs:'+json.dumps(s.get('defs',[]),ensure_ascii=False)+',ex:'+json.dumps(s.get('ex',[]),ensure_ascii=False)+'}')
            lines.append(f'    {{ko:"{w["ko"]}",zh:{zh},senses:[{",".join(sp)}],lv:{w["lv"]},cat:"{w["cat"]}"}}')
        else:
            defs = json.dumps(w.get('defs',[]), ensure_ascii=False)
            ex = json.dumps(w.get('ex',[]), ensure_ascii=False)
            lines.append(f'    {{ko:"{w["ko"]}",zh:{zh},defs:{defs},ex:{ex},lv:{w["lv"]},cat:"{w["cat"]}"}}')
    return ',\n'.join(lines)

def build_grammar_js(items, typ='study'):
    lines = []
    for g in items:
        if typ == 'study':
            ex = json.dumps(g.get('examples',[]), ensure_ascii=False)
            lines.append(f'    {{pattern:"{g["pattern"]}",meaning:"{g["meaning"]}",detail:"{g["detail"]}",examples:{ex},lv:{g["lv"]},cat:"{g["cat"]}"}}')
        else:
            opts = json.dumps(g.get('options',[]), ensure_ascii=False)
            lines.append(f'    {{sentence:"{g["sentence"]}",options:{opts},answer:{g["answer"]},explanation:"{g["explanation"]}",lv:{g["lv"]},cat:"{g["cat"]}"}}')
    return ',\n'.join(lines)

words_js = build_words_js(vocab)
grammar_js = build_grammar_js(grammar, 'study')
grammar_quiz_js = build_grammar_js(grammar_quiz, 'quiz')

# ── Build complete HTML ──
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hangul — Korean Learning</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--c-bg:#fff;--c-text:#333;--c-text-dim:#666;--c-text-fade:#999;--c-border:#e5e5e5;--c-accent:#4a4a4a;--c-accent-on:#1a1a1a;--font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
html,body{{height:100%;background:var(--c-bg);color:var(--c-text);font-family:var(--font-sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.app{{display:flex;flex-direction:column;min-height:100vh}}
.topbar{{display:flex;align-items:center;justify-content:space-between;padding:12px 24px;border-bottom:1px solid var(--c-border)}}
.logo{{display:flex;align-items:baseline;gap:4px;font-size:18px;color:var(--c-accent-on);text-decoration:none;letter-spacing:-0.3px}}
.logo b{{font-weight:600;font-size:20px}}
.logo small{{font-size:13px;color:var(--c-text-fade);font-weight:400}}
.topbar__right{{font-size:13px;color:var(--c-text-dim)}}
.stage{{flex:1;padding:32px 24px}}
.stage__panel{{display:none;max-width:780px;margin:0 auto}}
.stage__panel--active{{display:block}}
.words-header{{margin-bottom:16px}}
.words-header h2{{font-size:22px;font-weight:500;color:var(--c-text-dim);letter-spacing:-0.3px}}
.words-header .desc{{font-size:14px;color:var(--c-text-fade);margin-top:2px}}
.controls{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:16px}}
.ctrl-btn{{padding:6px 14px;font-size:13px;font-family:inherit;color:var(--c-text-dim);background:none;border:1px solid var(--c-border);border-radius:6px;cursor:pointer;transition:all 0.15s;white-space:nowrap}}
.ctrl-btn:hover{{color:var(--c-accent-on);border-color:var(--c-accent-on)}}
.ctrl-btn--active{{color:var(--c-accent-on);border-color:var(--c-accent-on);font-weight:500}}
.ctrl-btn--accent{{color:var(--c-bg);background:var(--c-accent-on);border-color:var(--c-accent-on)}}
.ctrl-btn--accent:hover{{opacity:0.85}}
.daily-input{{width:56px;padding:6px 8px;font-size:13px;font-family:inherit;text-align:center;border:1px solid var(--c-border);border-radius:6px;color:var(--c-text)}}
.daily-input:focus{{outline:none;border-color:var(--c-accent-on)}}
.daily-label{{font-size:13px;color:var(--c-text-fade)}}
.ctrl-sep{{width:1px;height:20px;background:var(--c-border);margin:0 4px}}
.dropdown{{position:relative;display:inline-block}}
.dropdown__panel{{display:none;position:absolute;top:100%;left:0;margin-top:6px;padding:10px 14px;background:var(--c-bg);border:1px solid var(--c-border);border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,0.08);z-index:10;min-width:200px}}
.dropdown__panel--show{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{padding:4px 11px;font-size:12px;font-family:inherit;color:var(--c-text-fade);background:none;border:1px solid var(--c-border);border-radius:14px;cursor:pointer;transition:all 0.15s;white-space:nowrap}}
.chip:hover{{color:var(--c-text-dim);border-color:var(--c-text-dim)}}
.chip--active{{color:var(--c-accent-on);border-color:var(--c-accent-on);font-weight:500}}
.progress-wrap{{max-width:540px;margin:0 auto 20px}}
.progress-bar{{width:100%;height:3px;background:var(--c-border);border-radius:2px;overflow:hidden}}
.progress-bar__fill{{height:100%;background:var(--c-accent-on);transition:width 0.3s}}
.progress-text{{display:flex;justify-content:space-between;margin-top:6px;font-size:12px;color:var(--c-text-fade)}}
.flashcard-area{{display:flex;flex-direction:column;align-items:center;margin-bottom:20px}}
.flashcard{{width:100%;max-width:540px;min-height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 32px;border:1px solid var(--c-border);border-radius:8px;cursor:pointer;user-select:none;transition:box-shadow 0.2s;text-align:center;position:relative}}
.flashcard:hover{{box-shadow:0 2px 12px rgba(0,0,0,0.06)}}
.flashcard--flipped{{cursor:default}}
.flashcard__word{{font-size:36px;font-weight:500;color:var(--c-accent-on);letter-spacing:-0.5px;line-height:1.3}}
.flashcard__level{{display:inline-block;margin-top:8px;padding:2px 10px;font-size:11px;color:var(--c-text-fade);border:1px solid var(--c-border);border-radius:10px}}
.flashcard__meaning{{font-size:22px;color:var(--c-text-dim);margin-top:16px;line-height:1.4}}
.flashcard__cat{{margin-top:8px;font-size:12px;color:var(--c-text-fade)}}
.flashcard__examples{{margin-top:20px;width:100%;text-align:left;border-top:1px solid var(--c-border);padding-top:16px}}
.flashcard__examples-title{{font-size:11px;color:var(--c-text-fade);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px}}
.flashcard__sense{{border-top:1px solid var(--c-border);padding-top:14px;margin-top:14px;width:100%;text-align:left}}
.flashcard__sense:first-child{{border-top:none;padding-top:0;margin-top:0}}
.flashcard__sense-label{{font-size:14px;font-weight:500;color:var(--c-accent-on);margin-bottom:8px}}
.flashcard__ex{{margin-bottom:12px}}
.flashcard__ex-ko{{font-size:15px;color:var(--c-text);line-height:1.5}}
.flashcard__ex-zh{{font-size:14px;color:var(--c-text-fade);margin-top:2px;line-height:1.4}}
.flashcard__hint{{margin-top:18px;font-size:12px;color:var(--c-text-fade);opacity:0.7}}
.review-actions{{display:flex;flex-direction:column;gap:6px;position:absolute;top:12px;right:16px}}
.review-btn{{padding:5px 12px;font-size:11px;font-family:inherit;color:var(--c-text-fade);background:rgba(255,255,255,0.9);border:1px solid var(--c-border);border-radius:4px;cursor:pointer;transition:all 0.15s}}
.review-btn:hover{{color:var(--c-accent-on);border-color:var(--c-accent-on)}}
.review-btn--today:hover{{color:#c0392b;border-color:#c0392b}}
.review-btn--intense:hover{{color:#e67e22;border-color:#e67e22}}
.input-mode-area{{display:flex;align-items:center;gap:10px;margin-top:16px}}
.input-mode-area input{{padding:8px 14px;font-size:16px;font-family:inherit;border:1px solid var(--c-border);border-radius:6px;width:200px;text-align:center}}
.input-mode-area input:focus{{outline:none;border-color:var(--c-accent-on)}}
.input-mode-area .submit-btn{{padding:8px 18px;font-size:13px;font-family:inherit;color:var(--c-bg);background:var(--c-accent-on);border:none;border-radius:6px;cursor:pointer}}
.input-feedback{{font-size:14px;min-height:20px;margin-top:8px}}
.input-feedback--correct{{color:#27ae60}}
.input-feedback--wrong{{color:#c0392b}}
.flashcard-nav{{display:flex;align-items:center;gap:20px;margin-top:16px}}
.flashcard-nav button{{padding:8px 20px;font-size:13px;font-family:inherit;color:var(--c-text-dim);background:none;border:1px solid var(--c-border);border-radius:6px;cursor:pointer;transition:all 0.15s}}
.flashcard-nav button:hover{{color:var(--c-accent-on);border-color:var(--c-accent-on)}}
.flashcard-nav .counter{{font-size:13px;color:var(--c-text-fade);min-width:80px;text-align:center}}
.word-list-section{{margin-top:20px}}
.word-list-header{{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border:1px solid var(--c-border);border-radius:6px;cursor:pointer;user-select:none;transition:background 0.15s}}
.word-list-header:hover{{background:#fafafa}}
.word-list-header span:first-child{{font-size:14px;font-weight:500;color:var(--c-text-dim)}}
.word-list-hint{{font-size:12px;color:var(--c-text-fade)}}
.word-list-wrap{{max-height:360px;overflow-y:auto;border:1px solid var(--c-border);border-top:none;border-radius:0 0 6px 6px}}
.word-list{{width:100%;border-collapse:collapse;font-size:14px}}
.word-list th{{position:sticky;top:0;text-align:left;padding:10px 12px;border-bottom:1px solid var(--c-border);background:#fafafa;font-weight:500;color:var(--c-text-fade);font-size:12px;text-transform:uppercase;letter-spacing:0.3px}}
.word-list td{{padding:9px 12px;border-bottom:1px solid var(--c-border);color:var(--c-text-dim);vertical-align:top}}
.word-list tr{{cursor:pointer;transition:background 0.1s}}
.word-list tr:hover{{background:#fafafa}}
.word-list tr.current{{background:#f5f5f5}}
.word-list .ko{{font-weight:500;color:var(--c-text);font-size:15px}}
.word-list .zh{{color:var(--c-text-fade);font-size:13px}}
.word-list .cat-tag{{font-size:11px;color:var(--c-text-fade)}}
.word-list .lv-tag{{font-size:11px;color:var(--c-text-fade)}}
.grammar-mode-toggle{{display:flex;gap:0;margin-bottom:16px}}
.grammar-mode-toggle .ctrl-btn{{border-radius:0}}
.grammar-mode-toggle .ctrl-btn:first-child{{border-radius:6px 0 0 6px}}
.grammar-mode-toggle .ctrl-btn:last-child{{border-radius:0 6px 6px 0}}
.grammar-list{{display:flex;flex-direction:column;gap:10px;margin-top:20px}}
.grammar-card{{border:1px solid var(--c-border);border-radius:6px;cursor:pointer;transition:background 0.15s}}
.grammar-card:hover{{background:#fafafa}}
.grammar-card__header{{display:flex;align-items:center;justify-content:space-between;padding:14px 18px}}
.grammar-card__pattern{{font-size:18px;font-weight:500;color:var(--c-accent-on)}}
.grammar-card__meaning{{font-size:14px;color:var(--c-text-dim);margin-left:12px}}
.grammar-card__meta{{font-size:12px;color:var(--c-text-fade);white-space:nowrap}}
.grammar-card__body{{display:none;padding:0 18px 18px;border-top:1px solid var(--c-border)}}
.grammar-card--open .grammar-card__body{{display:block}}
.grammar-card__detail{{font-size:14px;color:var(--c-text-dim);line-height:1.6;margin-top:12px}}
.grammar-card__examples{{margin-top:12px}}
.grammar-card__ex{{margin-bottom:8px}}
.grammar-card__ex-ko{{font-size:14px;color:var(--c-text);line-height:1.5}}
.grammar-card__ex-zh{{font-size:13px;color:var(--c-text-fade);margin-top:2px}}
.quiz-area{{max-width:600px;margin:0 auto}}
.quiz-progress{{margin-bottom:16px;font-size:13px;color:var(--c-text-fade)}}
.quiz-sentence{{font-size:20px;color:var(--c-accent-on);line-height:1.6;margin-bottom:20px;padding:20px 24px;border:1px solid var(--c-border);border-radius:8px;background:#fafafa}}
.quiz-blank{{display:inline-block;min-width:80px;border-bottom:2px solid var(--c-accent-on);margin:0 4px}}
.quiz-options{{display:flex;flex-direction:column;gap:10px;margin-bottom:20px}}
.quiz-opt{{padding:12px 18px;font-size:15px;font-family:inherit;color:var(--c-text);background:var(--c-bg);border:1px solid var(--c-border);border-radius:6px;cursor:pointer;text-align:left;transition:all 0.15s}}
.quiz-opt:hover{{border-color:var(--c-accent-on)}}
.quiz-opt--correct{{border-color:#27ae60!important;background:#eafaf1!important;color:#27ae60!important}}
.quiz-opt--wrong{{border-color:#c0392b!important;background:#fdf2f2!important;color:#c0392b!important}}
.quiz-opt--disabled{{pointer-events:none;opacity:0.7}}
.quiz-feedback{{display:none;padding:16px 18px;border-radius:6px;margin-bottom:16px;font-size:14px;line-height:1.6}}
.quiz-feedback--correct{{display:block;background:#eafaf1;color:#27ae60;border:1px solid #a3e4bc}}
.quiz-feedback--wrong{{display:block;background:#fdf2f2;color:#c0392b;border:1px solid #f5b7b7}}
.quiz-next{{margin-top:12px;text-align:center}}
.quiz-score{{text-align:center;font-size:14px;color:var(--c-text-dim);margin-top:10px}}
.subnav{{display:flex;justify-content:center;gap:0;border-top:1px solid var(--c-border);padding:0 24px}}
.subnav__item{{padding:14px 24px;font-size:14px;color:var(--c-text-fade);background:none;border:none;border-bottom:2px solid transparent;cursor:pointer;font-family:inherit;transition:color 0.15s,border-color 0.15s}}
.subnav__item:hover{{color:var(--c-text-dim)}}
.subnav__item--active{{color:var(--c-accent-on);border-bottom-color:var(--c-accent-on)}}
.footer{{display:flex;justify-content:center;align-items:center;gap:20px;padding:12px 24px 20px;font-size:12px;color:var(--c-text-fade)}}
.footer a{{color:var(--c-text-fade);text-decoration:none;transition:color 0.15s}}
.footer a:hover{{color:var(--c-text-dim)}}
</style>
</head>
<body>
<div class="app">
<header class="topbar">
<a class="logo" href="./"><b>Hangul</b><small>Korean Learning</small></a>
<div class="topbar__right" id="topbar-info">TOPIK 4·5·6</div>
</header>
<main class="stage">

<section class="stage__panel stage__panel--active" id="panel-words">
<div class="words-header"><h2>Vocabulary</h2><p class="desc">Enter 查看释义 · 再按 Enter 跳下一个 · ← → 翻页</p></div>
<div class="controls">
<div class="dropdown" id="dd-level"><button class="ctrl-btn" id="btn-level">等级 ▾</button><div class="dropdown__panel" id="dp-level"><button class="chip chip--active" data-lv="4">4级</button><button class="chip chip--active" data-lv="5">5级</button><button class="chip chip--active" data-lv="6">6级</button></div></div>
<div class="dropdown" id="dd-cat"><button class="ctrl-btn" id="btn-cat">分类 ▾</button><div class="dropdown__panel" id="dp-cat"></div></div>
<span class="ctrl-sep"></span>
<button class="ctrl-btn ctrl-btn--active" id="btn-mode-flip">卡片模式</button><button class="ctrl-btn" id="btn-mode-input">输入模式</button>
<span class="ctrl-sep"></span>
<span class="daily-label">今日</span><input class="daily-input" id="daily-count" type="number" value="20" min="1" max="999"><span class="daily-label">词</span>
<button class="ctrl-btn" id="btn-review-today">今日复习 <span id="review-today-count">0</span></button>
<button class="ctrl-btn" id="btn-review-intense">强化复习 <span id="review-intense-count">0</span></button>
</div>
<div class="progress-wrap"><div class="progress-bar"><div class="progress-bar__fill" id="progress-fill" style="width:0%"></div></div><div class="progress-text"><span id="progress-label">0 / 0</span><span id="progress-seen">已看 0</span></div></div>
<div class="flashcard-area">
<div class="flashcard" id="flashcard">
<div class="flashcard__word" id="fc-word"></div><div class="flashcard__level" id="fc-level"></div>
<div class="flashcard__meaning" id="fc-meaning" style="display:none"></div><div class="flashcard__cat" id="fc-cat" style="display:none"></div>
<div class="flashcard__examples" id="fc-examples" style="display:none"></div>
<div class="review-actions" id="review-actions" style="display:none"><button class="review-btn review-btn--today" id="btn-mark-today">今日复习 ＋</button><button class="review-btn review-btn--intense" id="btn-mark-intense">强化复习 ＋</button></div>
<div class="input-mode-area" id="input-mode-area" style="display:none"><input type="text" id="input-answer" placeholder="输入韩文单词" autocomplete="off" autocapitalize="none" autocorrect="off" spellcheck="false"><button class="submit-btn" id="btn-submit">确认</button></div>
<div class="input-feedback" id="input-feedback"></div>
<div class="flashcard__hint" id="fc-hint-text">Press Enter</div>
</div>
<div class="flashcard-nav"><button id="btn-prev">&larr; Prev</button><span class="counter" id="word-counter">1 / 1</span><button id="btn-next">Next &rarr;</button></div>
</div>
<div class="word-list-section"><div class="word-list-header" id="word-list-toggle"><span>单词列表</span><span class="word-list-hint">点击展开 ▼</span></div>
<div class="word-list-wrap" id="word-list-wrap" style="display:none"><table class="word-list"><thead><tr><th>韩文</th><th>中文</th><th>等级</th><th>分类</th></tr></thead><tbody id="word-list-body"></tbody></table></div></div>
</section>

<section class="stage__panel" id="panel-grammar">
<h2>Grammar</h2>
<div class="controls">
<div class="dropdown" id="dd-grammar-lv"><button class="ctrl-btn" id="btn-grammar-lv">等级 ▾</button><div class="dropdown__panel" id="dp-grammar-lv"><button class="chip chip--active" data-glv="4">4级</button><button class="chip chip--active" data-glv="5">5级</button><button class="chip chip--active" data-glv="6">6级</button></div></div>
<div class="dropdown" id="dd-grammar-cat"><button class="ctrl-btn" id="btn-grammar-cat">分类 ▾</button><div class="dropdown__panel" id="dp-grammar-cat"></div></div>
<span class="ctrl-sep"></span><span class="daily-label">今日</span><input class="daily-input" id="grammar-daily-count" type="number" value="10" min="1" max="999"><span class="daily-label">条</span>
<button class="ctrl-btn" id="btn-grammar-review-today">今日复习 <span id="grammar-review-today-count">0</span></button>
<button class="ctrl-btn" id="btn-grammar-review-intense">强化复习 <span id="grammar-review-intense-count">0</span></button>
<span class="ctrl-sep"></span>
<div class="grammar-mode-toggle" style="margin-bottom:0"><button class="ctrl-btn ctrl-btn--active" id="grammar-mode-study">Study</button><button class="ctrl-btn" id="grammar-mode-quiz">Quiz</button></div>
</div>
<div id="grammar-study-view"><p class="desc">TOPIK 4·5·6 grammar patterns · click to expand</p><div class="grammar-list" id="grammar-list"></div></div>
<div id="grammar-quiz-view" style="display:none"><div class="quiz-area"><div class="quiz-progress" id="quiz-progress"></div><div class="quiz-sentence" id="quiz-sentence"></div><div class="quiz-options" id="quiz-options"></div><div class="quiz-feedback" id="quiz-feedback"></div><div class="quiz-next"><button class="ctrl-btn" id="quiz-next-btn">Next &rarr;</button></div><div class="quiz-score" id="quiz-score"></div></div></div>
</section>

<section class="stage__panel" id="panel-shadowing">
<h2>Shadowing</h2><p class="desc">Coming soon.</p>
</section>
</main>
<nav class="subnav">
<button class="subnav__item subnav__item--active" data-panel="panel-words">Vocabulary</button>
<button class="subnav__item" data-panel="panel-grammar">Grammar</button>
<button class="subnav__item" data-panel="panel-shadowing">Shadowing</button>
</nav>
<nav class="footer"><a href="#">About</a><span>&middot;</span><span>Hangul &copy; 2026</span></nav>
</div>
<script>
/* WORDS DATA */
var WORDS = [
{words_js}
];

/* GRAMMAR DATA */
var GRAMMAR = [
{grammar_js}
];

/* GRAMMAR QUIZ DATA */
var GRAMMAR_QUIZ = [
{grammar_quiz_js}
];

/* LOCAL STORAGE HELPERS */
function loadReviewList(key){{ try {{ var d=JSON.parse(localStorage.getItem(key)); return Array.isArray(d)?d:[]; }} catch(e){{ return []; }} }}
function saveReviewList(key,list){{ localStorage.setItem(key,JSON.stringify(list)); }}
function addToReviewList(key,ko){{ var list=loadReviewList(key); if(list.indexOf(ko)===-1){{ list.push(ko); saveReviewList(key,list); }} }}
function removeFromReviewList(key,ko){{ var list=loadReviewList(key); var idx=list.indexOf(ko); if(idx!==-1){{ list.splice(idx,1); saveReviewList(key,list); }} }}
function isInReviewList(key,ko){{ return loadReviewList(key).indexOf(ko)!==-1; }}

/* VOCABULARY STATE */
var activeLevels={{4:true,5:true,6:true}}, activeCat="All", filtered=[], currentIndex=0, seenCount=0, flipped=false, inputMode=false, inputAnswered=false, dailyLimit=20, reviewMode=null;
var LS_TODAY="hangul_review_today", LS_INTENSE="hangul_review_intense";
var cats=["All"], seenCats={{}};
WORDS.forEach(function(w){{ if(!seenCats[w.cat]){{ seenCats[w.cat]=true; cats.push(w.cat); }} }});

function updateReviewCounts(){{
  document.getElementById('review-today-count').textContent=loadReviewList(LS_TODAY).length;
  document.getElementById('review-intense-count').textContent=loadReviewList(LS_INTENSE).length;
}}

function applyFilter(){{
  if(reviewMode==="today"){{ var tl=loadReviewList(LS_TODAY); filtered=WORDS.filter(function(w){{ return tl.indexOf(w.ko)!==-1; }}); }}
  else if(reviewMode==="intense"){{ var il=loadReviewList(LS_INTENSE); filtered=WORDS.filter(function(w){{ return il.indexOf(w.ko)!==-1; }}); }}
  else{{ filtered=WORDS.filter(function(w){{ if(!activeLevels[w.lv]) return false; if(activeCat!=="All"&& w.cat!==activeCat) return false; return true; }}); }}
  var limit=parseInt(document.getElementById('daily-count').value)||20; dailyLimit=Math.max(1,limit);
  shuffle(filtered); if(filtered.length>dailyLimit) filtered=filtered.slice(0,dailyLimit);
  currentIndex=0; flipped=false; inputAnswered=false; seenCount=0; renderAll();
}}

function shuffle(arr){{ for(var i=arr.length-1;i>0;i--){{ var j=Math.floor(Math.random()*(i+1)); var t=arr[i];arr[i]=arr[j];arr[j]=t; }} }}

function renderChips(){{
  var h=''; cats.forEach(function(c){{ var cls=(c===activeCat)?'chip chip--active':'chip'; h+='<button class="'+cls+'" data-cat="'+c+'">'+c+'</button>'; }});
  document.getElementById('cat-filters').innerHTML=h;
}}

function renderFlashcard(){{
  if(filtered.length===0){{ document.getElementById('fc-word').textContent='No words'; document.getElementById('fc-level').textContent=''; document.getElementById('fc-meaning').style.display='none'; document.getElementById('fc-cat').style.display='none'; document.getElementById('fc-examples').innerHTML=''; document.getElementById('review-actions').style.display='none'; document.getElementById('fc-hint-text').textContent=''; document.getElementById('word-counter').textContent='0 / 0'; document.getElementById('progress-fill').style.width='0%'; document.getElementById('progress-label').textContent='0 / 0'; document.getElementById('progress-seen').textContent='已看 0'; return; }}
  var w=filtered[currentIndex];
  if(inputMode){{
    document.getElementById('fc-word').textContent=w.zh.join(' / '); document.getElementById('fc-level').textContent='TOPIK '+w.lv+'级';
    document.getElementById('fc-meaning').style.display='none'; document.getElementById('fc-cat').style.display='none'; document.getElementById('fc-examples').style.display='none';
    document.getElementById('fc-hint-text').style.display='none'; document.getElementById('input-mode-area').style.display=''; document.getElementById('review-actions').style.display='none';
    document.getElementById('input-feedback').textContent=''; document.getElementById('input-answer').value='';
    document.getElementById('flashcard').classList.add('flashcard--flipped'); document.getElementById('flashcard').style.cursor='default'; inputAnswered=false;
  }}else{{
    document.getElementById('fc-word').textContent=w.ko; document.getElementById('fc-level').textContent='TOPIK '+w.lv+'级';
    document.getElementById('fc-meaning').textContent=w.zh.join(' / '); document.getElementById('fc-cat').textContent=w.cat;
    document.getElementById('input-mode-area').style.display='none'; document.getElementById('input-feedback').textContent='';
    var eh='';
    if(w.senses&& w.senses.length>0){{
      w.senses.forEach(function(s){{
        eh+='<div class="flashcard__sense"><div class="flashcard__sense-label">'+s.label+'</div>';
        if(s.defs&& s.defs.length>0){{ eh+='<div class="flashcard__examples-title">词典释义</div>'; s.defs.forEach(function(d){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+d[0]+'</div><div class="flashcard__ex-zh">'+d[1]+'</div></div>'; }}); }}
        if(s.ex&& s.ex.length>0){{ eh+='<div class="flashcard__examples-title">例句</div>'; s.ex.forEach(function(e){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+e[0]+'</div><div class="flashcard__ex-zh">'+e[1]+'</div></div>'; }}); }}
        eh+='</div>';
      }});
    }}else{{
      if(w.defs&& w.defs.length>0){{ eh+='<div class="flashcard__examples-title">词典释义</div>'; w.defs.forEach(function(d){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+d[0]+'</div><div class="flashcard__ex-zh">'+d[1]+'</div></div>'; }}); }}
      if(w.ex&& w.ex.length>0){{ eh+='<div class="flashcard__examples-title">例句</div>'; w.ex.forEach(function(e){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+e[0]+'</div><div class="flashcard__ex-zh">'+e[1]+'</div></div>'; }}); }}
    }}
    document.getElementById('fc-examples').innerHTML=eh;
    if(flipped){{ showBack(); updateReviewButtonStates(); }}else{{ showFront(); }}
  }}
  document.getElementById('word-counter').textContent=(currentIndex+1)+' / '+filtered.length;
  var pct=filtered.length>0?Math.round((currentIndex+1)/filtered.length*100):0;
  document.getElementById('progress-fill').style.width=pct+'%';
  document.getElementById('progress-label').textContent=(currentIndex+1)+' / '+filtered.length;
  document.getElementById('progress-seen').textContent='已看 '+seenCount;
}}

function showFront(){{ document.getElementById('fc-meaning').style.display='none'; document.getElementById('fc-cat').style.display='none'; document.getElementById('fc-examples').style.display='none'; document.getElementById('review-actions').style.display='none'; document.getElementById('input-mode-area').style.display='none'; document.getElementById('input-feedback').textContent=''; document.getElementById('fc-hint-text').style.display=''; document.getElementById('flashcard').classList.remove('flashcard--flipped'); document.getElementById('flashcard').style.cursor='pointer'; inputAnswered=false; }}
function showBack(){{ document.getElementById('fc-meaning').style.display=''; document.getElementById('fc-cat').style.display=''; document.getElementById('fc-examples').style.display=''; document.getElementById('review-actions').style.display=''; document.getElementById('input-mode-area').style.display='none'; document.getElementById('fc-hint-text').style.display='none'; document.getElementById('flashcard').classList.add('flashcard--flipped'); document.getElementById('flashcard').style.cursor='default'; }}

function updateReviewButtonStates(){{
  if(filtered.length===0) return; var w=filtered[currentIndex];
  var bT=document.getElementById('btn-mark-today'), bI=document.getElementById('btn-mark-intense');
  if(isInReviewList(LS_TODAY,w.ko)){{ bT.textContent='今日复习 ✓'; bT.style.color='#c0392b'; bT.style.borderColor='#c0392b'; }}else{{ bT.textContent='今日复习 ＋'; bT.style.color=''; bT.style.borderColor=''; }}
  if(isInReviewList(LS_INTENSE,w.ko)){{ bI.textContent='强化复习 ✓'; bI.style.color='#e67e22'; bI.style.borderColor='#e67e22'; }}else{{ bI.textContent='强化复习 ＋'; bI.style.color=''; bI.style.borderColor=''; }}
}}

window.flipCard=function(){{ if(filtered.length===0||inputMode) return; if(flipped){{ nextWord(); }}else{{ flipped=true; seenCount++; tableRevealed[currentIndex]=true; showBack(); updateReviewButtonStates(); renderTable(); }} }};
window.nextWord=function(){{ if(filtered.length===0) return; currentIndex=(currentIndex+1)%filtered.length; flipped=false; inputAnswered=false; var pi=(currentIndex-1+filtered.length)%filtered.length; tableRevealed[pi]=true; renderFlashcard(); renderTable(); }};
window.prevWord=function(){{ if(filtered.length===0) return; currentIndex=(currentIndex-1+filtered.length)%filtered.length; flipped=false; inputAnswered=false; renderFlashcard(); renderTable(); }};
window.checkAnswer=function(){{
  if(filtered.length===0||!inputMode||inputAnswered) return; var w=filtered[currentIndex]; var ua=document.getElementById('input-answer').value.trim(); if(!ua) return;
  if(ua===w.ko){{
    document.getElementById('input-feedback').textContent='正确！'; document.getElementById('input-feedback').className='input-feedback input-feedback--correct';
    var eh='';
    if(w.senses&& w.senses.length>0){{ w.senses.forEach(function(s){{ eh+='<div class="flashcard__sense"><div class="flashcard__sense-label">'+s.label+'</div>'; if(s.defs&& s.defs.length>0){{ eh+='<div class="flashcard__examples-title">词典释义</div>'; s.defs.forEach(function(d){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+d[0]+'</div><div class="flashcard__ex-zh">'+d[1]+'</div></div>'; }}); }} if(s.ex&& s.ex.length>0){{ eh+='<div class="flashcard__examples-title">例句</div>'; s.ex.forEach(function(e){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+e[0]+'</div><div class="flashcard__ex-zh">'+e[1]+'</div></div>'; }}); }} eh+='</div>'; }}); }}
    else{{ if(w.defs&&w.defs.length>0){{ eh+='<div class="flashcard__examples-title">词典释义</div>'; w.defs.forEach(function(d){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+d[0]+'</div><div class="flashcard__ex-zh">'+d[1]+'</div></div>'; }}); }} if(w.ex&&w.ex.length>0){{ eh+='<div class="flashcard__examples-title">例句</div>'; w.ex.forEach(function(e){{ eh+='<div class="flashcard__ex"><div class="flashcard__ex-ko">'+e[0]+'</div><div class="flashcard__ex-zh">'+e[1]+'</div></div>'; }}); }} }}
    document.getElementById('fc-examples').innerHTML=eh; document.getElementById('fc-examples').style.display='';
    document.getElementById('fc-word').textContent=w.ko; document.getElementById('review-actions').style.display=''; updateReviewButtonStates();
    inputAnswered=true; seenCount++;
  }}else{{ document.getElementById('input-feedback').textContent='不对，请重试'; document.getElementById('input-feedback').className='input-feedback input-feedback--wrong'; document.getElementById('input-answer').select(); }}
}};
window.toggleTodayReview=function(){{ if(filtered.length===0) return; var w=filtered[currentIndex]; if(isInReviewList(LS_TODAY,w.ko)){{ removeFromReviewList(LS_TODAY,w.ko); }}else{{ addToReviewList(LS_TODAY,w.ko); }} updateReviewButtonStates(); updateReviewCounts(); }};
window.toggleIntenseReview=function(){{ if(filtered.length===0) return; var w=filtered[currentIndex]; if(isInReviewList(LS_INTENSE,w.ko)){{ removeFromReviewList(LS_INTENSE,w.ko); }}else{{ addToReviewList(LS_INTENSE,w.ko); }} updateReviewButtonStates(); updateReviewCounts(); }};
window.enterReviewMode=function(mode){{ if(reviewMode===mode){{ reviewMode=null; document.getElementById('btn-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-review-intense').classList.remove('ctrl-btn--accent'); }}else{{ reviewMode=mode; document.getElementById('btn-review-today').classList.toggle('ctrl-btn--accent',mode==='today'); document.getElementById('btn-review-intense').classList.toggle('ctrl-btn--accent',mode==='intense'); }} applyFilter(); }};

var tableRevealed={{}};
function renderTable(){{
  var h=''; filtered.forEach(function(w,i){{ var cls=(i===currentIndex)?'current':''; var zd=tableRevealed[i]?w.zh.join(' / '):'<span style="color:var(--c-text-fade);font-style:italic">点击显示</span>'; h+='<tr class="'+cls+'" data-index="'+i+'"><td class="ko">'+w.ko+'</td><td class="zh">'+zd+'</td><td class="lv-tag">'+w.lv+'级</td><td class="cat-tag">'+w.cat+'</td></tr>'; }});
  document.getElementById('word-list-body').innerHTML=h;
}}

function renderAll(){{ renderChips(); renderFlashcard(); renderTable(); updateReviewCounts(); var label=reviewMode==="today"?"今日复习":reviewMode==="intense"?"强化复习":"TOPIK 4·5·6"; document.getElementById('topbar-info').textContent=label+' · '+filtered.length+' words'; }}

document.getElementById('flashcard').addEventListener('click',function(e){{ if(e.target.closest('button')||e.target.closest('input')) return; if(inputMode) return; flipCard(); }});
document.getElementById('btn-prev').addEventListener('click',prevWord);
document.getElementById('btn-next').addEventListener('click',nextWord);
document.getElementById('word-list-body').addEventListener('click',function(e){{ var row=e.target.closest('tr'); if(!row) return; var idx=parseInt(row.getAttribute('data-index'),10); if(idx===currentIndex){{ tableRevealed[idx]=!tableRevealed[idx]; renderTable(); return; }} currentIndex=idx; flipped=false; inputAnswered=false; tableRevealed[currentIndex]=true; renderFlashcard(); renderTable(); }});
document.getElementById('btn-level').addEventListener('click',function(e){{ e.stopPropagation(); document.getElementById('dp-level').classList.toggle('dropdown__panel--show'); document.getElementById('dp-cat').classList.remove('dropdown__panel--show'); }});
document.getElementById('dp-level').addEventListener('click',function(e){{ var chip=e.target.closest('.chip'); if(!chip) return; var lv=parseInt(chip.getAttribute('data-lv')); var ac=Object.values(activeLevels).filter(Boolean).length; if(ac===1&&activeLevels[lv]) return; activeLevels[lv]=!activeLevels[lv]; chip.classList.toggle('chip--active',activeLevels[lv]); reviewMode=null; document.getElementById('btn-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-review-intense').classList.remove('ctrl-btn--accent'); applyFilter(); }});
document.getElementById('btn-cat').addEventListener('click',function(e){{ e.stopPropagation(); document.getElementById('dp-cat').classList.toggle('dropdown__panel--show'); document.getElementById('dp-level').classList.remove('dropdown__panel--show'); }});
document.getElementById('dp-cat').addEventListener('click',function(e){{ var chip=e.target.closest('.chip'); if(!chip||chip.hasAttribute('data-lv')) return; activeCat=chip.getAttribute('data-cat'); reviewMode=null; document.getElementById('btn-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-review-intense').classList.remove('ctrl-btn--accent'); applyFilter(); }});
document.addEventListener('click',function(e){{ if(!e.target.closest('#dd-level')) document.getElementById('dp-level').classList.remove('dropdown__panel--show'); if(!e.target.closest('#dd-cat')) document.getElementById('dp-cat').classList.remove('dropdown__panel--show'); }});
document.getElementById('btn-mode-flip').addEventListener('click',function(){{ inputMode=false; flipped=false; inputAnswered=false; document.getElementById('btn-mode-flip').classList.add('ctrl-btn--active'); document.getElementById('btn-mode-input').classList.remove('ctrl-btn--active'); renderFlashcard(); }});
document.getElementById('btn-mode-input').addEventListener('click',function(){{ inputMode=true; flipped=false; inputAnswered=false; document.getElementById('btn-mode-input').classList.add('ctrl-btn--active'); document.getElementById('btn-mode-flip').classList.remove('ctrl-btn--active'); renderFlashcard(); }});
document.getElementById('daily-count').addEventListener('change',function(){{ reviewMode=null; document.getElementById('btn-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-review-intense').classList.remove('ctrl-btn--accent'); applyFilter(); }});
document.getElementById('btn-review-today').addEventListener('click',function(){{ enterReviewMode(reviewMode==='today'?null:'today'); }});
document.getElementById('btn-review-intense').addEventListener('click',function(){{ enterReviewMode(reviewMode==='intense'?null:'intense'); }});
document.getElementById('btn-mark-today').addEventListener('click',function(e){{ e.stopPropagation(); toggleTodayReview(); }});
document.getElementById('btn-mark-intense').addEventListener('click',function(e){{ e.stopPropagation(); toggleIntenseReview(); }});
document.getElementById('btn-submit').addEventListener('click',checkAnswer);
document.getElementById('input-answer').addEventListener('keydown',function(e){{ if(e.key==='Enter') checkAnswer(); }});
document.addEventListener('keydown',function(e){{ if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return; if(e.key==='ArrowLeft'){{ e.preventDefault(); prevWord(); }}else if(e.key==='ArrowRight'){{ e.preventDefault(); nextWord(); }}else if(e.key==='Enter'){{ e.preventDefault(); flipCard(); }} }});
document.getElementById('word-list-toggle').addEventListener('click',function(){{ var w=document.getElementById('word-list-wrap'); var h=this.querySelector('.word-list-hint'); if(w.style.display==='none'){{ w.style.display=''; h.textContent='点击收起 ▲'; }}else{{ w.style.display='none'; h.textContent='点击展开 ▼'; }} }});

/* GRAMMAR STATE */
var gActiveLvs={{4:true,5:true,6:true}}, gActiveCat="All", gDailyLimit=10, gReviewMode=null;
var LS_GRAMMAR_TODAY="hangul_grammar_review_today", LS_GRAMMAR_INTENSE="hangul_grammar_review_intense";
var gCats=["All"], gSeenCats={{}};
GRAMMAR.forEach(function(g){{ if(!gSeenCats[g.cat]){{ gSeenCats[g.cat]=true; gCats.push(g.cat); }} }});
GRAMMAR_QUIZ.forEach(function(q){{ if(!gSeenCats[q.cat]){{ gSeenCats[q.cat]=true; gCats.push(q.cat); }} }});

function renderGrammarCatChips(){{ var h='<button class="chip chip--active" data-gcat="All">All</button>'; gCats.forEach(function(c){{ if(c==='All') return; var cls=(c===gActiveCat)?'chip chip--active':'chip'; h+='<button class="'+cls+'" data-gcat="'+c+'">'+c+'</button>'; }}); document.getElementById('dp-grammar-cat').innerHTML=h; }}

function filterGrammarList(list){{ return list.filter(function(item){{ if(gReviewMode==='today') return isInReviewList(LS_GRAMMAR_TODAY,item.pattern||item.sentence); if(gReviewMode==='intense') return isInReviewList(LS_GRAMMAR_INTENSE,item.pattern||item.sentence); if(!gActiveLvs[item.lv]) return false; if(gActiveCat!=='All'&&item.cat!==gActiveCat) return false; return true; }}); }}

function applyGrammarFilter(){{ var limit=parseInt(document.getElementById('grammar-daily-count').value)||10; gDailyLimit=Math.max(1,limit); renderGrammarCatChips(); renderGrammarStudy(); updateGrammarReviewCounts(); }}

function renderGrammarStudy(){{
  var list=filterGrammarList(GRAMMAR); if(gDailyLimit&&list.length>gDailyLimit) list=list.slice(0,gDailyLimit);
  var h=''; list.forEach(function(g,idx){{ h+='<div class="grammar-card" data-gidx="'+idx+'"><div class="grammar-card__header"><div><span class="grammar-card__pattern">'+g.pattern+'</span><span class="grammar-card__meaning">'+g.meaning+'</span></div><span class="grammar-card__meta">TOPIK '+g.lv+' · '+g.cat+'</span></div><div class="grammar-card__body"><div class="grammar-card__detail">'+g.detail+'</div><div class="grammar-card__examples">'; g.examples.forEach(function(ex){{ h+='<div class="grammar-card__ex"><div class="grammar-card__ex-ko">'+ex[0]+'</div><div class="grammar-card__ex-zh">'+ex[1]+'</div></div>'; }}); h+='</div><div class="review-actions" style="position:static;display:flex;flex-direction:row;padding:12px 0 0;margin-top:12px;border-top:1px solid var(--c-border)"><button class="review-btn review-btn--today grammar-mark-btn" data-gpat="'+g.pattern+'" data-gtype="today">今日复习 ＋</button><button class="review-btn review-btn--intense grammar-mark-btn" data-gpat="'+g.pattern+'" data-gtype="intense">强化复习 ＋</button></div></div></div>'; }});
  document.getElementById('grammar-list').innerHTML=h||'<p style="color:var(--c-text-fade);text-align:center;padding:20px">No grammar points.</p>';
  setTimeout(updateGrammarMarkButtons,50);
}}

function updateGrammarMarkButtons(){{ document.querySelectorAll('.grammar-mark-btn').forEach(function(btn){{ var pat=btn.getAttribute('data-gpat'),type=btn.getAttribute('data-gtype'),key=type==='today'?LS_GRAMMAR_TODAY:LS_GRAMMAR_INTENSE; if(isInReviewList(key,pat)){{ btn.textContent=(type==='today'?'今日复习 ✓':'强化复习 ✓'); btn.style.color=type==='today'?'#c0392b':'#e67e22'; btn.style.borderColor=type==='today'?'#c0392b':'#e67e22'; }}else{{ btn.textContent=(type==='today'?'今日复习 ＋':'强化复习 ＋'); btn.style.color=''; btn.style.borderColor=''; }} }}); }}
function updateGrammarReviewCounts(){{ document.getElementById('grammar-review-today-count').textContent=loadReviewList(LS_GRAMMAR_TODAY).length; document.getElementById('grammar-review-intense-count').textContent=loadReviewList(LS_GRAMMAR_INTENSE).length; }}

document.getElementById('grammar-list').addEventListener('click',function(e){{ var mb=e.target.closest('.grammar-mark-btn'); if(mb){{ e.stopPropagation(); var pat=mb.getAttribute('data-gpat'),type=mb.getAttribute('data-gtype'),key=type==='today'?LS_GRAMMAR_TODAY:LS_GRAMMAR_INTENSE; if(isInReviewList(key,pat)) removeFromReviewList(key,pat); else addToReviewList(key,pat); updateGrammarReviewCounts(); updateGrammarMarkButtons(); return; }} var card=e.target.closest('.grammar-card'); if(!card) return; card.classList.toggle('grammar-card--open'); }});

var quizIdx=0,quizCorrect=0,quizTotal=0,quizFiltered=[];
function prepareQuiz(){{ quizFiltered=filterGrammarList(GRAMMAR_QUIZ); if(gDailyLimit&&quizFiltered.length>gDailyLimit) quizFiltered=quizFiltered.slice(0,gDailyLimit); for(var i=quizFiltered.length-1;i>0;i--){{ var j=Math.floor(Math.random()*(i+1)); var t=quizFiltered[i]; quizFiltered[i]=quizFiltered[j]; quizFiltered[j]=t; }} quizIdx=0; quizCorrect=0; quizTotal=0; }}
function renderQuizQuestion(){{
  if(quizIdx>=quizFiltered.length){{ document.getElementById('quiz-sentence').textContent='Quiz complete!'; document.getElementById('quiz-options').innerHTML=''; document.getElementById('quiz-feedback').style.display='none'; document.getElementById('quiz-next-btn').style.display='none'; document.getElementById('quiz-score').textContent='Score: '+quizCorrect+' / '+quizTotal; document.getElementById('quiz-progress').textContent=''; return; }}
  var q=quizFiltered[quizIdx]; document.getElementById('quiz-progress').textContent=(quizIdx+1)+' / '+quizFiltered.length;
  document.getElementById('quiz-sentence').innerHTML=q.sentence.replace('___','<span class="quiz-blank"></span>');
  var o=''; q.options.forEach(function(opt,oi){{ o+='<button class="quiz-opt" data-oi="'+oi+'">'+String.fromCharCode(9312+oi)+' '+opt+'</button>'; }});
  document.getElementById('quiz-options').innerHTML=o; document.getElementById('quiz-feedback').style.display='none'; document.getElementById('quiz-next-btn').style.display='none'; document.getElementById('quiz-score').textContent='Correct: '+quizCorrect+' / '+quizTotal;
}}
document.getElementById('quiz-options').addEventListener('click',function(e){{ var btn=e.target.closest('.quiz-opt'); if(!btn||btn.classList.contains('quiz-opt--disabled')) return; var oi=parseInt(btn.getAttribute('data-oi')),q=quizFiltered[quizIdx]; quizTotal++; var correct=(oi===q.answer); if(correct) quizCorrect++; var all=document.querySelectorAll('#quiz-options .quiz-opt'); all.forEach(function(o){{ o.classList.add('quiz-opt--disabled'); if(parseInt(o.getAttribute('data-oi'))===q.answer) o.classList.add('quiz-opt--correct'); }}); if(!correct) btn.classList.add('quiz-opt--wrong'); var fb=document.getElementById('quiz-feedback'); fb.className='quiz-feedback quiz-feedback--'+(correct?'correct':'wrong'); fb.innerHTML=(correct?'Correct! ':'Wrong. ')+q.explanation; fb.style.display='block'; document.getElementById('quiz-next-btn').style.display=''; document.getElementById('quiz-score').textContent='Correct: '+quizCorrect+' / '+quizTotal; }});
document.getElementById('quiz-next-btn').addEventListener('click',function(){{ quizIdx++; renderQuizQuestion(); }});
document.getElementById('grammar-mode-study').addEventListener('click',function(){{ this.classList.add('ctrl-btn--active'); document.getElementById('grammar-mode-quiz').classList.remove('ctrl-btn--active'); document.getElementById('grammar-study-view').style.display=''; document.getElementById('grammar-quiz-view').style.display='none'; }});
document.getElementById('grammar-mode-quiz').addEventListener('click',function(){{ this.classList.add('ctrl-btn--active'); document.getElementById('grammar-mode-study').classList.remove('ctrl-btn--active'); document.getElementById('grammar-study-view').style.display='none'; document.getElementById('grammar-quiz-view').style.display=''; prepareQuiz(); renderQuizQuestion(); }});
document.getElementById('dp-grammar-lv').addEventListener('click',function(e){{ var chip=e.target.closest('.chip'); if(!chip) return; var lv=parseInt(chip.getAttribute('data-glv')); var ac=Object.values(gActiveLvs).filter(Boolean).length; if(ac===1&&gActiveLvs[lv]) return; gActiveLvs[lv]=!gActiveLvs[lv]; chip.classList.toggle('chip--active',gActiveLvs[lv]); gReviewMode=null; document.getElementById('btn-grammar-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-grammar-review-intense').classList.remove('ctrl-btn--accent'); applyGrammarFilter(); }});
document.getElementById('btn-grammar-lv').addEventListener('click',function(e){{ e.stopPropagation(); document.getElementById('dp-grammar-lv').classList.toggle('dropdown__panel--show'); document.getElementById('dp-grammar-cat').classList.remove('dropdown__panel--show'); }});
document.getElementById('dp-grammar-cat').addEventListener('click',function(e){{ var chip=e.target.closest('.chip'); if(!chip) return; gActiveCat=chip.getAttribute('data-gcat'); gReviewMode=null; document.getElementById('btn-grammar-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-grammar-review-intense').classList.remove('ctrl-btn--accent'); applyGrammarFilter(); }});
document.getElementById('btn-grammar-cat').addEventListener('click',function(e){{ e.stopPropagation(); document.getElementById('dp-grammar-cat').classList.toggle('dropdown__panel--show'); document.getElementById('dp-grammar-lv').classList.remove('dropdown__panel--show'); }});
document.getElementById('grammar-daily-count').addEventListener('change',function(){{ gReviewMode=null; document.getElementById('btn-grammar-review-today').classList.remove('ctrl-btn--accent'); document.getElementById('btn-grammar-review-intense').classList.remove('ctrl-btn--accent'); applyGrammarFilter(); }});
document.getElementById('btn-grammar-review-today').addEventListener('click',function(){{ if(gReviewMode==='today'){{ gReviewMode=null; this.classList.remove('ctrl-btn--accent'); }}else{{ gReviewMode='today'; this.classList.add('ctrl-btn--accent'); document.getElementById('btn-grammar-review-intense').classList.remove('ctrl-btn--accent'); }} applyGrammarFilter(); }});
document.getElementById('btn-grammar-review-intense').addEventListener('click',function(){{ if(gReviewMode==='intense'){{ gReviewMode=null; this.classList.remove('ctrl-btn--accent'); }}else{{ gReviewMode='intense'; this.classList.add('ctrl-btn--accent'); document.getElementById('btn-grammar-review-today').classList.remove('ctrl-btn--accent'); }} applyGrammarFilter(); }});

renderChips(); renderGrammarCatChips(); applyFilter(); applyGrammarFilter(); updateReviewCounts(); updateGrammarReviewCounts();

(function(){{
  var nav=document.querySelector('.subnav'); var items=nav.querySelectorAll('.subnav__item'); var panels=document.querySelectorAll('.stage__panel');
  nav.addEventListener('click',function(e){{ var btn=e.target.closest('.subnav__item'); if(!btn) return; var pid=btn.getAttribute('data-panel'); items.forEach(function(el){{ el.classList.remove('subnav__item--active'); }}); btn.classList.add('subnav__item--active'); panels.forEach(function(el){{ el.classList.remove('stage__panel--active'); }}); document.getElementById(pid).classList.add('stage__panel--active'); }});
}})();
</script>
</body>
</html>'''

with open("index_fresh.html", "w") as f:
    f.write(html)
print(f"Generated index_fresh.html ({len(html)} bytes)")
