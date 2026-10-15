# build_html.py
# Compiles all 100 questions and the interactive game engine into an ultra-juiced,
# visually stunning, sound-equipped standalone single-file HTML5 app (index.html).

import json
from generate_syllabus_questions import add_q, questions
from syllabus_part1 import load_part1
from syllabus_part2 import load_part2
from syllabus_part3 import load_part3

load_part1(add_q)
load_part2(add_q)
load_part3(add_q)

questions_json = json.dumps(questions, indent=2)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>C Midterm Arena - Ultimate Visual & Audio Edition</title>
  <style>
    /* -------------------------------------------------------------
       DESIGN SYSTEM: Cyber-Tokyo Glass & Obsidian Palette
       ------------------------------------------------------------- */
    :root {
      --bg-base: #080c14;
      --bg-surface: #0f1726;
      --bg-surface-elevated: #162238;
      --bg-code: #05080f;
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: #38bdf8;
      
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #475569;
      
      --accent-blue: #38bdf8;
      --accent-blue-glow: rgba(56, 189, 248, 0.4);
      --accent-amber: #fbbf24;
      --accent-amber-glow: rgba(251, 191, 36, 0.4);
      --accent-green: #34d399;
      --accent-green-glow: rgba(52, 211, 153, 0.4);
      --accent-red: #fb7185;
      --accent-red-glow: rgba(251, 113, 133, 0.4);
      --accent-purple: #c084fc;
      
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: "Fira Code", "JetBrains Mono", Consolas, Menlo, monospace;
      
      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --shadow-elevated: 0 10px 30px -5px rgba(0, 0, 0, 0.7);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      user-select: none;
    }

    /* Screen shake container */
    #arena-root {
      display: flex;
      flex-direction: column;
      flex: 1;
      height: 100vh;
      overflow: hidden;
      transform-origin: center center;
    }

    /* Particle Canvas overlay */
    #particle-canvas {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      pointer-events: none;
      z-index: 999;
    }

    /* Scrollbars */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }

    /* Header Bar */
    header {
      background: rgba(15, 23, 38, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .logo-badge {
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      color: #fff;
      font-weight: 800;
      font-size: 13px;
      letter-spacing: 0.5px;
      padding: 5px 12px;
      border-radius: var(--radius-sm);
      font-family: var(--font-mono);
      box-shadow: 0 0 16px var(--accent-blue-glow);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .brand-title {
      font-weight: 700;
      font-size: 16px;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .brand-subtitle {
      font-size: 12px;
      color: var(--text-dim);
      font-weight: 400;
    }

    /* Mode Switcher */
    .mode-bar {
      display: flex;
      background: rgba(0, 0, 0, 0.4);
      padding: 4px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-subtle);
      gap: 2px;
    }

    .mode-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .mode-btn.active {
      background: var(--bg-surface-elevated);
      color: var(--accent-blue);
      box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    .mode-btn:hover:not(.active) {
      color: var(--text-main);
    }

    /* Stats & Telemetry */
    .header-stats {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .stat-pill {
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .stat-pill.pop {
      transform: scale(1.15);
    }

    .stat-pill.streak { color: var(--accent-amber); border-color: rgba(251, 191, 36, 0.2); }
    .stat-pill.lives { color: var(--accent-red); border-color: rgba(251, 113, 133, 0.2); }
    .stat-pill.accuracy { color: var(--accent-green); border-color: rgba(52, 211, 153, 0.2); }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .icon-btn {
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
      font-size: 15px;
    }

    .icon-btn:hover {
      background: var(--bg-surface-elevated);
      color: var(--text-main);
      border-color: rgba(255,255,255,0.2);
      transform: translateY(-1px);
    }

    .icon-btn.active {
      color: var(--accent-amber);
      border-color: var(--accent-amber);
      box-shadow: 0 0 10px var(--accent-amber-glow);
    }

    /* Subheader Filter Bar */
    .filter-bar {
      background: #0b111c;
      border-bottom: 1px solid var(--border-subtle);
      padding: 8px 24px;
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
    }

    .filter-chip {
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 12px;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
    }

    .filter-chip:hover {
      background: var(--bg-surface-elevated);
      color: var(--text-main);
    }

    .filter-chip.active {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-blue);
      color: var(--accent-blue);
      font-weight: 600;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.2);
    }

    /* Main Split Arena */
    main {
      flex: 1;
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      height: calc(100vh - 105px);
      overflow: hidden;
    }

    @media (max-width: 1024px) {
      main {
        grid-template-columns: 1fr;
        height: auto;
        overflow: visible;
      }
    }

    /* Left Pane */
    .left-pane {
      border-right: 1px solid var(--border-subtle);
      padding: 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    /* Right Pane */
    .right-pane {
      background: #090e17;
      padding: 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    /* Question Meta */
    .q-meta {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .q-badges {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .badge {
      font-size: 11px;
      font-weight: 700;
      padding: 3px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-family: var(--font-mono);
    }

    .badge.cat { background: rgba(56, 189, 248, 0.15); color: var(--accent-blue); border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge.easy { background: rgba(52, 211, 153, 0.15); color: var(--accent-green); }
    .badge.medium { background: rgba(251, 191, 36, 0.15); color: var(--accent-amber); }
    .badge.tricky { background: rgba(192, 132, 252, 0.15); color: var(--accent-purple); }
    .badge.nightmare { background: rgba(251, 113, 133, 0.15); color: var(--accent-red); box-shadow: 0 0 10px rgba(251, 113, 133, 0.3); }

    .q-index {
      font-size: 13px;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }

    .q-title {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-main);
      line-height: 1.3;
      letter-spacing: -0.3px;
    }

    .q-prompt {
      font-size: 14px;
      color: var(--text-muted);
    }

    /* Code Container */
    .code-container {
      background: var(--bg-code);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
      box-shadow: inset 0 2px 8px rgba(0,0,0,0.6);
      transition: border-color 0.2s ease;
    }

    .code-header {
      background: #0d1422;
      border-bottom: 1px solid var(--border-subtle);
      padding: 9px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: var(--text-dim);
      font-family: var(--font-mono);
    }

    .code-dots {
      display: flex;
      gap: 6px;
    }

    .code-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #1e293b;
    }

    .code-body {
      padding: 14px 0;
      font-family: var(--font-mono);
      font-size: 13.5px;
      line-height: 1.65;
      overflow-x: auto;
    }

    .code-line {
      display: flex;
      padding: 1px 16px;
      transition: background 0.15s ease, border 0.15s ease;
      position: relative;
    }

    .code-line.trap-line {
      background: rgba(251, 191, 36, 0.12);
      border-left: 3px solid var(--accent-amber);
    }

    .code-line.executing-line {
      background: rgba(56, 189, 248, 0.18);
      border-left: 3px solid var(--accent-blue);
    }

    .line-num {
      width: 32px;
      color: #334155;
      user-select: none;
      text-align: right;
      padding-right: 14px;
      flex-shrink: 0;
    }

    .line-text {
      flex: 1;
      white-space: pre;
    }

    /* Syntax Highlighting */
    .tok-kw { color: #f472b6; font-weight: 600; }
    .tok-type { color: #38bdf8; font-weight: 600; }
    .tok-pre { color: #c084fc; font-weight: 600; }
    .tok-str { color: #a3e635; }
    .tok-num { color: #fb923c; }
    .tok-cmt { color: #64748b; font-style: italic; }
    .tok-fn  { color: #60a5fa; }

    /* Trap Token Highlight Badge */
    mark.trap-token {
      background: rgba(251, 191, 36, 0.25);
      color: #fef08a;
      padding: 1px 5px;
      border-radius: 4px;
      border: 1px dashed var(--accent-amber);
      font-weight: 700;
      animation: pulse-glow 2s infinite ease-in-out;
    }

    @keyframes pulse-glow {
      0%, 100% { box-shadow: 0 0 0 rgba(251, 191, 36, 0); }
      50% { box-shadow: 0 0 12px rgba(251, 191, 36, 0.5); }
    }

    /* Options Grid */
    .options-grid {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .option-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 15px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
      cursor: pointer;
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }

    .option-card:hover:not(.locked) {
      background: var(--bg-surface-elevated);
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }

    .option-card:active:not(.locked) {
      transform: scale(0.98);
    }

    .option-card.locked {
      cursor: default;
    }

    .option-key {
      width: 32px;
      height: 32px;
      border-radius: var(--radius-sm);
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 13px;
      font-family: var(--font-mono);
      flex-shrink: 0;
      transition: all 0.2s ease;
    }

    .option-text {
      flex: 1;
      font-family: var(--font-mono);
      font-size: 14.5px;
      color: var(--text-main);
    }

    .option-card.correct {
      background: rgba(52, 211, 153, 0.12);
      border-color: var(--accent-green);
      box-shadow: 0 0 20px var(--accent-green-glow);
      animation: pop-spring 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .option-card.correct .option-key {
      background: var(--accent-green);
      color: #0b0f17;
      border-color: var(--accent-green);
    }

    .option-card.wrong {
      background: rgba(251, 113, 133, 0.12);
      border-color: var(--accent-red);
      box-shadow: 0 0 20px var(--accent-red-glow);
      animation: shake-h 0.3s ease-in-out;
    }

    .option-card.wrong .option-key {
      background: var(--accent-red);
      color: #fff;
      border-color: var(--accent-red);
    }

    @keyframes pop-spring {
      0% { transform: scale(0.95); }
      50% { transform: scale(1.03); }
      100% { transform: scale(1); }
    }

    @keyframes shake-h {
      0%, 100% { transform: translateX(0); }
      20%, 60% { transform: translateX(-6px); }
      40%, 80% { transform: translateX(6px); }
    }

    /* Bottom Navigation Bar */
    .nav-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-top: 8px;
    }

    .btn {
      padding: 12px 24px;
      border-radius: var(--radius-sm);
      font-weight: 700;
      font-size: 14px;
      cursor: pointer;
      border: none;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .btn-secondary {
      background: var(--bg-surface-elevated);
      color: var(--text-main);
      border: 1px solid var(--border-subtle);
    }

    .btn-secondary:hover:not(:disabled) {
      background: #1e2c44;
      transform: translateY(-1px);
    }

    .btn-primary {
      background: var(--accent-blue);
      color: #080c14;
      box-shadow: 0 0 15px var(--accent-blue-glow);
    }

    .btn-primary:hover:not(:disabled) {
      background: #7dd3fc;
      transform: translateY(-2px);
      box-shadow: 0 0 25px var(--accent-blue-glow);
    }

    .btn:disabled {
      opacity: 0.35;
      cursor: not-allowed;
      transform: none !important;
      box-shadow: none !important;
    }

    /* Right Pane: Inspector Cards */
    .inspector-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      box-shadow: var(--shadow-elevated);
    }

    .card-title {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-dim);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Stepper Controls */
    .stepper-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    .stepper-controls {
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .step-btn {
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 7px 14px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s ease;
    }

    .step-btn:hover:not(:disabled) {
      background: var(--bg-surface-elevated);
      border-color: var(--accent-blue);
      color: var(--accent-blue);
    }

    .step-btn:disabled {
      opacity: 0.25;
      cursor: not-allowed;
    }

    .stepper-slider {
      width: 100%;
      height: 6px;
      background: rgba(0, 0, 0, 0.4);
      border-radius: 3px;
      outline: none;
      -webkit-appearance: none;
    }

    .stepper-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--accent-blue);
      cursor: pointer;
      box-shadow: 0 0 12px var(--accent-blue-glow);
    }

    .step-desc-box {
      background: var(--bg-code);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      padding: 14px;
      font-size: 13.5px;
      line-height: 1.5;
      color: var(--text-main);
      border-left: 3px solid var(--accent-blue);
    }

    /* Memory Table & Interactive SVG */
    .mem-table {
      width: 100%;
      border-collapse: collapse;
      font-family: var(--font-mono);
      font-size: 12.5px;
    }

    .mem-table th {
      text-align: left;
      padding: 8px 12px;
      color: var(--text-dim);
      border-bottom: 1px solid var(--border-subtle);
      font-weight: 600;
    }

    .mem-table td {
      padding: 8px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-main);
    }

    .mem-addr { color: #64748b; }
    .mem-val { color: var(--accent-amber); font-weight: 700; }
    .mem-ptr { color: var(--accent-blue); font-weight: 600; }

    /* Trap Spotlight Card */
    .trap-card {
      background: rgba(251, 191, 36, 0.06);
      border: 1px solid rgba(251, 191, 36, 0.3);
      border-radius: var(--radius-md);
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 0 20px rgba(251, 191, 36, 0.08);
    }

    .trap-card-title {
      color: var(--accent-amber);
      font-size: 13px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .trap-card-text {
      font-size: 13.5px;
      color: #fef08a;
      line-height: 1.5;
    }

    /* Distractor Psychology */
    .distractor-item {
      background: var(--bg-code);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-sm);
      overflow: hidden;
    }

    .distractor-header {
      padding: 12px 16px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      background: #0d1422;
      transition: background 0.15s ease;
    }

    .distractor-header:hover {
      background: #141f33;
    }

    .distractor-body {
      padding: 14px 16px;
      font-size: 12.5px;
      line-height: 1.6;
      color: var(--text-muted);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .c-standard-badge {
      display: inline-block;
      font-size: 11.5px;
      color: var(--text-dim);
      font-family: var(--font-mono);
      margin-top: 6px;
    }

    /* Modal Styling */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 200;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-box {
      background: var(--bg-surface);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: var(--radius-lg);
      width: 90%;
      max-width: 620px;
      max-height: 85vh;
      overflow-y: auto;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      box-shadow: 0 25px 60px rgba(0,0,0,0.9);
      transform: translateY(20px);
      transition: transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .modal-overlay.open .modal-box {
      transform: translateY(0);
    }

    .modal-title {
      font-size: 20px;
      font-weight: 800;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
  </style>
</head>
<body>

  <!-- Particle Canvas for 60fps sparks & confetti -->
  <canvas id="particle-canvas"></canvas>

  <div id="arena-root">

    <!-- Top Navigation Header -->
    <header>
      <div class="brand-group">
        <span class="logo-badge">⚡ C::ARENA</span>
        <div>
          <div class="brand-title">
            <span>Konsep Pemrograman</span>
            <span class="brand-subtitle">UTS Mastery Arena</span>
          </div>
        </div>
      </div>

      <!-- Mode Switcher -->
      <div class="mode-bar">
        <button class="mode-btn active" id="mode-study" onclick="setMode('STUDY')">📖 Study</button>
        <button class="mode-btn" id="mode-rush" onclick="setMode('RUSH')">⚡ Exam Rush (30Q)</button>
        <button class="mode-btn" id="mode-survival" onclick="setMode('SURVIVAL')">💀 Survival (3 Lives)</button>
      </div>

      <!-- Stats & Live Telemetry -->
      <div class="header-stats">
        <div class="stat-pill streak" id="stat-streak" title="Correct Streak">🔥 0</div>
        <div class="stat-pill lives" id="stat-lives" style="display:none;" title="Lives Remaining">❤️❤️❤️</div>
        <div class="stat-pill accuracy" id="stat-score" title="Accuracy Rate">0%</div>
        <div class="stat-pill" id="stat-counter" title="Current Question Index">1 / 100</div>
      </div>

      <!-- Header Tools -->
      <div class="header-actions">
        <button class="icon-btn active" id="btn-audio" onclick="toggleAudio()" title="Sound Effects (M)">🔊</button>
        <button class="icon-btn" id="btn-bookmark" onclick="toggleBookmark()" title="Bookmark Trap (B)">⭐</button>
        <button class="icon-btn" onclick="openShortcutsModal()" title="Keyboard Shortcuts">⌨️</button>
        <button class="icon-btn" onclick="openReportModal()" title="Export Study Guide">📋</button>
      </div>
    </header>

    <!-- Subheader / Category Filter Bar -->
    <nav class="filter-bar" id="category-filter-bar">
      <button class="filter-chip active" data-cat="ALL" onclick="setCategoryFilter('ALL')">All Syllabus Questions (100)</button>
      <button class="filter-chip" data-cat="TOPIC_DATATYPES" onclick="setCategoryFilter('TOPIC_DATATYPES')">1. Data Types & Variables (16)</button>
      <button class="filter-chip" data-cat="TOPIC_OPERATORS" onclick="setCategoryFilter('TOPIC_OPERATORS')">2. Operators & Expressions (18)</button>
      <button class="filter-chip" data-cat="TOPIC_CONDITIONALS" onclick="setCategoryFilter('TOPIC_CONDITIONALS')">3. Conditionals (if/switch) (16)</button>
      <button class="filter-chip" data-cat="TOPIC_LOOPS" onclick="setCategoryFilter('TOPIC_LOOPS')">4. Loops (for/while/do-while) (18)</button>
      <button class="filter-chip" data-cat="TOPIC_FUNCTIONS" onclick="setCategoryFilter('TOPIC_FUNCTIONS')">5. Functions & Procedures (16)</button>
      <button class="filter-chip" data-cat="TOPIC_ARRAYS" onclick="setCategoryFilter('TOPIC_ARRAYS')">6. Arrays & Strings (16)</button>
      <button class="filter-chip" data-cat="BOOKMARKED" onclick="setCategoryFilter('BOOKMARKED')">⭐ Bookmarked Only</button>
    </nav>

    <!-- Main Split Arena -->
    <main>
      <!-- Left Pane: Code & Question Options -->
      <section class="left-pane" id="pane-left">
        <div class="q-meta">
          <div class="q-badges">
            <span class="badge cat" id="q-category">Data Types</span>
            <span class="badge tricky" id="q-difficulty">Tricky</span>
          </div>
          <div class="q-index" id="q-id-label">Question Q001</div>
        </div>

        <h1 class="q-title" id="q-title-text">Post-Increment Dereference (*p++)</h1>
        <p class="q-prompt" id="q-prompt-text">What is the output of the following program?</p>

        <!-- C Code Block -->
        <div class="code-container">
          <div class="code-header">
            <div class="code-dots">
              <div class="code-dot" style="background:#f43f5e;"></div>
              <div class="code-dot" style="background:#fbbf24;"></div>
              <div class="code-dot" style="background:#10b981;"></div>
            </div>
            <span>solution.c (ISO C99/C11)</span>
          </div>
          <div class="code-body" id="code-viewer">
            <!-- Populated by JavaScript -->
          </div>
        </div>

        <!-- Multiple Choice Options -->
        <div class="options-grid" id="options-container">
          <!-- Populated by JavaScript -->
        </div>

        <!-- Bottom Navigation Controls -->
        <div class="nav-bar">
          <button class="btn btn-secondary" id="btn-prev" onclick="prevQuestion()" disabled>← Previous</button>
          <button class="btn btn-primary" id="btn-next" onclick="nextQuestion()">Next Question (Space) →</button>
        </div>
      </section>

      <!-- Right Pane: Pedagogical Stepper & Memory Visualizer -->
      <section class="right-pane" id="pane-right">
        
        <!-- Stepper Controls -->
        <div class="inspector-card">
          <div class="stepper-header">
            <span class="card-title">🔍 Step-by-Step Execution Tracer</span>
            <div class="stepper-controls">
              <button class="step-btn" onclick="stepReset()" title="Reset to start">⏮</button>
              <button class="step-btn" onclick="stepPrev()" title="Previous step (Left Arrow)">◀ Prev</button>
              <button class="step-btn" onclick="stepNext()" title="Next step (Right Arrow)">▶ Next</button>
              <button class="step-btn" onclick="stepToEnd()" title="Jump to end">⏭</button>
            </div>
          </div>
          <input type="range" class="stepper-slider" id="stepper-slider" min="0" max="1" value="0" oninput="onSliderChange(this.value)">
          <div class="step-desc-box" id="step-description">
            Click an answer or use the stepper controls above to inspect line-by-line machine execution.
          </div>
        </div>

        <!-- Active Memory Layout Diagram -->
        <div class="inspector-card" id="memory-card">
          <span class="card-title">🧠 Stack Memory & Pointer Architecture</span>
          <div class="memory-view" id="memory-view-content">
            <table class="mem-table">
              <thead>
                <tr>
                  <th>Variable</th>
                  <th>Address</th>
                  <th>Type</th>
                  <th>Stored Value</th>
                </tr>
              </thead>
              <tbody id="mem-table-body">
                <tr><td colspan="4" style="color:var(--text-dim); text-align:center;">Select an answer or step forward to inspect stack state.</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Trap Spotlight Card -->
        <div class="trap-card" id="trap-spotlight">
          <div class="trap-card-title">⚠️ The Trap Spotlight</div>
          <div class="trap-card-text" id="trap-spotlight-text">
            Loading trap analysis...
          </div>
        </div>

        <!-- Cognitive Distractor Breakdown -->
        <div class="inspector-card">
          <span class="card-title">💡 Why Your Wrong Answer Was Tempting</span>
          <div style="display:flex; flex-direction:column; gap:8px;" id="distractor-container">
            <!-- Populated by JavaScript -->
          </div>
          <span class="c-standard-badge" id="c-standard-ref">ISO Standard: ISO/IEC 9899 §6.5</span>
        </div>

      </section>
    </main>
  </div>

  <!-- Keyboard Shortcuts Modal -->
  <div class="modal-overlay" id="shortcuts-modal" onclick="closeModalOnOuter(event, 'shortcuts-modal')">
    <div class="modal-box">
      <div class="modal-title">
        <span>⌨️ Keyboard Shortcuts</span>
        <button class="icon-btn" onclick="closeModal('shortcuts-modal')">✕</button>
      </div>
      <table class="mem-table">
        <tbody>
          <tr><td><kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> or <kbd>A</kbd> / <kbd>B</kbd> / <kbd>C</kbd> / <kbd>D</kbd></td><td>Select Multiple Choice Option</td></tr>
          <tr><td><kbd>Space</kbd> or <kbd>Enter</kbd></td><td>Next Question</td></tr>
          <tr><td><kbd>Left Arrow</kbd> / <kbd>Right Arrow</kbd></td><td>Step Execution Back / Forward</td></tr>
          <tr><td><kbd>B</kbd></td><td>Bookmark / Star Question</td></tr>
          <tr><td><kbd>M</kbd></td><td>Mute / Unmute Audio Synthesizer</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Study Guide / Missed Questions Report Modal -->
  <div class="modal-overlay" id="report-modal" onclick="closeModalOnOuter(event, 'report-modal')">
    <div class="modal-box" style="max-width: 750px;">
      <div class="modal-title">
        <span>📋 Midterm Study & Cramming Summary</span>
        <button class="icon-btn" onclick="closeModal('report-modal')">✕</button>
      </div>
      <div id="report-modal-content" style="display:flex; flex-direction:column; gap:16px;">
        <!-- Populated by JavaScript -->
      </div>
      <div style="display:flex; justify-content:flex-end; gap:10px;">
        <button class="btn btn-secondary" onclick="window.print()">🖨️ Print Cheat Sheet</button>
        <button class="btn btn-primary" onclick="closeModal('report-modal')">Back to Arena</button>
      </div>
    </div>
  </div>

  <script>
    /* -------------------------------------------------------------
       DATABASE: All 100 Verified Questions
       ------------------------------------------------------------- */
    const QUESTION_BANK = __QUESTIONS_DATA__;

    /* -------------------------------------------------------------
       APPLICATION STATE
       ------------------------------------------------------------- */
    const State = {
      mode: "STUDY",             // STUDY | RUSH | SURVIVAL
      currentIndex: 0,
      filterCategory: "ALL",
      filteredQuestions: [],
      userAnswers: {},           // { [qId]: { selectedKey: 'A', isCorrect: true } }
      bookmarks: new Set(),
      streak: 0,
      lives: 3,
      currentStep: 0,
      audioEnabled: true,
      audioCtx: null,
      trauma: 0                  // For screen shake
    };

    /* -------------------------------------------------------------
       CANVAS PARTICLE ENGINE (Sparks & Confetti)
       ------------------------------------------------------------- */
    const canvas = document.getElementById('particle-canvas');
    const pCtx = canvas.getContext('2d');
    let particles = [];

    function resizeCanvas() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function spawnConfetti(originX, originY, count = 40) {
      const colors = ['#38bdf8', '#fbbf24', '#34d399', '#f472b6', '#a78bfa', '#f8fafc'];
      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 8 + 3;
        particles.push({
          x: originX,
          y: originY,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed - 2,
          size: Math.random() * 7 + 4,
          color: colors[Math.floor(Math.random() * colors.length)],
          rotation: Math.random() * 360,
          rotSpeed: (Math.random() - 0.5) * 12,
          alpha: 1,
          decay: Math.random() * 0.02 + 0.015
        });
      }
    }

    function renderParticles() {
      pCtx.clearRect(0, 0, canvas.width, canvas.height);
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.22; // gravity
        p.alpha -= p.decay;
        p.rotation += p.rotSpeed;

        if (p.alpha <= 0) {
          particles.splice(i, 1);
          continue;
        }

        pCtx.save();
        pCtx.globalAlpha = p.alpha;
        pCtx.translate(p.x, p.y);
        pCtx.rotate((p.rotation * Math.PI) / 180);
        pCtx.fillStyle = p.color;
        pCtx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.6);
        pCtx.restore();
      }
      requestAnimationFrame(renderParticles);
    }
    renderParticles();

    /* -------------------------------------------------------------
       GAME FEEL: Trauma-Based Screen Shake
       ------------------------------------------------------------- */
    let shakeTime = 0;
    function addTrauma(amount) {
      State.trauma = Math.min(1.0, State.trauma + amount);
    }

    function updateShake() {
      if (State.trauma > 0) {
        State.trauma = Math.max(0, State.trauma - 0.05);
        const shake = State.trauma * State.trauma;
        shakeTime += 0.3;
        const offsetX = Math.sin(shakeTime * 3) * 12 * shake;
        const offsetY = Math.cos(shakeTime * 4) * 8 * shake;
        const rot = Math.sin(shakeTime * 2) * 1.5 * shake;
        document.getElementById('arena-root').style.transform = `translate(${offsetX}px, ${offsetY}px) rotate(${rot}deg)`;
      } else {
        document.getElementById('arena-root').style.transform = 'none';
      }
      requestAnimationFrame(updateShake);
    }
    updateShake();

    /* -------------------------------------------------------------
       AUDIO ENGINE: Rich Web Audio Synthesizer (Mechanical & Synths)
       ------------------------------------------------------------- */
    function getAudioContext() {
      if (!State.audioCtx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) State.audioCtx = new AudioCtx();
      }
      if (State.audioCtx && State.audioCtx.state === 'suspended') {
        State.audioCtx.resume();
      }
      return State.audioCtx;
    }

    function playSound(type) {
      if (!State.audioEnabled) return;
      try {
        const ctx = getAudioContext();
        if (!ctx) return;
        const now = ctx.currentTime;

        if (type === 'thock') {
          // Tactile mechanical switch click
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(450, now);
          osc.frequency.exponentialRampToValueAtTime(100, now + 0.05);
          gain.gain.setValueAtTime(0.12, now);
          gain.gain.linearRampToValueAtTime(0, now + 0.05);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.05);
        } else if (type === 'correct') {
          // Lush Major-7th chord arpeggio (C5, E5, G5, B5, C6)
          const notes = [523.25, 659.25, 783.99, 987.77, 1046.50];
          notes.forEach((freq, idx) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + idx * 0.05);
            gain.gain.setValueAtTime(0.12, now + idx * 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.05 + 0.35);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + idx * 0.05);
            osc.stop(now + idx * 0.05 + 0.35);
          });
        } else if (type === 'wrong') {
          // Sub-bass thud + dissonant interval
          [140, 98].forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(freq, now + i * 0.07);
            gain.gain.setValueAtTime(0.18, now + i * 0.07);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.2);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(now + i * 0.07);
            osc.stop(now + i * 0.07 + 0.2);
          });
        } else if (type === 'step') {
          // High-frequency subtle click
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(900, now);
          gain.gain.setValueAtTime(0.05, now);
          gain.gain.linearRampToValueAtTime(0, now + 0.025);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.025);
        }
      } catch (e) {}
    }

    function toggleAudio() {
      State.audioEnabled = !State.audioEnabled;
      const btn = document.getElementById('btn-audio');
      btn.innerText = State.audioEnabled ? '🔊' : '🔇';
      btn.classList.toggle('active', State.audioEnabled);
      if (State.audioEnabled) playSound('thock');
    }

    /* -------------------------------------------------------------
       SYNTAX HIGHLIGHTER
       ------------------------------------------------------------- */
    function escapeHTML(str) {
      return str.replace(/[&<>'"]/g, tag => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
      }[tag] || tag));
    }

    function highlightLineC(rawLine, trapToken) {
      let line = escapeHTML(rawLine);
      line = line.replace(/(\/\/.*$|\/\*.*?\*\/)/g, '<span class="tok-cmt">$1</span>');
      line = line.replace(/(^\s*#\s*[a-zA-Z_]+)/g, '<span class="tok-pre">$1</span>');
      line = line.replace(/(["'])(?:(?=(\\?))\2.)*?\1/g, '<span class="tok-str">$&</span>');
      line = line.replace(/\\b(int|char|float|double|void|long|short|unsigned|signed|size_t|ptrdiff_t)\\b/g, '<span class="tok-type">$1</span>');
      line = line.replace(/\\b(return|if|else|for|while|do|switch|case|default|break|continue|static|extern|const|volatile|sizeof|typedef|struct|union|enum)\\b/g, '<span class="tok-kw">$1</span>');
      line = line.replace(/\\b(0x[0-9a-fA-F]+|0[0-7]+|\\d+\\.?\\d*f?)\\b/g, '<span class="tok-num">$1</span>');

      if (trapToken && line.includes(trapToken)) {
        line = line.replaceAll(trapToken, `<mark class="trap-token">${trapToken}</mark>`);
      }
      return line;
    }

    /* -------------------------------------------------------------
       CORE RENDERING ENGINE
       ------------------------------------------------------------- */
    function getActiveQuestion() {
      return State.filteredQuestions[State.currentIndex] || QUESTION_BANK[0];
    }

    function renderQuestion() {
      const q = getActiveQuestion();
      if (!q) return;

      const catMap = {
        'TOPIC_DATATYPES': 'Data Types & Variables',
        'TOPIC_OPERATORS': 'Operators & Expressions',
        'TOPIC_CONDITIONALS': 'Conditionals',
        'TOPIC_LOOPS': 'Loops',
        'TOPIC_FUNCTIONS': 'Functions & Procedures',
        'TOPIC_ARRAYS': 'Arrays & Strings'
      };
      document.getElementById('q-category').innerText = catMap[q.category] || q.category.replace(/^TOPIC_|^CAT_/, '');
      const diffEl = document.getElementById('q-difficulty');
      diffEl.innerText = q.difficulty;
      diffEl.className = 'badge ' + q.difficulty.toLowerCase();
      document.getElementById('q-id-label').innerText = `${q.id} (Item ${State.currentIndex + 1} of ${State.filteredQuestions.length})`;
      document.getElementById('q-title-text').innerText = q.title;
      document.getElementById('q-prompt-text').innerText = q.prompt;

      const isBookmarked = State.bookmarks.has(q.id);
      document.getElementById('btn-bookmark').classList.toggle('active', isBookmarked);

      // Render Code Lines
      const lines = q.code.split('\\n');
      const viewer = document.getElementById('code-viewer');
      viewer.innerHTML = lines.map((line, idx) => {
        const lineNum = idx + 1;
        const isTrapLine = (q.trapInfo && q.trapInfo.line === lineNum);
        const trapToken = isTrapLine ? q.trapInfo.token : null;
        const formatted = highlightLineC(line, trapToken);
        const trapClass = isTrapLine ? 'trap-line' : '';
        return `<div class="code-line ${trapClass}" id="code-line-${lineNum}" data-line="${lineNum}">
          <span class="line-num">${lineNum}</span>
          <span class="line-text">${formatted}</span>
        </div>`;
      }).join('');

      // Render Options
      const optContainer = document.getElementById('options-container');
      const answered = State.userAnswers[q.id];

      optContainer.innerHTML = q.options.map(opt => {
        let cardClass = "option-card";
        if (answered) {
          cardClass += " locked";
          if (opt.isCorrect) cardClass += " correct";
          else if (answered.selectedKey === opt.key) cardClass += " wrong";
        }
        return `
          <div class="${cardClass}" onclick="selectOption('${opt.key}', event)">
            <div class="option-key">${opt.key}</div>
            <div class="option-text">${escapeHTML(opt.text)}</div>
          </div>
        `;
      }).join('');

      document.getElementById('btn-prev').disabled = (State.currentIndex === 0);
      document.getElementById('btn-next').disabled = (State.currentIndex === State.filteredQuestions.length - 1);

      document.getElementById('trap-spotlight-text').innerText = q.trapInfo.shortWarning || q.explanation.summary;

      // Distractor Breakdown
      const distContainer = document.getElementById('distractor-container');
      distContainer.innerHTML = q.options.map(opt => {
        const statusBadge = opt.isCorrect ? '<span style="color:var(--accent-green)">✅ Correct Answer</span>' : '<span style="color:var(--accent-red)">❌ Common Misconception</span>';
        const explanationText = opt.isCorrect ? opt.whyTempting : `${opt.whyTempting} <br><strong style="color:#f87171">Why it's wrong:</strong> ${opt.whyWrong || ''}`;
        return `
          <div class="distractor-item">
            <div class="distractor-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'flex' : 'none'">
              <span>Option ${opt.key}: <code>${escapeHTML(opt.text)}</code></span>
              <span>${statusBadge}</span>
            </div>
            <div class="distractor-body" style="display: ${answered && (answered.selectedKey === opt.key || opt.isCorrect) ? 'flex' : 'none'};">
              <div>${explanationText}</div>
            </div>
          </div>
        `;
      }).join('');

      document.getElementById('c-standard-ref').innerText = `ISO Standard: ${q.explanation.cStandardRef}`;

      const traces = q.executionTrace || [];
      const slider = document.getElementById('stepper-slider');
      slider.max = Math.max(0, traces.length - 1);
      State.currentStep = (answered ? traces.length - 1 : 0);
      slider.value = State.currentStep;
      renderStep();
      updateHeaderStats();
    }

    /* -------------------------------------------------------------
       STEPPER & MEMORY VISUALIZER
       ------------------------------------------------------------- */
    function renderStep() {
      const q = getActiveQuestion();
      const traces = q.executionTrace || [];
      if (traces.length === 0) {
        document.getElementById('step-description').innerText = "Execution trace unavailable for this question.";
        return;
      }

      const step = traces[State.currentStep] || traces[0];
      document.getElementById('step-description').innerHTML = `<strong>Step ${step.step} of ${traces.length} (Line ${step.line}):</strong> ${step.description}`;
      document.getElementById('stepper-slider').value = State.currentStep;

      document.querySelectorAll('.code-line').forEach(el => el.classList.remove('executing-line'));
      const activeLine = document.getElementById(`code-line-${step.line}`);
      if (activeLine) activeLine.classList.add('executing-line');

      // Memory Table
      const memBody = document.getElementById('mem-table-body');
      if (step.memorySnapshots && step.memorySnapshots.stack) {
        memBody.innerHTML = step.memorySnapshots.stack.map(cell => {
          const ptrNotice = cell.pointsTo ? ` ──▶ <span class="mem-ptr">${cell.pointsTo}</span>` : '';
          return `
            <tr>
              <td><strong>${escapeHTML(cell.name)}</strong></td>
              <td class="mem-addr">${cell.address}</td>
              <td class="mem-ptr">${escapeHTML(cell.type)}</td>
              <td class="mem-val">${escapeHTML(String(cell.value))}${ptrNotice}</td>
            </tr>
          `;
        }).join('');
      } else if (step.variables && Object.keys(step.variables).length > 0) {
        memBody.innerHTML = Object.entries(step.variables).map(([k, v]) => `
          <tr>
            <td><strong>${escapeHTML(k)}</strong></td>
            <td class="mem-addr">0x7FFF..</td>
            <td class="mem-ptr">auto</td>
            <td class="mem-val">${escapeHTML(String(v))}</td>
          </tr>
        `).join('');
      } else {
        memBody.innerHTML = `<tr><td colspan="4" style="color:var(--text-dim); text-align:center;">No local variables active on line ${step.line}.</td></tr>`;
      }
    }

    function stepNext() {
      const q = getActiveQuestion();
      const traces = q.executionTrace || [];
      if (State.currentStep < traces.length - 1) {
        State.currentStep++;
        playSound('step');
        renderStep();
      }
    }

    function stepPrev() {
      if (State.currentStep > 0) {
        State.currentStep--;
        playSound('step');
        renderStep();
      }
    }

    function stepReset() {
      State.currentStep = 0;
      playSound('step');
      renderStep();
    }

    function stepToEnd() {
      const q = getActiveQuestion();
      const traces = q.executionTrace || [];
      State.currentStep = Math.max(0, traces.length - 1);
      playSound('step');
      renderStep();
    }

    function onSliderChange(val) {
      State.currentStep = parseInt(val, 10);
      playSound('step');
      renderStep();
    }

    /* -------------------------------------------------------------
       USER INTERACTIONS WITH JUICE
       ------------------------------------------------------------- */
    function selectOption(key, event) {
      const q = getActiveQuestion();
      if (State.userAnswers[q.id]) return;

      const opt = q.options.find(o => o.key === key);
      const isCorrect = opt ? opt.isCorrect : false;

      State.userAnswers[q.id] = { selectedKey: key, isCorrect: isCorrect };

      if (isCorrect) {
        playSound('correct');
        State.streak++;
        
        // Spawn particle explosion at click coordinates
        const x = event ? event.clientX : window.innerWidth / 3;
        const y = event ? event.clientY : window.innerHeight / 2;
        spawnConfetti(x, y, 45);

        // Pop streak stat badge
        const streakEl = document.getElementById('stat-streak');
        streakEl.classList.add('pop');
        setTimeout(() => streakEl.classList.remove('pop'), 200);

      } else {
        playSound('wrong');
        addTrauma(0.45); // Screen shake!
        State.streak = 0;

        if (State.mode === 'SURVIVAL') {
          State.lives--;
          if (State.lives <= 0) {
            setTimeout(() => alert("💀 Out of lives! Check your missed traps in the study summary!"), 150);
          }
        }
      }

      saveStorage();
      renderQuestion();
    }

    function nextQuestion() {
      playSound('thock');
      if (State.currentIndex < State.filteredQuestions.length - 1) {
        State.currentIndex++;
        renderQuestion();
      }
    }

    function prevQuestion() {
      playSound('thock');
      if (State.currentIndex > 0) {
        State.currentIndex--;
        renderQuestion();
      }
    }

    function toggleBookmark() {
      const q = getActiveQuestion();
      if (State.bookmarks.has(q.id)) {
        State.bookmarks.delete(q.id);
      } else {
        State.bookmarks.add(q.id);
      }
      playSound('thock');
      saveStorage();
      renderQuestion();
    }

    function setCategoryFilter(cat) {
      State.filterCategory = cat;
      playSound('thock');

      document.querySelectorAll('.filter-chip').forEach(el => {
        el.classList.toggle('active', el.dataset.cat === cat);
      });

      if (cat === 'ALL') {
        State.filteredQuestions = [...QUESTION_BANK];
      } else if (cat === 'BOOKMARKED') {
        State.filteredQuestions = QUESTION_BANK.filter(q => State.bookmarks.has(q.id));
        if (State.filteredQuestions.length === 0) {
          alert("No bookmarked questions yet! Click the ⭐ button on tricky questions to save them here.");
          State.filteredQuestions = [...QUESTION_BANK];
        }
      } else {
        State.filteredQuestions = QUESTION_BANK.filter(q => q.category === cat);
      }

      State.currentIndex = 0;
      renderQuestion();
    }

    function setMode(mode) {
      State.mode = mode;
      playSound('thock');
      document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(`mode-${mode.toLowerCase()}`).classList.add('active');

      const livesPill = document.getElementById('stat-lives');
      if (mode === 'SURVIVAL') {
        State.lives = 3;
        livesPill.style.display = 'flex';
        livesPill.innerText = '❤️❤️❤️';
      } else {
        livesPill.style.display = 'none';
      }

      if (mode === 'RUSH') {
        State.filteredQuestions = [...QUESTION_BANK].sort(() => 0.5 - Math.random()).slice(0, 30);
      } else {
        setCategoryFilter(State.filterCategory);
      }

      State.currentIndex = 0;
      renderQuestion();
    }

    function updateHeaderStats() {
      document.getElementById('stat-counter').innerText = `${State.currentIndex + 1} / ${State.filteredQuestions.length}`;
      document.getElementById('stat-streak').innerText = `🔥 ${State.streak}`;
      
      const answeredKeys = Object.keys(State.userAnswers);
      if (answeredKeys.length === 0) {
        document.getElementById('stat-score').innerText = '0%';
      } else {
        const correctCount = answeredKeys.filter(id => State.userAnswers[id].isCorrect).length;
        const pct = Math.round((correctCount / answeredKeys.length) * 100);
        document.getElementById('stat-score').innerText = `${pct}%`;
      }

      if (State.mode === 'SURVIVAL') {
        const hearts = '❤️'.repeat(Math.max(0, State.lives)) + '🖤'.repeat(Math.max(0, 3 - State.lives));
        document.getElementById('stat-lives').innerText = hearts;
      }
    }

    /* -------------------------------------------------------------
       MODALS
       ------------------------------------------------------------- */
    function openShortcutsModal() {
      playSound('thock');
      document.getElementById('shortcuts-modal').classList.add('open');
    }

    function openReportModal() {
      playSound('thock');
      const modal = document.getElementById('report-modal');
      const content = document.getElementById('report-modal-content');

      const answeredIds = Object.keys(State.userAnswers);
      const correct = answeredIds.filter(id => State.userAnswers[id].isCorrect);
      const wrong = answeredIds.filter(id => !State.userAnswers[id].isCorrect);

      content.innerHTML = `
        <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:12px;">
          <div class="stat-pill" style="justify-content:center; flex-direction:column; padding:12px;">
            <span style="font-size:26px; font-weight:800; color:var(--accent-blue);">${answeredIds.length}</span>
            <span style="font-size:11px; color:var(--text-dim);">Questions Answered</span>
          </div>
          <div class="stat-pill" style="justify-content:center; flex-direction:column; padding:12px;">
            <span style="font-size:26px; font-weight:800; color:var(--accent-green);">${correct.length}</span>
            <span style="font-size:11px; color:var(--text-dim);">Correct Answers</span>
          </div>
          <div class="stat-pill" style="justify-content:center; flex-direction:column; padding:12px;">
            <span style="font-size:26px; font-weight:800; color:var(--accent-red);">${wrong.length}</span>
            <span style="font-size:11px; color:var(--text-dim);">Traps Triggered</span>
          </div>
        </div>

        <h3 style="font-size:15px; font-weight:700; color:var(--text-main); margin-top:8px;">Missed Questions for Review</h3>
        <div style="display:flex; flex-direction:column; gap:8px; max-height:300px; overflow-y:auto;">
          ${wrong.length === 0 ? '<div style="color:var(--text-dim); font-size:13px;">No missed questions yet. Keep practicing!</div>' : wrong.map(id => {
            const q = QUESTION_BANK.find(item => item.id === id);
            return `
              <div class="distractor-item" style="padding:12px 16px;">
                <strong>${q.id}: ${q.title}</strong>
                <div style="font-size:12px; color:var(--accent-amber); margin-top:4px;">⚠️ ${q.trapInfo.shortWarning}</div>
                <div style="font-size:11.5px; color:var(--text-dim); margin-top:3px;">${q.explanation.summary}</div>
              </div>
            `;
          }).join('')}
        </div>
      `;

      modal.classList.add('open');
    }

    function closeModal(id) {
      playSound('thock');
      document.getElementById(id).classList.remove('open');
    }

    function closeModalOnOuter(e, id) {
      if (e.target.id === id) closeModal(id);
    }

    /* -------------------------------------------------------------
       LOCAL STORAGE
       ------------------------------------------------------------- */
    function saveStorage() {
      try {
        localStorage.setItem("C_MIDTERM_ARENA_V2", JSON.stringify({
          answers: State.userAnswers,
          bookmarks: Array.from(State.bookmarks),
          streak: State.streak
        }));
      } catch (e) {}
    }

    function loadStorage() {
      try {
        const raw = localStorage.getItem("C_MIDTERM_ARENA_V2");
        if (raw) {
          const parsed = JSON.parse(raw);
          State.userAnswers = parsed.answers || {};
          State.bookmarks = new Set(parsed.bookmarks || []);
          State.streak = parsed.streak || 0;
        }
      } catch (e) {}
    }

    /* -------------------------------------------------------------
       KEYBOARD SHORTCUTS
       ------------------------------------------------------------- */
    window.addEventListener('keydown', e => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

      const key = e.key.toUpperCase();
      if (['1', 'A'].includes(key)) selectOption('A');
      else if (['2', 'B'].includes(key) && e.key !== 'b') selectOption('B');
      else if (['3', 'C'].includes(key)) selectOption('C');
      else if (['4', 'D'].includes(key)) selectOption('D');
      else if (e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        nextQuestion();
      } else if (e.key === 'ArrowRight') {
        stepNext();
      } else if (e.key === 'ArrowLeft') {
        stepPrev();
      } else if (e.key === 'b' || e.key === 'B') {
        toggleBookmark();
      } else if (e.key === 'm' || e.key === 'M') {
        toggleAudio();
      }
    });

    /* -------------------------------------------------------------
       INIT
       ------------------------------------------------------------- */
    loadStorage();
    State.filteredQuestions = [...QUESTION_BANK];
    renderQuestion();
  </script>
</body>
</html>
"""

final_html = html_template.replace("__QUESTIONS_DATA__", questions_json)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

with open("c_midterm_arena.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Generated ultra-juiced index.html ({len(final_html.encode('utf-8')) / 1024:.2f} KB)!")
