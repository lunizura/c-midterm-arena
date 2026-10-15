"""
create_pdf_guide.py
Generates the comprehensive 'C Midterm Survival Guide & Trap Cheat Sheet' PDF.
Uses modern print-CSS with exact A4 page breaks, callout boxes, code styling, and tables.
"""

import os
import subprocess
import sys

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>C Midterm Exam Survival Guide</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 14mm 14mm 14mm;
    @bottom-right {
      content: "Page " counter(page) " of " counter(pages);
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      font-size: 8.5pt;
      color: #64748b;
    }
  }

  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #0f172a;
    background: #ffffff;
    font-size: 9.2pt;
    line-height: 1.45;
    margin: 0;
    padding: 0;
  }

  /* Header Cover Banner */
  .doc-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 16px;
    border-left: 6px solid #38bdf8;
  }

  .doc-title {
    font-size: 19pt;
    font-weight: 900;
    letter-spacing: -0.5px;
    margin: 0 0 4px 0;
    color: #f8fafc;
  }

  .doc-subtitle {
    font-size: 10.5pt;
    font-weight: 500;
    color: #94a3b8;
    margin: 0 0 8px 0;
  }

  .badge-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }

  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .badge-blue { background: #0284c7; color: #ffffff; }
  .badge-amber { background: #d97706; color: #ffffff; }
  .badge-emerald { background: #059669; color: #ffffff; }
  .badge-indigo { background: #4f46e5; color: #ffffff; }

  /* Section Containers */
  .section {
    margin-bottom: 18px;
    page-break-inside: avoid;
  }

  .page-break {
    page-break-before: always;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 5px;
    margin-bottom: 10px;
    margin-top: 14px;
  }

  .section-number {
    background: #0f172a;
    color: #38bdf8;
    font-size: 10pt;
    font-weight: 800;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .section-title {
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
    letter-spacing: -0.2px;
  }

  /* Grid Layouts */
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 10px;
  }

  /* Cards */
  .card {
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 12px;
    background: #f8fafc;
    margin-bottom: 8px;
    page-break-inside: avoid;
  }

  .card-what {
    border-left: 4px solid #0284c7;
    background: #f0f9ff;
  }

  .card-trap {
    border-left: 4px solid #ea580c;
    background: #fff7ed;
  }

  .card-header-what {
    font-weight: 800;
    font-size: 9pt;
    color: #0369a1;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
  }

  .card-header-trap {
    font-weight: 800;
    font-size: 9pt;
    color: #c2410c;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 4px;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 6px 0 10px 0;
  }

  th {
    background: #1e293b;
    color: #ffffff;
    font-weight: 700;
    text-align: left;
    padding: 5px 8px;
    border: 1px solid #1e293b;
  }

  td {
    padding: 4.5px 8px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }

  tr:nth-child(even) td {
    background: #f1f5f9;
  }

  /* Code Blocks */
  code {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.8pt;
    background: #e2e8f0;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
  }

  pre {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.2pt;
    line-height: 1.35;
    background: #0f172a;
    color: #f8fafc;
    padding: 8px 10px;
    border-radius: 5px;
    margin: 5px 0;
    overflow-x: auto;
  }

  .tok-kw { color: #f43f5e; font-weight: bold; }
  .tok-type { color: #38bdf8; font-weight: bold; }
  .tok-num { color: #a78bfa; }
  .tok-str { color: #34d399; }
  .tok-cmt { color: #94a3b8; font-style: italic; }
  .tok-trap { background: #78350f; color: #fde047; padding: 1px 3px; border-radius: 2px; font-weight: bold; }

  /* Checklist Box */
  .checklist {
    background: #f8fafc;
    border: 1px solid #94a3b8;
    border-radius: 6px;
    padding: 12px 14px;
    margin-top: 10px;
  }

  .check-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 6px;
    font-size: 9pt;
  }

  .check-num {
    background: #0284c7;
    color: white;
    font-size: 7.5pt;
    font-weight: 800;
    padding: 1px 6px;
    border-radius: 3px;
    margin-top: 2px;
    flex-shrink: 0;
  }

  .tag-right {
    color: #15803d;
    font-weight: 700;
  }

  .tag-wrong {
    color: #b91c1c;
    font-weight: 700;
  }
</style>
</head>
<body>

  <!-- DOCUMENT HEADER -->
  <div class="doc-header">
    <h1 class="doc-title">⚡ C MIDTERM EXAM SURVIVAL GUIDE</h1>
    <div class="doc-subtitle">Konsep Pemrograman (CS101) &bull; High-Yield Topic Cheatsheet & Trap Breakdown</div>
    <div class="badge-row">
      <span class="badge badge-blue">ISO C99/C11 Standard</span>
      <span class="badge badge-amber">100% Calibrated to 6 Midterm Modules</span>
      <span class="badge badge-emerald">Multiple Choice Trap Defense</span>
      <span class="badge badge-indigo">Quick Reference</span>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- MODULE 1: DATA TYPES & VARIABLES -->
  <!-- ============================================================== -->
  <div class="section">
    <div class="section-header">
      <div class="section-number">1</div>
      <h2 class="section-title">Data Types &amp; Variables (Module 1)</h2>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width:18%;">Type</th>
          <th style="width:12%;">Bytes</th>
          <th style="width:12%;">Format</th>
          <th style="width:28%;">Value Range (32/64-bit OS)</th>
          <th style="width:30%;">Key Exam Behavior</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>char</code></td>
          <td>1 byte</td>
          <td><code>%c</code> / <code>%d</code></td>
          <td>-128 to 127 (or 0 to 255)</td>
          <td>Stored as ASCII integer. Arithmetic with <code>'0'</code> converts digit char to int.</td>
        </tr>
        <tr>
          <td><code>int</code></td>
          <td>4 bytes</td>
          <td><code>%d</code> / <code>%i</code></td>
          <td>-2,147,483,648 to 2,147,483,647</td>
          <td>Default integer type. Overflow wraps around on two's complement.</td>
        </tr>
        <tr>
          <td><code>unsigned int</code></td>
          <td>4 bytes</td>
          <td><code>%u</code></td>
          <td>0 to 4,294,967,295</td>
          <td>Cannot be negative. <code>0u - 1u</code> wraps around to maximum <code>4294967295</code>.</td>
        </tr>
        <tr>
          <td><code>float</code></td>
          <td>4 bytes</td>
          <td><code>%f</code></td>
          <td>&plusmn;3.4 &times; 10<sup>38</sup> (~6-7 dec digits)</td>
          <td>Single precision. Float literals need suffix <code>f</code> (e.g. <code>3.14f</code>).</td>
        </tr>
        <tr>
          <td><code>double</code></td>
          <td>8 bytes</td>
          <td><code>%f</code> / <code>%lf</code></td>
          <td>&plusmn;1.7 &times; 10<sup>308</sup> (~15-17 dec digits)</td>
          <td>Default for float literals (e.g. <code>3.14</code>). In <code>scanf</code>, MUST use <code>%lf</code>!</td>
        </tr>
      </tbody>
    </table>

    <div class="two-col">
      <!-- What It Does -->
      <div class="card card-what">
        <div class="card-header-what">💡 WHAT TO REMEMBER</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Format Specifier Precision:</strong> <code>%.2f</code> rounds output to 2 decimal places. <code>%5d</code> pads with spaces to width 5.</li>
          <li><strong>ASCII Math:</strong> <code>'5' - '0' == 5</code>. <code>'A' + 32 == 'a'</code>. Characters are directly swappable with integer codes.</li>
          <li><strong><code>const</code> Qualifier:</strong> Declares read-only variables. Reassignment causes a compile error.</li>
          <li><strong>Scope:</strong> Inner <code>{ ... }</code> blocks can declare variables with the same name, shadowing outer variables until the block closes.</li>
        </ul>
      </div>

      <!-- What to Look Out For (Traps) -->
      <div class="card card-trap">
        <div class="card-header-trap">⚠️ TRAPS TO WATCH OUT FOR (PROFESSOR FAVORITES)</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Integer Division Truncation:</strong><br>
            <code>double x = 5 / 2;</code> &rarr; Stores <span class="tag-wrong">2.0</span>, NOT 2.5!<br>
            <em>Why:</em> Both <code>5</code> and <code>2</code> are ints, so <code>5/2</code> truncates to int <code>2</code> before assigning.
          </li>
          <li><strong>Casting Order:</strong><br>
            <code>(double)(5 / 2) == 2.0</code> (parentheses divide first!)<br>
            <code>(double)5 / 2 == 2.5</code> (5 becomes 5.0 first!)
          </li>
          <li><strong>Float Literal Equality:</strong><br>
            <code>float f = 0.1f; if (f == 0.1)</code> &rarr; <span class="tag-wrong">FALSE!</span><br>
            <em>Why:</em> <code>0.1</code> is a double. 0.1 has no exact binary representation, so 32-bit float and 64-bit double differ slightly!
          </li>
        </ul>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- MODULE 2: OPERATORS & EXPRESSIONS -->
  <!-- ============================================================== -->
  <div class="section">
    <div class="section-header">
      <div class="section-number">2</div>
      <h2 class="section-title">Operators &amp; Expressions (Module 2)</h2>
    </div>

    <!-- Precedence Table -->
    <table>
      <thead>
        <tr>
          <th style="width:8%;">Prec</th>
          <th style="width:25%;">Operators</th>
          <th style="width:32%;">Description</th>
          <th style="width:15%;">Associativity</th>
          <th style="width:20%;">Sneaky Exam Trap</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1 (High)</strong></td>
          <td><code>()  []  -&gt;  .  x++  x--</code></td>
          <td>Postfix, array subscript, parens</td>
          <td>Left-to-Right</td>
          <td><code>x++</code> returns OLD value first!</td>
        </tr>
        <tr>
          <td><strong>2</strong></td>
          <td><code>++x  --x  +  -  !  ~  (type)  sizeof</code></td>
          <td>Unary operators, prefix inc/dec, cast</td>
          <td><strong>Right-to-Left</strong></td>
          <td><code>sizeof</code> doesn't evaluate side-effects!</td>
        </tr>
        <tr>
          <td><strong>3</strong></td>
          <td><code>*  /  %</code></td>
          <td>Multiplicative (multiply, divide, mod)</td>
          <td>Left-to-Right</td>
          <td><code>%</code> only valid on integers!</td>
        </tr>
        <tr>
          <td><strong>4</strong></td>
          <td><code>+  -</code></td>
          <td>Additive (binary addition, subtraction)</td>
          <td>Left-to-Right</td>
          <td>Higher precedence than shifts!</td>
        </tr>
        <tr>
          <td><strong>5</strong></td>
          <td><code>&lt;&lt;  &gt;&gt;</code></td>
          <td>Bitwise left &amp; right shifts</td>
          <td>Left-to-Right</td>
          <td><code>1 &lt;&lt; 2 + 3</code> is <code>1 &lt;&lt; (2+3) = 32</code>!</td>
        </tr>
        <tr>
          <td><strong>6</strong></td>
          <td><code>&lt;  &lt;=  &gt;  &gt;=</code></td>
          <td>Relational comparisons</td>
          <td>Left-to-Right</td>
          <td><code>1 &lt; x &lt; 10</code> does NOT check range!</td>
        </tr>
        <tr>
          <td><strong>7</strong></td>
          <td><code>==  !=</code></td>
          <td>Equality checks</td>
          <td>Left-to-Right</td>
          <td>Don't confuse with assignment <code>=</code>!</td>
        </tr>
        <tr>
          <td><strong>8–10</strong></td>
          <td><code>&amp;</code> then <code>^</code> then <code>|</code></td>
          <td>Bitwise AND, XOR, OR</td>
          <td>Left-to-Right</td>
          <td>Lower precedence than <code>==</code>!</td>
        </tr>
        <tr>
          <td><strong>11</strong></td>
          <td><code>&amp;&amp;</code></td>
          <td>Logical AND</td>
          <td>Left-to-Right</td>
          <td><strong>Short-circuits:</strong> stops if left is 0!</td>
        </tr>
        <tr>
          <td><strong>12</strong></td>
          <td><code>||</code></td>
          <td>Logical OR</td>
          <td>Left-to-Right</td>
          <td><strong>Short-circuits:</strong> stops if left is 1!</td>
        </tr>
        <tr>
          <td><strong>13</strong></td>
          <td><code>?:</code></td>
          <td>Ternary conditional</td>
          <td><strong>Right-to-Left</strong></td>
          <td><code>a ? b : c ? d : e</code> groups right-to-left.</td>
        </tr>
        <tr>
          <td><strong>14 (Low)</strong></td>
          <td><code>=  +=  -=  *=  /=  %=</code></td>
          <td>Assignment &amp; augmented assignment</td>
          <td><strong>Right-to-Left</strong></td>
          <td><code>x *= y + 1</code> means <code>x = x * (y + 1)</code>!</td>
        </tr>
      </tbody>
    </table>

    <div class="two-col">
      <div class="card card-what">
        <div class="card-header-what">💡 CORE MECHANICS TO REMEMBER</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Pre vs Post Increment:</strong><br>
            <code>int a = 5; int b = a++;</code> &rarr; <code>b = 5, a = 6</code> (old value copied).<br>
            <code>int a = 5; int b = ++a;</code> &rarr; <code>b = 6, a = 6</code> (incremented first).
          </li>
          <li><strong>Modulo Sign Rule:</strong> In C99, <code>a % b</code> ALWAYS takes the sign of the LEFT operand <code>a</code>:<br>
            <code>-7 % 3 == -1</code> &bull; <code>7 % -3 == 1</code> &bull; <code>-7 % -3 == -1</code>.
          </li>
        </ul>
      </div>

      <div class="card card-trap">
        <div class="card-header-trap">⚠️ SHORT-CIRCUIT &amp; COMPOUND TRAPS</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Short-Circuit Skipping Side Effects:</strong><br>
            <pre><code>int a = 0, b = 5;
if (a && ++b) { }
printf("%d", b); // PRINTS 5, NOT 6! (++b never ran!)</code></pre>
          </li>
          <li><strong>Compound Assignment Right-Hand Precedence:</strong><br>
            <code>x *= y + 3;</code> is parsed as <code>x = x * (y + 3)</code>, NOT <code>(x * y) + 3</code>!
          </li>
          <li><strong>Chained Comparisons Myth:</strong><br>
            <code>if (5 &lt; x &lt; 2)</code> evaluates <code>(5 &lt; x)</code> to <code>0</code> or <code>1</code>, and then compares <code>0 &lt; 2</code> (always true)!
          </li>
        </ul>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ============================================================== -->
  <!-- MODULE 3: CONDITIONALS (IF / SWITCH) -->
  <!-- ============================================================== -->
  <div class="section">
    <div class="section-header">
      <div class="section-number">3</div>
      <h2 class="section-title">Conditionals: if, else &amp; switch (Module 3)</h2>
    </div>

    <div class="two-col">
      <!-- What It Does -->
      <div class="card card-what">
        <div class="card-header-what">💡 HOW CONDITIONALS WORK IN C</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Boolean Truth Value:</strong> In C, there is no separate primitive bool type in standard C90. <strong>Any non-zero value is TRUE</strong> (e.g. <code>1</code>, <code>-42</code>, <code>999</code>). Exactly <strong><code>0</code> is FALSE</strong>.</li>
          <li><strong>Switch Structure:</strong> Evaluates an integer or character expression once, then jumps to the matching <code>case</code> label.</li>
          <li><strong>Case Label Requirements:</strong> Each <code>case</code> MUST be a compile-time constant integer or char (e.g. <code>case 1:</code>, <code>case 'A':</code>). You CANNOT use variables like <code>case x:</code>!</li>
          <li><strong>Ternary Operator:</strong> <code>condition ? expr_if_true : expr_if_false</code> returns an expression value.</li>
        </ul>
      </div>

      <!-- Traps -->
      <div class="card card-trap">
        <div class="card-header-trap">⚠️ EXAM TRAPS: 4 CLASSIC SNEAKY BUGS</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>1. The Assignment in Condition Trap:</strong><br>
            <code>if (x = 5) { ... }</code> &rarr; <span class="tag-wrong">ALWAYS TRUE!</span><br>
            <em>Why:</em> Uses single <code>=</code> (assignment), NOT <code>==</code>. Sets <code>x = 5</code>, which evaluates to 5 (non-zero = true).
          </li>
          <li><strong>2. The Accidental Semicolon:</strong><br>
            <code>if (score &gt; 90); { printf("Passed"); }</code><br>
            <em>Why:</em> The semicolon immediately ends the <code>if</code>! The block following it runs UNCONDITIONALLY!
          </li>
          <li><strong>3. Dangling Else Binding:</strong><br>
            In C, an <code>else</code> always binds to the <strong>closest preceding unmatched <code>if</code></strong>, regardless of code indentation!
          </li>
          <li><strong>4. Switch Fallthrough without Break:</strong><br>
            Once a <code>case</code> matches, ALL subsequent cases execute sequentially until a <code>break;</code> is encountered!
          </li>
        </ul>
      </div>
    </div>

    <!-- Visual Example of Dangling Else and Switch Fallthrough -->
    <div class="two-col">
      <div class="card" style="background:#0f172a; color:#f8fafc;">
        <span style="color:#38bdf8; font-weight:bold; font-size:8.5pt;">Dangling Else Reality Check:</span>
        <pre><code>int a = 1, b = 0;
if (a &gt; 0)
    if (b &gt; 0)
        printf("A");
else // &lt;-- BINDS TO if (b &gt; 0), NOT if (a &gt; 0)!
    printf("B");
// OUTPUT: "B" is printed!</code></pre>
      </div>

      <div class="card" style="background:#0f172a; color:#f8fafc;">
        <span style="color:#fbbf24; font-weight:bold; font-size:8.5pt;">Switch Fallthrough Reality Check:</span>
        <pre><code>int x = 2;
switch(x) {
    case 1: printf("1");
    case 2: printf("2"); // Matches here!
    case 3: printf("3"); // Falls through!
    default: printf("D"); // Falls through!
}
// OUTPUT: Prints "23D" because breaks are missing!</code></pre>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- MODULE 4: LOOPS (FOR / WHILE / DO-WHILE) -->
  <!-- ============================================================== -->
  <div class="section">
    <div class="section-header">
      <div class="section-number">4</div>
      <h2 class="section-title">Loops &amp; Iteration (Module 4)</h2>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width:20%;">Loop Type</th>
          <th style="width:25%;">Syntax</th>
          <th style="width:20%;">Condition Check</th>
          <th style="width:15%;">Min Iterations</th>
          <th style="width:20%;">Typical Use Case</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong><code>for</code> loop</strong></td>
          <td><code>for (init; cond; step)</code></td>
          <td>Pre-tested (before body)</td>
          <td><strong>0</strong> times</td>
          <td>Known iteration count, array traversal.</td>
        </tr>
        <tr>
          <td><strong><code>while</code> loop</strong></td>
          <td><code>while (cond) { ... }</code></td>
          <td>Pre-tested (before body)</td>
          <td><strong>0</strong> times</td>
          <td>Event-driven, unknown loop count.</td>
        </tr>
        <tr>
          <td><strong><code>do-while</code> loop</strong></td>
          <td><code>do { ... } while (cond);</code></td>
          <td><strong>Post-tested</strong> (after body)</td>
          <td><strong>1 time (Guaranteed)</strong></td>
          <td>Menu prompts, user input validation.</td>
        </tr>
      </tbody>
    </table>

    <div class="two-col">
      <div class="card card-what">
        <div class="card-header-what">💡 BREAK vs CONTINUE MECHANICS</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong><code>break;</code></strong>: Terminates the innermost loop or switch statement immediately. Execution jumps to the statement following the loop.</li>
          <li><strong><code>continue;</code></strong>: Skips the remaining code in the <em>current</em> iteration:
            <ul>
              <li>In <code>for</code>: Jumps straight to the <strong>step expression</strong> (e.g. <code>i++</code>), then evaluates condition.</li>
              <li>In <code>while</code> / <code>do-while</code>: Jumps directly to the <strong>condition test</strong>.</li>
            </ul>
          </li>
          <li><strong>Do-While Semicolon:</strong> The <code>do { ... } while (cond);</code> loop MUST end with a semicolon <code>;</code>.</li>
        </ul>
      </div>

      <div class="card card-trap">
        <div class="card-header-trap">⚠️ THE 4 DEADLIEST LOOP TRAPS</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>1. The Empty Body Semicolon:</strong><br>
            <code>for (int i = 0; i &lt; 5; i++);</code> &rarr; The loop does nothing 5 times! Semicolon acts as empty body. Block after runs once with <code>i = 5</code>!
          </li>
          <li><strong>2. While Loop Continue Freeze:</strong><br>
            If you call <code>continue</code> before incrementing <code>i++</code> in a <code>while</code> loop, <code>i</code> never changes &rarr; <span class="tag-wrong">INFINITE LOOP!</span>
          </li>
          <li><strong>3. Unsigned Backward Loop:</strong><br>
            <code>for (unsigned int i = 3; i &gt;= 0; i--)</code><br>
            When <code>i = 0</code> decrements, it wraps to <code>4294967295</code> &gt;= 0 &rarr; <span class="tag-wrong">NEVER TERMINATES!</span>
          </li>
          <li><strong>4. Post-Increment in Test:</strong><br>
            <code>while (i++ &lt; 3)</code> tests <code>i &lt; 3</code>, but increments <code>i</code> regardless of true/false!
          </li>
        </ul>
      </div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ============================================================== -->
  <!-- MODULE 5: FUNCTIONS & PROCEDURES -->
  <!-- ============================================================== -->
  <div class="section">
    <div class="section-header">
      <div class="section-number">5</div>
      <h2 class="section-title">Functions &amp; Procedures (Module 5)</h2>
    </div>

    <div class="two-col">
      <div class="card card-what">
        <div class="card-header-what">💡 FUNCTION CONCEPTS &amp; DEFINITIONS</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Prototype (Declaration):</strong> <code>int add(int a, int b);</code> informs the compiler about return type and parameters before <code>main()</code>.</li>
          <li><strong>Definition:</strong> Contains the actual body of the function.</li>
          <li><strong>Function vs Procedure:</strong> In C, a "procedure" is simply a function with return type <code>void</code> (does not return a value).</li>
          <li><strong>Scope of Local Variables:</strong> Variables declared inside a function exist on the stack and are destroyed when the function returns.</li>
        </ul>
      </div>

      <div class="card card-trap">
        <div class="card-header-trap">⚠️ THE #1 EXAM CONCEPT: PASS-BY-VALUE!</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>C is STRICTLY Pass-by-Value:</strong><br>
            When arguments are passed, C copies their values into parameter variables. Modifications inside the callee do NOT affect the caller!
            <pre><code>void increment(int x) { x = x + 1; }
int main() {
    int val = 10;
    increment(val);
    printf("%d", val); // PRINTS 10, NOT 11!
}</code></pre>
          </li>
        </ul>
      </div>
    </div>

    <div class="two-col">
      <div class="card card-trap">
        <div class="card-header-trap">⚠️ STATIC LOCAL VARIABLE RETENTION</div>
        <p style="margin:0 0 6px 0;">A <code>static</code> local variable inside a function is <strong>initialized only ONCE</strong> and <strong>retains its value between function calls</strong>!</p>
        <pre><code>void counter() {
    static int c = 0; // Initialized once!
    c++;
    printf("%d ", c);
}
int main() {
    counter(); counter(); counter();
    // OUTPUT: 1 2 3 (NOT 1 1 1!)
}</code></pre>
      </div>

      <div class="card card-what">
        <div class="card-header-what">💡 HOW TO TRACE RECURSION ON EXAMS</div>
        <p style="margin:0 0 6px 0;">Always draw an activation tree downward, then return values upward:</p>
        <pre><code>int f(int n) {
    if (n &lt;= 1) return 1; // Base case
    return n * f(n - 1);
}
// Trace f(3):
// f(3) = 3 * f(2)
//   f(2) = 2 * f(1)
//     f(1) = 1 (Base case reached!)
//   f(2) = 2 * 1 = 2
// f(3) = 3 * 2 = 6</code></pre>
        <small style="color:#64748b;"><em>Watch out: Missing or unreachable base case causes Stack Overflow crash.</em></small>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- MODULE 6: ARRAYS & STRINGS -->
  <!-- ============================================================== -->
  <div class="section">
    <div class="section-header">
      <div class="section-number">6</div>
      <h2 class="section-title">Arrays &amp; Strings (Module 6)</h2>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width:22%;">Declaration</th>
          <th style="width:25%;">Memory Content</th>
          <th style="width:15%;">Valid Indices</th>
          <th style="width:38%;">Critical Exam Pitfall</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><code>int a[5];</code></td>
          <td>Garbage values (uninitialized)</td>
          <td><code>0, 1, 2, 3, 4</code></td>
          <td>Accessing <code>a[5]</code> is <strong>out of bounds</strong> (undefined behavior)!</td>
        </tr>
        <tr>
          <td><code>int a[5] = {1, 2};</code></td>
          <td><code>{1, 2, 0, 0, 0}</code></td>
          <td><code>0, 1, 2, 3, 4</code></td>
          <td><strong>Partial Init Zero-Padding:</strong> Unspecified elements become 0!</td>
        </tr>
        <tr>
          <td><code>int m[2][3];</code></td>
          <td>2 rows, 3 cols (6 elements)</td>
          <td><code>[0..1][0..2]</code></td>
          <td>Stored in <strong>Row-Major Order</strong> contiguously in memory.</td>
        </tr>
        <tr>
          <td><code>char s[6] = "hello";</code></td>
          <td><code>{'h','e','l','l','o','&#92;0'}</code></td>
          <td><code>0..5</code> (Length 5)</td>
          <td>Requires <strong>6 bytes</strong> to store the trailing null terminator <code>&#92;0</code>!</td>
        </tr>
        <tr>
          <td><code>char s[5] = "hello";</code></td>
          <td><code>{'h','e','l','l','o'}</code></td>
          <td><strong>NO NULL BYTE!</strong></td>
          <td><code>printf("%s", s)</code> will over-read memory until a random <code>&#92;0</code> is found!</td>
        </tr>
      </tbody>
    </table>

    <div class="two-col">
      <div class="card card-what">
        <div class="card-header-what">💡 SIZEOF vs STRLEN IN STRINGS</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong><code>sizeof(str)</code></strong>: Returns the <strong>total buffer size in bytes</strong> allocated to the array, regardless of string length.</li>
          <li><strong><code>strlen(str)</code></strong>: Counts the characters up to (but not including) the first null terminator <code>'&#92;0'</code>.</li>
          <li><em>Example:</em>
            <pre><code>char s[20] = "cat";
sizeof(s); // == 20 (array capacity)
strlen(s); // == 3  ('c', 'a', 't')</code></pre>
          </li>
        </ul>
      </div>

      <div class="card card-trap">
        <div class="card-header-trap">⚠️ 2D ARRAY INDEXING &amp; ROW-MAJOR ORDER</div>
        <ul style="margin:0; padding-left:16px;">
          <li><strong>Row vs Column:</strong> In <code>int arr[R][C]</code>, <code>R</code> is the number of rows, <code>C</code> is the number of columns. Element is <code>arr[row][col]</code>.</li>
          <li><strong>Memory Layout:</strong> Row 0 is stored first, immediately followed by Row 1 in linear memory:
            <pre><code>int m[2][2] = {{10, 20}, {30, 40}};
// In memory: [10][20][30][40]
// m[0][0]=10, m[0][1]=20, m[1][0]=30, m[1][1]=40</code></pre>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- 10 GOLDEN RULES CHECKLIST -->
  <!-- ============================================================== -->
  <div class="checklist">
    <div style="font-weight:900; font-size:11pt; color:#0f172a; margin-bottom:8px; display:flex; align-items:center; gap:6px;">
      <span>🏆 10 GOLDEN RULES TO MEMORIZE BEFORE ENTERING THE EXAM ROOM</span>
    </div>
    
    <div class="check-item">
      <span class="check-num">1</span>
      <div><strong>5 / 2 is 2, NOT 2.5:</strong> Dividing two integer literals always truncates fractional digits toward zero.</div>
    </div>
    <div class="check-item">
      <span class="check-num">2</span>
      <div><strong>Single '=' is assignment:</strong> <code>if (x = 5)</code> sets <code>x = 5</code> and evaluates to TRUE. Always check for double <code>==</code>.</div>
    </div>
    <div class="check-item">
      <span class="check-num">3</span>
      <div><strong>Semicolons kill branches and loops:</strong> Watch out for <code>if (...);</code>, <code>for (...);</code>, and <code>while (...);</code>. They create empty bodies.</div>
    </div>
    <div class="check-item">
      <span class="check-num">4</span>
      <div><strong>Switch falls through:</strong> Without a <code>break;</code> statement, execution continues into subsequent cases regardless of their labels.</div>
    </div>
    <div class="check-item">
      <span class="check-num">5</span>
      <div><strong>Logical operators short-circuit:</strong> In <code>0 &amp;&amp; f()</code> and <code>1 || f()</code>, the right-hand function or expression is NEVER evaluated.</div>
    </div>
    <div class="check-item">
      <span class="check-num">6</span>
      <div><strong>Post-increment returns the old value:</strong> <code>int y = x++;</code> gives <code>y</code> the value of <code>x</code> *before* it was incremented.</div>
    </div>
    <div class="check-item">
      <span class="check-num">7</span>
      <div><strong>C is strictly pass-by-value:</strong> Changes to ordinary parameters inside functions do not modify the caller's variables.</div>
    </div>
    <div class="check-item">
      <span class="check-num">8</span>
      <div><strong>Static local variables remember:</strong> <code>static int x = 0;</code> retains its value across function calls and initializes only once.</div>
    </div>
    <div class="check-item">
      <span class="check-num">9</span>
      <div><strong>Array bounds start at 0:</strong> An array of size 5 has valid elements <code>arr[0]</code> through <code>arr[4]</code>. <code>arr[5]</code> is illegal!</div>
    </div>
    <div class="check-item">
      <span class="check-num">10</span>
      <div><strong>Strings must have room for &#39;&#92;0&#39;:</strong> A 5-letter word requires an array of size at least 6 bytes to store the null terminator <code>&#92;0</code>.</div>
    </div>
  </div>

</body>
</html>
"""

# 1. Write HTML file
html_path = os.path.abspath("c_midterm_survival_guide.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML source at: {html_path}")

# 2. Paths for output PDFs
desktop_pdf = os.path.expanduser(r"~\Desktop\C_Midterm_Survival_Guide.pdf")
local_pdf = os.path.abspath("C_Midterm_Survival_Guide.pdf")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

print(f"Using Edge binary at: {edge_path}")

# 3. Compile to PDF via Edge Headless
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={local_pdf}",
    html_path
]

print("Running Edge headless print-to-pdf...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error during PDF compilation:", res.stderr)
    sys.exit(1)

# 4. Copy to Desktop
import shutil
shutil.copy2(local_pdf, desktop_pdf)
print(f"Successfully generated PDF Cheat Sheet at:")
print(f"  [1] Desktop: {desktop_pdf}")
print(f"  [2] Project: {local_pdf}")

# 5. Verify PDF with pypdf
import pypdf
reader = pypdf.PdfReader(local_pdf)
print(f"PDF verified! Total pages: {len(reader.pages)}")
