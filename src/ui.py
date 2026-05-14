def get_html():
  return r'''
  <!DOCTYPE html>
  <html lang="en" data-theme="light">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Pathfinding Visualizer</title>
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
      <style>
        :root,
        [data-theme="light"] {
          --bg:        #f0f4f8;
          --surface:   #ffffff;
          --border:    #cbd5e1;
          --green:     #059669;
          --green-dim: #047857;
          --cyan:      #0284c7;
          --amber:     #d97706;
          --red:       #dc2626;
          --purple:    #7c3aed;
          --text:      #1e293b;
          --text-dim:  #64748b;
          --mono:      'Share Tech Mono', monospace;
          --display:   'Orbitron', sans-serif;
          --c-empty:   #e8f0fe;
          --c-wall:    #1e293b;
          --c-start:   #059669;
          --c-end:     #dc2626;
          --c-visited: #bfdbfe;
          --c-path:    #f59e0b;
          --c-grid:    #cbd5e1;
          --tool-wall-bg:  rgba(30,41,59,0.08);
          --tool-wall-clr: #1e293b;
          --tool-wall-bdr: #1e293b;
        }

        [data-theme="dark"] {
          --bg:        #060a0f;
          --surface:   #0c1420;
          --border:    #1a2d45;
          --green:     #00ff88;
          --green-dim: #00c464;
          --cyan:      #00d4ff;
          --amber:     #ffb300;
          --red:       #ff3b3b;
          --purple:    #c084fc;
          --text:      #a8c4d8;
          --text-dim:  #94a3b8;
          --c-empty:   #0d1b2a;
          --c-wall:    #e2e8f0;
          --c-start:   #00ff88;
          --c-end:     #ff3b3b;
          --c-visited: #0d3352;
          --c-path:    #ffb300;
          --c-grid:    #111e2e;
          --tool-wall-bg:  rgba(226,232,240,0.08);
          --tool-wall-clr: #e2e8f0;
          --tool-wall-bdr: #94a3b8;
        }

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          background: var(--bg);
          color: var(--text);
          font-family: var(--mono);
          min-height: 100vh;
          overflow-x: hidden;
          transition: background 0.25s, color 0.25s;
        }

        [data-theme="dark"] body::after {
          content: '';
          position: fixed; inset: 0;
          background: repeating-linear-gradient(
            0deg, transparent, transparent 2px,
            rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px
          );
          pointer-events: none;
          z-index: 9999;
        }

        header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 14px 28px;
          border-bottom: 1px solid var(--border);
          background: var(--surface);
          position: sticky; top: 0; z-index: 100;
          transition: background 0.25s, border-color 0.25s;
          box-shadow: 0 1px 4px rgba(0,0,0,0.07);
        }
        .logo {
          font-family: var(--display);
          font-size: 1.05rem;
          font-weight: 900;
          letter-spacing: 0.15em;
          color: var(--green);
          transition: color 0.25s;
        }
        [data-theme="dark"] .logo { text-shadow: 0 0 20px rgba(0,255,136,0.4); }
        .logo span { color: var(--cyan); }

        .header-right { display: flex; align-items: center; gap: 20px; }
        .header-status {
          font-size: 0.71rem; color: var(--text-dim);
          letter-spacing: 0.09em; display: flex; gap: 20px;
        }
        .status-dot {
          display: inline-block; width: 6px; height: 6px;
          border-radius: 50%; background: var(--green);
          margin-right: 6px; animation: pulse 2s infinite;
        }
        [data-theme="dark"] .status-dot { box-shadow: 0 0 8px var(--green); }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

        .theme-toggle {
          display: flex; align-items: center; gap: 8px;
          cursor: pointer; font-size: 0.69rem;
          color: var(--text-dim); letter-spacing: 0.08em;
          user-select: none;
          padding: 5px 12px;
          border: 1px solid var(--border);
          border-radius: 20px;
          background: var(--bg);
          transition: all 0.2s;
          white-space: nowrap;
        }
        .theme-toggle:hover { border-color: var(--cyan); color: var(--cyan); }

        .toggle-track {
          width: 34px; height: 17px; border-radius: 9px;
          background: var(--border); position: relative;
          transition: background 0.25s; flex-shrink: 0;
        }
        [data-theme="dark"] .toggle-track { background: var(--green-dim); }
        .toggle-thumb {
          position: absolute; top: 2px; left: 2px;
          width: 13px; height: 13px; border-radius: 50%;
          background: var(--surface);
          box-shadow: 0 1px 3px rgba(0,0,0,0.3);
          transition: transform 0.25s;
        }
        [data-theme="dark"] .toggle-thumb { transform: translateX(17px); }

        .layout {
          display: grid;
          grid-template-columns: 254px 1fr 254px;
          height: calc(100vh - 53px);
        }

        .panel {
          background: var(--surface);
          border-right: 1px solid var(--border);
          padding: 18px 14px;
          display: flex; flex-direction: column; gap: 16px;
          overflow-y: auto;
          transition: background 0.25s, border-color 0.25s;
        }
        .panel:last-child { border-right: none; border-left: 1px solid var(--border); }
        .panel-title {
          font-family: var(--display); font-size: 0.58rem;
          letter-spacing: 0.2em; color: var(--text-dim);
          text-transform: uppercase; padding-bottom: 8px;
          border-bottom: 1px solid var(--border);
        }

        .row2 { display: flex; gap: 8px; }
        .row2 input {
          flex: 1; background: var(--bg); border: 1px solid var(--border);
          color: var(--text); font-family: var(--mono); font-size: 0.88rem;
          padding: 7px 10px; border-radius: 4px; text-align: center;
          transition: background 0.2s, border-color 0.2s, color 0.2s;
        }
        .row2 input:focus { outline: none; border-color: var(--green); }
        .label { font-size: 0.68rem; color: var(--text-dim); margin-bottom: 4px; letter-spacing: 0.08em; }

        .btn {
          font-family: var(--mono); font-size: 0.78rem; letter-spacing: 0.08em;
          padding: 9px 14px; border-radius: 4px; border: 1px solid;
          cursor: pointer; transition: all 0.15s; background: transparent;
          width: 100%; text-align: left;
        }
        .btn-green { color: var(--green);    border-color: var(--green-dim); }
        .btn-cyan  { color: var(--cyan);     border-color: var(--cyan);      }
        .btn-amber { color: var(--amber);    border-color: var(--amber);     }
        .btn-dim   { color: var(--text-dim); border-color: var(--border);    }
        .btn:hover { filter: brightness(1.15); transform: translateX(2px); }
        [data-theme="dark"] .btn:hover { filter: brightness(1.3); }
        .btn:disabled { opacity: 0.35; cursor: not-allowed; transform: none; }

        /* Run/Stop toggle button */
        .btn-run-stop {
          font-family: var(--mono); font-size: 0.82rem; letter-spacing: 0.08em;
          padding: 11px 14px; border-radius: 4px; border: 1px solid;
          cursor: pointer; transition: all 0.15s; background: transparent;
          width: 100%; text-align: center; margin-top: auto;
        }
        .btn-run-stop.state-run {
          color: var(--green); border-color: var(--green-dim);
        }
        .btn-run-stop.state-stop {
          color: var(--amber); border-color: var(--amber);
        }
        .btn-run-stop:hover { filter: brightness(1.2); transform: translateX(2px); }
        [data-theme="dark"] .btn-run-stop:hover { filter: brightness(1.35); }
        .btn-run-stop:disabled { opacity: 0.35; cursor: not-allowed; transform: none; }

        .tool-group { display: flex; flex-direction: column; gap: 5px; }
        .tool-btn {
          font-family: var(--mono); font-size: 0.75rem; padding: 8px 12px;
          border-radius: 4px; border: 1px solid var(--border);
          cursor: pointer; background: transparent; color: var(--text-dim);
          text-align: left; transition: all 0.15s; letter-spacing: 0.04em;
        }
        .tool-btn:hover { border-color: var(--text-dim); color: var(--text); }
        .tool-btn.active-wall {
          border-color: var(--tool-wall-bdr);
          background:   var(--tool-wall-bg);
          color:        var(--tool-wall-clr);
        }
        .tool-btn.active-start { border-color:var(--green); background:rgba(5,150,105,0.1);  color:var(--green); }
        .tool-btn.active-end   { border-color:var(--red);   background:rgba(220,38,38,0.08);  color:var(--red);   }
        .tool-btn.active-erase { border-color:var(--cyan);  background:rgba(2,132,199,0.08);  color:var(--cyan);  }
        [data-theme="dark"] .tool-btn.active-start { background:rgba(0,255,136,0.08); }
        [data-theme="dark"] .tool-btn.active-end   { background:rgba(255,59,59,0.08); }
        [data-theme="dark"] .tool-btn.active-erase { background:rgba(0,212,255,0.06); }

        .algo-list { display: flex; flex-direction: column; gap: 4px; }
        .algo-btn {
          font-family: var(--mono); font-size: 0.73rem; padding: 7px 10px;
          border-radius: 4px; border: 1px solid var(--border);
          cursor: pointer; background: transparent; color: var(--text-dim);
          text-align: left; transition: all 0.15s;
        }
        .algo-btn:hover { color: var(--text); border-color: var(--text-dim); }
        .algo-btn.selected {
          border-color: var(--cyan); color: var(--cyan);
          background: rgba(2,132,199,0.07);
        }
        [data-theme="dark"] .algo-btn.selected { background: rgba(0,212,255,0.05); }
        .algo-tag {
          font-family: var(--display); font-size: 0.58rem; font-weight: 700;
          letter-spacing: 0.1em; display: inline-block; min-width: 46px; margin-right: 6px;
        }

        .speed-wrap { display: flex; flex-direction: column; gap: 6px; }
        input[type=range] { width: 100%; accent-color: var(--green); }
        .speed-labels { display: flex; justify-content: space-between; font-size: 0.63rem; color: var(--text-dim); }

        .canvas-area {
          display: flex; flex-direction: column;
          align-items: center; justify-content: center;
          padding: 24px; overflow: auto; background: var(--bg);
          transition: background 0.25s;
        }
        #gridCanvas {
          cursor: crosshair; display: block; image-rendering: pixelated;
          border: 1px solid var(--border);
          box-shadow: 0 4px 24px rgba(0,0,0,0.1);
          transition: border-color 0.25s;
        }
        [data-theme="dark"] #gridCanvas {
          box-shadow: 0 0 40px rgba(0,255,136,0.04), 0 0 80px rgba(0,0,0,0.6);
        }
        .coords {
          margin-top: 10px; font-size: 0.68rem;
          color: var(--text-dim); letter-spacing: 0.08em; height: 16px;
        }

        .stat-row {
          display: flex; justify-content: space-between; align-items: baseline;
          padding: 5px 0; border-bottom: 1px solid var(--border); font-size: 0.78rem;
        }
        .stat-key { color: var(--text-dim); }
        .stat-val { color: var(--text); font-size: 0.88rem; }
        .stat-val.green { color: var(--green); }
        .stat-val.amber { color: var(--amber); }
        .stat-val.red   { color: var(--red);   }
        .stat-val.cyan  { color: var(--cyan);  }

        .prog-wrap {
          height: 4px; background: var(--border);
          border-radius: 2px; overflow: hidden; margin-top: 4px;
        }
        .prog-bar {
          height: 100%;
          background: linear-gradient(90deg, var(--green), var(--cyan));
          border-radius: 2px; width: 0%; transition: width 0.1s linear;
        }
        [data-theme="dark"] .prog-bar { box-shadow: 0 0 8px rgba(0,255,136,0.5); }

        .log-box {
          background: var(--bg); border: 1px solid var(--border);
          border-radius: 4px; padding: 10px; font-size: 0.67rem;
          line-height: 1.85; height: 130px; overflow-y: auto;
          color: var(--text-dim); flex-shrink: 0;
          transition: background 0.25s, border-color 0.25s;
        }
        .log-ok   { color: var(--green); }
        .log-err  { color: var(--red);   }
        .log-info { color: var(--cyan);  }

        .legend { display: flex; flex-direction: column; gap: 5px; }
        .leg-row { display: flex; align-items: center; gap: 8px; font-size: 0.7rem; color: var(--text-dim); }
        .leg-swatch {
          width: 14px; height: 14px; border-radius: 2px; flex-shrink: 0;
          border: 1px solid rgba(0,0,0,0.12);
        }
        [data-theme="dark"] .leg-swatch { border-color: rgba(255,255,255,0.08); }

        @media (max-width: 900px) {
          .layout { grid-template-columns: 1fr; grid-template-rows: auto 1fr auto; }
          .panel { border-right: none; border-bottom: 1px solid var(--border); }
          .panel:last-child { border-left: none; border-top: 1px solid var(--border); }
          .header-status { display: none; }
        }
      </style>
    </head>
    <body>
      <header>
        <div class="logo">
          PATH
          <span>FINDING</span>
          <span style="color:var(--text-dim);font-size:0.65em"> VISUALIZER</span>
        </div>
        <div class="header-right">
          <div class="header-status">
            <span><span class="status-dot"></span>SYSTEM ONLINE</span>
            <span id="hdrAlgo">ALGO: —</span>
            <span id="hdrSize">GRID: —</span>
          </div>
          <div class="theme-toggle" onclick="toggleTheme()" title="Light / Dark Mode">
            <span id="themeLabel">☀ LIGHT</span>
            <div class="toggle-track"><div class="toggle-thumb"></div></div>
          </div>
        </div>
      </header>

      <div class="layout">
        <aside class="panel">
          <div class="panel-title">// Grid Config</div>
          <div>
            <div class="label">DIMENSIONS (rows × cols)</div>
            <div class="row2">
              <input type="number" id="inRows" value="20" min="5" max="60">
              <input type="number" id="inCols" value="35" min="5" max="80">
            </div>
          </div>
          <button class="btn btn-dim" onclick="initGrid()">GENERATE GRID</button>
          <button class="btn btn-dim" onclick="clearGrid()">CLEAR PATHS</button>
          <button class="btn btn-dim" onclick="resetGrid()">RESET ALL</button>

          <div class="panel-title">// Draw Tool</div>
          <div class="tool-group">
            <button class="tool-btn active-wall"  id="tool-wall"  onclick="setTool('wall')" >WALL</button>
            <button class="tool-btn"              id="tool-erase" onclick="setTool('erase')">PATH</button>
            <button class="tool-btn"              id="tool-start" onclick="setTool('start')">🟢 START</button>
            <button class="tool-btn"              id="tool-end"   onclick="setTool('end')"  >🔴 END</button>
          </div>

          <div class="panel-title">// Algorithm</div>
          <div class="algo-list">
            <button class="algo-btn selected" onclick="selectAlgo('bfs', this)">
              <span class="algo-tag" style="color:var(--cyan)">BFS</span>Breadth-First Search
            </button>
            <button class="algo-btn" onclick="selectAlgo('dfs', this)">
              <span class="algo-tag" style="color:var(--purple)">DFS</span>Depth-First Search
            </button>
            <button class="algo-btn" onclick="selectAlgo('dijkstra', this)">
              <span class="algo-tag" style="color:var(--green)">DIJ</span>Dijkstra's Algorithm
            </button>
            <button class="algo-btn" onclick="selectAlgo('astar', this)">
              <span class="algo-tag" style="color:var(--amber)">A*</span>A* Search
            </button>
            <button class="algo-btn" onclick="selectAlgo('greedy_best_first', this)">
              <span class="algo-tag" style="color:var(--red)">GBF</span>Greedy Best-First
            </button>
          </div>

          <div class="panel-title">// Speed</div>
          <div class="speed-wrap">
            <input type="range" id="speedSlider" min="1" max="5" value="3">
            <div class="speed-labels"><span>SLOW</span><span>FAST</span></div>
          </div>
          
          <button class="btn-run-stop state-run" id="btnRunStop" onclick="toggleRunStop()">
            ▶ RUN ALGORITHM
          </button>
        </aside>

        <main class="canvas-area">
          <canvas id="gridCanvas"></canvas>
          <div class="coords" id="coordsDisplay">hover over grid to inspect</div>
        </main>

        <aside class="panel">
          <div class="panel-title">// Execution Stats</div>
          <div>
            <div class="stat-row"><span class="stat-key">ALGORITHM</span><span class="stat-val cyan" id="sAlgo">—</span></div>
            <div class="stat-row"><span class="stat-key">STATUS</span>   <span class="stat-val"      id="sStatus">IDLE</span></div>
            <div class="stat-row"><span class="stat-key">TIME</span>     <span class="stat-val green" id="sTime">—</span></div>
            <div class="stat-row"><span class="stat-key">VISITED</span>  <span class="stat-val"       id="sVisited">—</span></div>
            <div class="stat-row"><span class="stat-key">PATH LEN</span> <span class="stat-val amber" id="sPath">—</span></div>
          </div>

          <div>
            <div class="label" style="margin-bottom:6px">ANIMATION PROGRESS</div>
            <div class="prog-wrap"><div class="prog-bar" id="progBar"></div></div>
          </div>

          <div class="panel-title">// Activity Log</div>
          <div class="log-box" id="logBox"></div>

          <div class="panel-title">// Legend</div>
          <div class="legend" id="legendBox"></div>
        </aside>
      </div>

      <script>
        let isDark = false;

        function toggleTheme() {
          isDark = !isDark;
          document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
          document.getElementById('themeLabel').textContent = isDark ? '🌙 DARK' : '☀ LIGHT';
          updateColors();
          render();
          buildLegend();
        }

        function cssVar(name) {
          return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        }

        const COLORS = { empty:'', wall:'', start:'', end:'', visited:'', path:'', grid:'' };

        function updateColors() {
          COLORS.empty   = cssVar('--c-empty');
          COLORS.wall    = cssVar('--c-wall');
          COLORS.start   = cssVar('--c-start');
          COLORS.end     = cssVar('--c-end');
          COLORS.visited = cssVar('--c-visited');
          COLORS.path    = cssVar('--c-path');
          COLORS.grid    = cssVar('--c-grid');
        }

        function buildLegend() {
          const items = [
            { color: COLORS.empty,   label: 'EMPTY CELL'    },
            { color: COLORS.wall,    label: 'WALL'          },
            { color: COLORS.start,   label: 'START'         },
            { color: COLORS.end,     label: 'END'           },
            { color: COLORS.visited, label: 'VISITED'       },
            { color: COLORS.path,    label: 'SHORTEST PATH' },
          ];
          document.getElementById('legendBox').innerHTML = items.map(i =>
            `<div class="leg-row">
              <div class="leg-swatch" style="background:${i.color}"></div>${i.label}
            </div>`
          ).join('');
        }

        const CELL = 28;
        const GAP  = 1;
        const EMPTY_V = 0, WALL_V = 1, START_V = 2, END_V = 3;

        let rows = 20, cols = 35;
        let matrix = [];
        let currentTool = 'wall';
        let selectedAlgo = 'bfs';
        let isDrawing = false;
        let animFrameId = null;
        let animRunning  = false;
        let visitedSet = new Set();
        let pathSet    = new Set();

        const canvas = document.getElementById('gridCanvas');
        const ctx    = canvas.getContext('2d');

        function setRunStopState(running) {
          const btn = document.getElementById('btnRunStop');
          if (running) {
            btn.textContent = '■ STOP';
            btn.className = 'btn-run-stop state-stop';
          } else {
            btn.textContent = '▶ RUN ALGORITHM';
            btn.className = 'btn-run-stop state-run';
          }
        }

        function toggleRunStop() {
          if (animRunning) {
            stopAnimation();
          } else {
            runSolver();
          }
        }

        function initGrid() {
          rows = Math.max(5, Math.min(60, parseInt(document.getElementById('inRows').value) || 20));
          cols = Math.max(5, Math.min(80, parseInt(document.getElementById('inCols').value) || 35));
          matrix = Array.from({length: rows}, () => Array(cols).fill(EMPTY_V));
          visitedSet.clear(); pathSet.clear();
          resizeCanvas(); render();
          document.getElementById('hdrSize').textContent = `GRID: ${rows}×${cols}`;
          log(`Grid initialized ${rows}×${cols}`, 'info');
          resetStats();
        }
        function resizeCanvas() {
          const t = CELL + GAP;
          canvas.width  = cols * t + GAP;
          canvas.height = rows * t + GAP;
        }
        function clearGrid() {
          visitedSet.clear(); pathSet.clear(); render(); resetStats();
          log('Visualization cleared.', 'info');
        }
        function resetGrid() {
          visitedSet.clear(); pathSet.clear();
          matrix = Array.from({length: rows}, () => Array(cols).fill(EMPTY_V));
          render(); resetStats();
          log('Grid reset.', 'info');
        }

        function cellColor(r, c) {
          const v = matrix[r][c];
          if (v === START_V) return COLORS.start;
          if (v === END_V)   return COLORS.end;
          if (v === WALL_V)  return COLORS.wall;
          const key = `${r},${c}`;
          if (pathSet.has(key))    return COLORS.path;
          if (visitedSet.has(key)) return COLORS.visited;
          return COLORS.empty;
        }

        function render() {
          const t = CELL + GAP;
          ctx.fillStyle = COLORS.grid;
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          for (let r = 0; r < rows; r++)
            for (let c = 0; c < cols; c++)
              paintCanvasCell(r, c, c * t + GAP, r * t + GAP);
        }

        function paintCanvasCell(r, c, x, y) {
          const color = cellColor(r, c);
          ctx.shadowBlur = 0;
          ctx.fillStyle  = color;
          ctx.fillRect(x, y, CELL, CELL);
          const v = matrix[r][c];
          if (isDark && (v === START_V || v === END_V)) {
            ctx.shadowColor = color; ctx.shadowBlur = 12;
            ctx.fillStyle = color; ctx.fillRect(x, y, CELL, CELL);
            ctx.shadowBlur = 0;
          }
        }

        function renderCell(r, c) {
          const t = CELL + GAP;
          paintCanvasCell(r, c, c * t + GAP, r * t + GAP);
        }

        function setTool(t) {
          currentTool = t;
          ['wall','start','end','erase'].forEach(id => {
            document.getElementById('tool-' + id).className =
              'tool-btn' + (id === t ? ' active-' + t : '');
          });
        }

        function selectAlgo(key, btn) {
          selectedAlgo = key;
          document.querySelectorAll('.algo-btn').forEach(b => b.classList.remove('selected'));
          btn.classList.add('selected');
          document.getElementById('hdrAlgo').textContent = 'ALGO: ' + key.toUpperCase();
          document.getElementById('sAlgo').textContent   = key.toUpperCase();
        }

        function getCellFromEvent(e) {
          const rect   = canvas.getBoundingClientRect();
          const scaleX = canvas.width  / rect.width;
          const scaleY = canvas.height / rect.height;
          const px = (e.clientX - rect.left) * scaleX;
          const py = (e.clientY - rect.top)  * scaleY;
          const t = CELL + GAP;
          const c = Math.floor(px / t);
          const r = Math.floor(py / t);
          if (r < 0 || r >= rows || c < 0 || c >= cols) return null;
          return {r, c};
        }

        function paintCell(r, c) {
          const prev = matrix[r][c];
          
          if (currentTool === 'wall') {
            if (prev === START_V || prev === END_V) return;
            matrix[r][c] = WALL_V;
            renderCell(r, c); 
            
          } else if (currentTool === 'erase') {
            if (prev === START_V || prev === END_V) return;
            matrix[r][c] = EMPTY_V;
            renderCell(r, c);
            
          } else if (currentTool === 'start') {
            if (prev === START_V) return;
            for (let rr=0; rr<rows; rr++) {
              for (let cc=0; cc<cols; cc++) {
                if (matrix[rr][cc]===START_V) matrix[rr][cc]=EMPTY_V;
              }
            }
            matrix[r][c] = START_V;
            render();
            
          } else if (currentTool === 'end') {
            if (prev === END_V) return;
            for (let rr=0; rr<rows; rr++) {
              for (let cc=0; cc<cols; cc++) {
                if (matrix[rr][cc]===END_V) matrix[rr][cc]=EMPTY_V;
              }
            }
            matrix[r][c] = END_V;
            render();
          }
        }

        canvas.addEventListener('mousedown', e => {
          const cell = getCellFromEvent(e); if (!cell) return;
          isDrawing = true; paintCell(cell.r, cell.c);
        });
        canvas.addEventListener('mousemove', e => {
          const cell = getCellFromEvent(e);
          if (cell) {
            const lbl = ['EMPTY','WALL','START','END'];
            document.getElementById('coordsDisplay').textContent =
              `[${cell.r}, ${cell.c}]  —  ${lbl[matrix[cell.r][cell.c]]||'?'}`;
          }
          if (!isDrawing || !cell) return;
          if (currentTool !== 'start' && currentTool !== 'end') paintCell(cell.r, cell.c);
        });
        canvas.addEventListener('mouseup',    () => { isDrawing = false; });
        canvas.addEventListener('mouseleave', () => { isDrawing = false; });

        canvas.addEventListener('touchstart', e => {
          e.preventDefault();
          const cell = getCellFromEvent(e.touches[0]); if (!cell) return;
          isDrawing = true; paintCell(cell.r, cell.c);
        }, {passive:false});
        canvas.addEventListener('touchmove', e => {
          e.preventDefault(); if (!isDrawing) return;
          const cell = getCellFromEvent(e.touches[0]); if (!cell) return;
          if (currentTool !== 'start' && currentTool !== 'end') paintCell(cell.r, cell.c);
        }, {passive:false});
        canvas.addEventListener('touchend', () => { isDrawing = false; });

        async function runSolver() {
          if (animRunning) return;
          let hasStart = false, hasEnd = false;
          for (let r=0;r<rows;r++) for (let c=0;c<cols;c++) {
            if (matrix[r][c]===START_V) hasStart = true;
            if (matrix[r][c]===END_V)   hasEnd   = true;
          }
          if (!hasStart) { log('No START cell placed!', 'err'); return; }
          if (!hasEnd)   { log('No END cell placed!',   'err'); return; }

          visitedSet.clear(); pathSet.clear(); render();
          setRunStopState(true);
          log(`Running ${selectedAlgo.toUpperCase()} ...`, 'info');
          setStatus('RUNNING', '');

          try {
            const res = await fetch('/solve', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ matrix, algorithm: selectedAlgo }),
            });
            const data = await res.json();
            if (data.error) { log('ERROR: ' + data.error, 'err'); setStatus('ERROR', 'red'); return; }
            document.getElementById('sTime').textContent    = data.time_ms + ' ms';
            document.getElementById('sVisited').textContent = data.visited_count;
            document.getElementById('sPath').textContent    = data.found ? data.path_length : '—';
            animRunning = true;
            await animateVisited(data.visited_order, data.path, data.found);
          } catch(err) {
            log('Fetch error: ' + err.message, 'err'); setStatus('ERROR', 'red');
          } finally {
            animRunning = false;
            setRunStopState(false);
          }
        }

        function speedDelay() {
          return [0, 40, 18, 7, 2, 0][parseInt(document.getElementById('speedSlider').value)];
        }

        function animateVisited(visitedOrder, path, found) {
          return new Promise(resolve => {
            let i = 0;
            const total = visitedOrder.length;
            function step() {
              if (!animRunning) { resolve(); return; }
              const delay = speedDelay();
              const batch = delay === 0 ? 50 : 1;
              for (let b = 0; b < batch && i < total; b++, i++) {
                const [r, c] = visitedOrder[i];
                if (matrix[r][c]!==START_V && matrix[r][c]!==END_V) {
                  visitedSet.add(`${r},${c}`); renderCell(r, c);
                }
              }
              document.getElementById('progBar').style.width = (i / total * 100) + '%';
              if (i < total) {
                animFrameId = delay===0 ? requestAnimationFrame(step)
                                        : setTimeout(()=>requestAnimationFrame(step), delay);
              } else {
                if (found && path) setTimeout(()=>animatePath(path, resolve), 80);
                else { setStatus('NO PATH','red'); log('No path found.','err'); resolve(); }
              }
            }
            requestAnimationFrame(step);
          });
        }

        function animatePath(path, done) {
          if (!animRunning) { done(); return; }
          let i = 0;
          function step() {
            if (!animRunning) { done(); return; }
            if (i >= path.length) {
              setStatus('FOUND','green');
              log(`Path found! ${path.length-1} steps.`,'ok');
              done(); return;
            }
            const [r, c] = path[i];
            if (matrix[r][c]!==START_V && matrix[r][c]!==END_V) {
              pathSet.add(`${r},${c}`); renderCell(r, c);
            }
            i++;
            animFrameId = setTimeout(()=>requestAnimationFrame(step), 22);
          }
          requestAnimationFrame(step);
        }

        function stopAnimation() {
          animRunning = false;
          if (animFrameId) { clearTimeout(animFrameId); cancelAnimationFrame(animFrameId); }
          setRunStopState(false);
          setStatus('STOPPED','amber');
          log('Animation stopped.','info');
        }

        function setStatus(text, cls) {
          const el = document.getElementById('sStatus');
          el.textContent = text; el.className = 'stat-val ' + (cls||'');
        }
        function resetStats() {
          setStatus('IDLE','');
          document.getElementById('sTime').textContent    = '—';
          document.getElementById('sVisited').textContent = '—';
          document.getElementById('sPath').textContent    = '—';
          document.getElementById('progBar').style.width  = '0%';
        }

        const logBox = document.getElementById('logBox');
        function log(msg, type='') {
          const line = document.createElement('div');
          if (type) line.className = 'log-' + type;
          line.textContent = `[${new Date().toTimeString().slice(0,8)}] ${msg}`;
          logBox.appendChild(line);
          logBox.scrollTop = logBox.scrollHeight;
        }

        updateColors();
        buildLegend();
        initGrid();
        setTool('wall');
        log('System ready. Draw walls, place START & END, choose algorithm.', 'ok');
      </script>
    </body>
  </html>
  '''