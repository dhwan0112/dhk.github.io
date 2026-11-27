/*
 * ChemViz players: SVG animations drawn in the browser from small JSON files.
 *
 * Markup:
 *   <div class="cv-player" data-cv="rutherford|maxwell-boltzmann|mb-convergence"
 *        data-src="path/to/data.json" aria-label="..."></div>
 *
 * The data files are written by export_web_data.py from the original Python
 * scripts (same seeds and parameters). Rutherford trajectories are integrated
 * here with the same velocity Verlet scheme; the molecular-dynamics frames are
 * stored positions and speeds.
 */
(function () {
  'use strict';

  var SVG_NS = 'http://www.w3.org/2000/svg';
  var FPS = 20;
  var W = 600;
  var H = 800;
  var BOX = { x: 72, y: 36, w: 456, h: 456 };
  var PLOT = { x: 84, y: 552, w: 432, h: 156 };
  var PT = 100 / 72;

  function el(name, attrs, parent) {
    var node = document.createElementNS(SVG_NS, name);
    if (attrs) {
      for (var key in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, key)) continue;
        if (key === 'fill' || key === 'stroke') node.style.setProperty(key, attrs[key]);
        else node.setAttribute(key, attrs[key]);
      }
    }
    if (parent) parent.appendChild(node);
    return node;
  }

  function text(parent, x, y, size, anchor, baseline, content, extra) {
    var attrs = {
      x: x,
      y: y,
      'font-size': (size * PT).toFixed(1),
      'text-anchor': anchor || 'start',
      'dominant-baseline': baseline || 'central',
      fill: 'var(--cv-ink)'
    };
    if (extra) for (var k in extra) attrs[k] = extra[k];
    var node = el('text', attrs, parent);
    if (content !== undefined) node.textContent = content;
    return node;
  }

  function figX(f) { return f * W; }
  function figY(f) { return (1 - f) * H; }

  function show(node, visible) {
    node.style.display = visible ? '' : 'none';
  }

  function decodeUint16(b64) {
    var raw = atob(b64);
    var bytes = new Uint8Array(raw.length);
    for (var i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
    return new Uint16Array(bytes.buffer);
  }

  function fmt(value, digits) {
    return value.toFixed(digits).replace('-', '−');
  }

  /* ---------- colours that follow the site theme ---------- */

  function parseColour(value) {
    value = value.trim();
    if (value.charAt(0) === '#') {
      var hex = value.slice(1);
      if (hex.length === 3) hex = hex.replace(/./g, function (c) { return c + c; });
      return [parseInt(hex.slice(0, 2), 16), parseInt(hex.slice(2, 4), 16), parseInt(hex.slice(4, 6), 16)];
    }
    var match = value.match(/\d+(\.\d+)?/g);
    return match ? [Number(match[0]), Number(match[1]), Number(match[2])] : [0, 0, 0];
  }

  var palette = { ink: [17, 17, 17], paper: [255, 255, 255] };

  function readPalette() {
    var style = getComputedStyle(document.documentElement);
    var ink = style.getPropertyValue('--ink');
    var paper = style.getPropertyValue('--paper');
    if (ink) palette.ink = parseColour(ink);
    if (paper) palette.paper = parseColour(paper);
  }

  /* fraction 0 gives paper, 1 gives ink */
  function mix(fraction) {
    var p = palette.paper;
    var k = palette.ink;
    return 'rgb(' + Math.round(p[0] + (k[0] - p[0]) * fraction) + ',' +
      Math.round(p[1] + (k[1] - p[1]) * fraction) + ',' +
      Math.round(p[2] + (k[2] - p[2]) * fraction) + ')';
  }

  /* ---------- shared player shell ---------- */

  var players = [];

  function Player(root, scene) {
    var self = this;
    this.root = root;
    this.scene = scene;
    this.frame = 0;
    this.playing = false;
    this.timer = null;
    this.last = 0;

    root.classList.add('cv-ready');
    var svg = el('svg', {
      viewBox: '0 0 ' + W + ' ' + H,
      role: 'img',
      'aria-label': root.getAttribute('aria-label') || '',
      class: 'cv-svg'
    });
    root.appendChild(svg);
    this.svg = svg;

    var bar = document.createElement('div');
    bar.className = 'cv-controls';
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'cv-play';
    button.setAttribute('aria-label', 'Play');
    button.textContent = '▶';
    var range = document.createElement('input');
    range.type = 'range';
    range.min = '0';
    range.step = '1';
    range.value = '0';
    range.className = 'cv-scrub';
    range.setAttribute('aria-label', 'Frame');
    var clock = document.createElement('span');
    clock.className = 'cv-clock';
    bar.appendChild(button);
    bar.appendChild(range);
    bar.appendChild(clock);
    root.appendChild(bar);
    this.button = button;
    this.range = range;
    this.clock = clock;

    button.addEventListener('click', function () {
      if (self.playing) self.pause(); else self.play(true);
    });
    range.addEventListener('input', function () {
      self.pause();
      self.seek(Number(range.value));
    });
    this.loading('loading…');
  }

  Player.prototype.loading = function (message) {
    if (!this.note) this.note = text(this.svg, W / 2, H / 2, 12, 'middle', 'central', '');
    this.note.textContent = message;
  };

  Player.prototype.ready = function () {
    if (this.note) {
      this.note.remove();
      this.note = null;
    }
    this.scene.build(this.svg);
    this.total = this.scene.totalFrames();
    this.range.max = String(this.total - 1);
    this.seek(this.scene.posterFrame ? this.scene.posterFrame() : 0);
    this.isReady = true;
  };

  Player.prototype.seek = function (frame) {
    this.frame = Math.max(0, Math.min(this.total - 1, frame));
    this.scene.draw(this.frame);
    this.range.value = String(this.frame);
    var seconds = this.frame / FPS;
    this.clock.textContent = seconds.toFixed(1) + ' / ' + (this.total / FPS).toFixed(1) + ' s';
  };

  Player.prototype.play = function (fromUser) {
    if (!this.isReady || this.playing) return;
    if (fromUser) this.userStarted = true;
    if (this.frame >= this.total - 1) this.seek(0);
    this.playing = true;
    this.button.textContent = '❚❚';
    this.button.setAttribute('aria-label', 'Pause');
    var self = this;
    this.last = performance.now();
    var tick = function (now) {
      if (!self.playing) return;
      var due = Math.floor((now - self.last) * FPS / 1000);
      if (due > 0) {
        self.last += due * 1000 / FPS;
        var next = self.frame + due;
        if (next >= self.total) next = 0;
        self.seek(next);
      }
      self.timer = requestAnimationFrame(tick);
    };
    this.timer = requestAnimationFrame(tick);
  };

  Player.prototype.pause = function () {
    this.playing = false;
    if (this.timer) cancelAnimationFrame(this.timer);
    this.timer = null;
    this.button.textContent = '▶';
    this.button.setAttribute('aria-label', 'Play');
  };

  Player.prototype.redraw = function () {
    if (this.isReady) this.scene.draw(this.frame);
  };

  /* ---------- axes helpers ---------- */

  function frameRect(parent, rect, width) {
    return el('rect', {
      x: rect.x, y: rect.y, width: rect.w, height: rect.h,
      fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': (width * PT).toFixed(2)
    }, parent);
  }

  function clipFor(svg, rect, id) {
    var defs = svg.querySelector('defs') || el('defs', null, svg);
    var clip = el('clipPath', { id: id }, defs);
    el('rect', { x: rect.x, y: rect.y, width: rect.w, height: rect.h }, clip);
    return 'url(#' + id + ')';
  }

  var uid = 0;
  function nextId(prefix) {
    uid += 1;
    return prefix + uid;
  }

  function linearAxis(parent, rect, x0, x1, y0, y1, xticks, yticks, xlabel, ylabel, yfmt) {
    var g = el('g', null, parent);
    var sx = function (x) { return rect.x + rect.w * (x - x0) / (x1 - x0); };
    var sy = function (y) { return rect.y + rect.h - rect.h * (y - y0) / (y1 - y0); };
    xticks.forEach(function (t) {
      var x = sx(t);
      el('line', { x1: x, x2: x, y1: rect.y + rect.h, y2: rect.y + rect.h - 5, stroke: 'var(--cv-ink)', 'stroke-width': 1.1 }, g);
      text(g, x, rect.y + rect.h + 12, 9, 'middle', 'central', String(t));
    });
    yticks.forEach(function (t) {
      var y = sy(t);
      el('line', { x1: rect.x, x2: rect.x + 5, y1: y, y2: y, stroke: 'var(--cv-ink)', 'stroke-width': 1.1 }, g);
      text(g, rect.x - 6, y, 9, 'end', 'central', yfmt ? yfmt(t) : String(t));
    });
    frameRect(g, rect, 0.8);
    if (xlabel) text(g, rect.x + rect.w / 2, rect.y + rect.h + 32, 11, 'middle', 'central', xlabel);
    if (ylabel) text(g, rect.x - 40, rect.y + rect.h / 2, 11, 'middle', 'central', ylabel,
      { transform: 'rotate(-90 ' + (rect.x - 40) + ' ' + (rect.y + rect.h / 2) + ')' });
    return { g: g, sx: sx, sy: sy };
  }

  function stepsMid(xs, ys, sx, sy) {
    var d = '';
    for (var i = 0; i < xs.length; i++) {
      var y = sy(ys[i]);
      if (i === 0) {
        d += 'M' + sx(xs[0]).toFixed(1) + ' ' + y.toFixed(1);
      } else {
        var mid = sx(0.5 * (xs[i - 1] + xs[i])).toFixed(1);
        d += 'H' + mid + 'V' + y.toFixed(1);
      }
      if (i === xs.length - 1) d += 'H' + sx(xs[i]).toFixed(1);
    }
    return d;
  }

  function mbTheory(v, t) {
    return v / t * Math.exp(-(v * v) / (2 * t));
  }

  function histogramDensity(speeds, offset, count, edges) {
    var bins = edges.length - 1;
    var low = edges[0];
    var width = (edges[bins] - low) / bins;
    var out = new Float64Array(bins);
    var inside = 0;
    for (var i = 0; i < count; i++) {
      var v = speeds[offset + i];
      if (v < low || v > edges[bins]) continue;
      var b = Math.floor((v - low) / width);
      if (b === bins) b = bins - 1;
      out[b] += 1;
      inside += 1;
    }
    for (var j = 0; j < bins; j++) out[j] = inside ? out[j] / (inside * width) : 0;
    return out;
  }

  function linspace(a, b, n) {
    var out = [];
    for (var i = 0; i < n; i++) out.push(a + (b - a) * i / (n - 1));
    return out;
  }

  /* ---------- Rutherford ---------- */

  function rutherfordScene(data) {
    var C = data.constants;
    var N = C.particles;
    var SAMPLE_DT = C.step * C.sampleEvery;
    var INTRO_FRAMES = C.zoomKeys[C.zoomKeys.length - 1][0];
    var HOLD = 3 * FPS;
    var scenes = { nuclear: data.nuclear, pudding: data.pudding };

    /* Velocity Verlet, the same scheme and step as rutherford_paper.py. Only the
       part of each path up to the detector is kept; the final direction comes
       from the exported final angle (repulsion keeps the side of y0). With
       full = true the whole run is integrated so the final angle can be checked. */
    function integrateRange(scene, from, to, full) {
      var steps = Math.trunc(C.totalTime / C.step);
      var strength = C.halfApproach * C.speed * C.speed;
      var rc = scene.chargeRadius;
      for (var p = from; p < to; p++) {
        var keep = scene.exitIndex[p] + 1;
        var limit = full ? steps : scene.exitIndex[p] * C.sampleEvery;
        var path = new Float32Array(2 * keep);
        var angle = new Float32Array(keep);
        var x = C.startX, y = data.y0[p], vx = C.speed, vy = 0;
        var r = Math.max(Math.hypot(x, y), rc);
        var ax = strength * x / (r * r * r), ay = strength * y / (r * r * r);
        path[0] = x; path[1] = y; angle[0] = 0;
        for (var s = 1; s <= limit; s++) {
          var hx = vx + 0.5 * C.step * ax;
          var hy = vy + 0.5 * C.step * ay;
          x += C.step * hx;
          y += C.step * hy;
          r = Math.max(Math.hypot(x, y), rc);
          var r3 = r * r * r;
          ax = strength * x / r3;
          ay = strength * y / r3;
          vx = hx + 0.5 * C.step * ax;
          vy = hy + 0.5 * C.step * ay;
          if (s % C.sampleEvery === 0) {
            var idx = s / C.sampleEvery;
            if (idx < keep) {
              path[2 * idx] = x;
              path[2 * idx + 1] = y;
              angle[idx] = Math.abs(Math.atan2(vy, vx) * 180 / Math.PI);
            }
          }
        }
        if (full) scene.jsFinalAngle[p] = Math.abs(Math.atan2(vy, vx) * 180 / Math.PI);
        var theta = scene.finalAngle[p] * Math.PI / 180;
        scene.dir[2 * p] = Math.cos(theta);
        scene.dir[2 * p + 1] = (data.y0[p] < 0 ? -1 : 1) * Math.sin(theta);
        scene.path[p] = path;
        scene.angle[p] = angle;
        scene.detect[p] = scene.launch[p] + scene.exitIndex[p] * SAMPLE_DT;
      }
    }

    function allocate(scene) {
      scene.path = new Array(N);
      scene.angle = new Array(N);
      scene.dir = new Float64Array(2 * N);
      scene.jsFinalAngle = new Float64Array(N);
      scene.detect = new Float64Array(N);
    }

    function solidAngles(edges) {
      var out = [];
      for (var i = 0; i < edges.length - 1; i++) {
        out.push(2 * Math.PI * (Math.cos(edges[i] * Math.PI / 180) - Math.cos(edges[i + 1] * Math.PI / 180)));
      }
      return out;
    }

    function perSolidAngle(angles, edges, omega) {
      var counts = new Array(edges.length - 1).fill(0);
      angles.forEach(function (a) {
        if (a < edges[0] || a > edges[edges.length - 1]) return;
        var i = 0;
        while (i < edges.length - 2 && a >= edges[i + 1]) i++;
        counts[i] += 1;
      });
      return counts.map(function (c, i) { return c > 0 ? c / omega[i] : NaN; });
    }

    function centres(edges) {
      var out = [];
      for (var i = 0; i < edges.length - 1; i++) out.push(0.5 * (edges[i] + edges[i + 1]));
      return out;
    }

    var nuclearOmega = solidAngles(C.nuclearBins);
    var puddingOmega = solidAngles(C.puddingBins);
    var nuclearCentres = centres(C.nuclearBins);
    var puddingCentres = centres(C.puddingBins);
    var puddingFinal = perSolidAngle(data.pudding.finalAngle, C.puddingBins, puddingOmega);
    var fine = linspace(9, 180, 300);
    var nuclearStart = INTRO_FRAMES + data.pudding.frames + C.interludeFrames;
    var lastFrame = nuclearStart + data.nuclear.frames;

    function zoomExponent(frame) {
      var keys = C.zoomKeys;
      for (var i = 0; i < keys.length - 1; i++) {
        var start = keys[i][0], low = keys[i][1], stop = keys[i + 1][0], high = keys[i + 1][1];
        if (frame <= stop) {
          var f = (frame - start) / (stop - start);
          var eased = f * f * (3 - 2 * f);
          return low + (high - low) * eased;
        }
      }
      return keys[keys.length - 1][1];
    }

    var ui = {};
    var view = { scale: BOX.w / (2 * C.view) };
    function bx(x) { return BOX.x + BOX.w / 2 + x * view.scale; }
    function by(y) { return BOX.y + BOX.h / 2 - y * view.scale; }

    var py = function (v) {
      var lo = -1, hi = Math.log10(3e6);
      return PLOT.y + PLOT.h - PLOT.h * (Math.log10(v) - lo) / (hi - lo);
    };
    var px = function (deg) { return PLOT.x + PLOT.w * deg / 180; };
    var rx = function (m) { return PLOT.x + PLOT.w * (Math.log10(m) + 15) / 15; };
    var ry = function (v) { return PLOT.y + PLOT.h - PLOT.h * v / 1.15; };

    function arcPath(radiusPx, fromDeg, toDeg) {
      var cx = BOX.x + BOX.w / 2, cy = BOX.y + BOX.h / 2;
      var a0 = fromDeg * Math.PI / 180, a1 = toDeg * Math.PI / 180;
      var large = (toDeg - fromDeg) > 180 ? 1 : 0;
      return 'M' + (cx + radiusPx * Math.cos(a0)).toFixed(2) + ' ' + (cy - radiusPx * Math.sin(a0)).toFixed(2) +
        'A' + radiusPx.toFixed(2) + ' ' + radiusPx.toFixed(2) + ' 0 ' + large + ' 0 ' +
        (cx + radiusPx * Math.cos(a1)).toFixed(2) + ' ' + (cy - radiusPx * Math.sin(a1)).toFixed(2);
    }

    function polylineD(path, begin, end) {
      var d = 'M' + bx(path[2 * begin]).toFixed(1) + ' ' + by(path[2 * begin + 1]).toFixed(1);
      for (var i = begin + 1; i <= end; i++) {
        d += 'L' + bx(path[2 * i]).toFixed(1) + ' ' + by(path[2 * i + 1]).toFixed(1);
      }
      return d;
    }

    function dotsD(points, sxf, syf) {
      var d = '';
      for (var i = 0; i < points.length; i += 2) {
        d += 'M' + sxf(points[i]).toFixed(1) + ' ' + syf(points[i + 1]).toFixed(1) + 'h0';
      }
      return d;
    }

    function markerPath(xs, ys, shape, size) {
      var d = '';
      for (var i = 0; i < xs.length; i++) {
        if (!isFinite(ys[i]) || ys[i] < 0.1 || ys[i] > 3e6) continue;
        var x = px(xs[i]), y = py(ys[i]), h = size / 2;
        if (shape === 'circle') {
          d += 'M' + (x - h).toFixed(1) + ' ' + y.toFixed(1) + 'a' + h + ' ' + h + ' 0 1 0 ' + size + ' 0a' + h + ' ' + h + ' 0 1 0 ' + (-size) + ' 0';
        } else {
          d += 'M' + (x - h).toFixed(1) + ' ' + (y - h).toFixed(1) + 'h' + size + 'v' + size + 'h' + (-size) + 'z';
        }
      }
      return d;
    }

    function lineD(xs, ys, sxf, syf) {
      var d = '';
      var pen = false;
      for (var i = 0; i < xs.length; i++) {
        var v = ys[i];
        if (!isFinite(v) || v <= 0) { pen = false; continue; }
        var y = Math.max(PLOT.y, Math.min(PLOT.y + PLOT.h, syf(v)));
        d += (pen ? 'L' : 'M') + sxf(xs[i]).toFixed(1) + ' ' + y.toFixed(1);
        pen = true;
      }
      return d;
    }

    function build(svg) {
      var clipBox = clipFor(svg, BOX, nextId('cvbox'));
      el('rect', { x: 0, y: 0, width: W, height: H, fill: 'var(--cv-paper)' }, svg);
      var box = el('g', { 'clip-path': clipBox }, svg);
      ui.cloud = el('circle', { cx: bx(0), cy: by(0), r: C.puddingRadius * view.scale, stroke: 'var(--cv-ink)', 'stroke-width': 0.9 * PT, 'stroke-dasharray': '5.6 4.2' }, box);
      ui.kept = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.3 * PT, 'stroke-opacity': 0.85 }, box);
      ui.layers = [
        el('path', { fill: 'none', 'stroke-width': 0.5 * PT }, box),
        el('path', { fill: 'none', 'stroke-width': 1.0 * PT }, box),
        el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 2.2 * PT, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, box)
      ];
      var screenPx = C.screenRadius * view.scale;
      ui.screen = el('path', { d: arcPath(screenPx, -180 + C.screenGapDegrees, 180 - C.screenGapDegrees), fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.1 * PT }, box);
      var edge = 2 * Math.atan2(C.halfApproach, C.beamRadius) * 180 / Math.PI;
      ui.direct = el('path', { d: arcPath(screenPx + 0.21 * view.scale, -edge, edge), fill: 'none', 'stroke-width': 7 * PT }, box);
      ui.hits = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-opacity': 0.55, 'stroke-width': 1.9, 'stroke-linecap': 'round' }, box);
      ui.flashes = el('path', { fill: 'var(--cv-paper)', stroke: 'var(--cv-ink)', 'stroke-width': 0.9 * PT }, box);
      ui.nucleus = el('circle', { cx: bx(0), cy: by(0), r: 0.09 * view.scale, fill: 'var(--cv-ink)' }, box);
      var labelBg = { 'paint-order': 'stroke', stroke: 'var(--cv-paper)', 'stroke-width': 4, 'stroke-linejoin': 'round' };
      ui.centreLabel = text(box, bx(0), by(-0.45), 10, 'middle', 'hanging', '', labelBg);
      ui.beam = el('g', null, box);
      el('line', { x1: bx(-4.7), y1: by(4.4), x2: bx(-3.45), y2: by(4.4), stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT }, ui.beam);
      el('path', { d: 'M' + bx(-3.3) + ' ' + by(4.4) + 'l-10 -4v8z', fill: 'var(--cv-ink)' }, ui.beam);
      text(ui.beam, bx(-3.1), by(4.4), 10, 'start', 'central', 'α beam', labelBg);
      ui.fired = text(box, bx(-4.7), by(-4.5), 10, 'start', 'central', '', labelBg);
      ui.screenLabel = text(box, bx(4.8), by(-4.72), 9, 'end', 'central', 'ZnS screen (not to scale)', labelBg);
      ui.directLabel = text(box, bx(4.3), by(0), 9, 'end', 'central', 'direct beam', labelBg);

      ui.intro = el('g', null, box);
      ui.introScreen = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.1 * PT }, ui.intro);
      ui.introAtom = el('circle', { cx: bx(0), cy: by(0), fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT, 'stroke-dasharray': '5.6 4.2' }, ui.intro);
      ui.introNucleus = el('circle', { cx: bx(0), cy: by(0), fill: 'var(--cv-ink)' }, ui.intro);
      el('circle', { cx: bx(0), cy: by(0), r: 1.5, fill: 'var(--cv-ink)' }, ui.intro);
      ui.introTags = [
        [text(ui.intro, bx(0), 0, 11, 'middle', 'text-after-edge', 'nucleus'), C.nucleusMetres],
        [text(ui.intro, bx(0), 0, 11, 'middle', 'text-after-edge', 'atom'), C.atomMetres],
        [text(ui.intro, bx(0), 0, 11, 'middle', 'text-after-edge', 'ZnS screen'), C.screenMetres]
      ];
      ui.unseen = text(ui.intro, BOX.x + BOX.w / 2, BOX.y + BOX.h * (1 - 0.455), 10, 'middle', 'hanging', 'nucleus (far too small to see)');
      ui.viewNote = text(ui.intro, BOX.x + 0.03 * BOX.w, BOX.y + BOX.h * (1 - 0.955), 11, 'start', 'central', '');
      ui.introCaption = text(ui.intro, BOX.x + BOX.w / 2, BOX.y + BOX.h * 0.94, 12, 'middle', 'central', '');
      frameRect(svg, BOX, 1.4);

      ui.model = text(svg, figX(0.12), figY(0.968), 13, 'start', 'central', '');
      ui.key = text(svg, figX(0.88), figY(0.968), 11, 'end', 'central', '');
      ui.setup = text(svg, figX(0.88), figY(0.366), 10, 'end', 'central', '');
      ui.panel = text(svg, figX(0.14), figY(0.336), 13, 'start', 'central', '');
      ui.chartKey = text(svg, figX(0.86), figY(0.336), 10, 'end', 'central', '');
      ui.footer = text(svg, figX(0.5), figY(0.032), 13, 'middle', 'central', '', { 'font-style': 'italic' });

      ui.plot = el('g', null, svg);
      var ax = linearAxis(ui.plot, PLOT, 0, 180, 0, 1, [0, 30, 60, 90, 120, 150, 180], [], 'scattering angle θ (degrees)', 'dN/dΩ');
      ax.g.querySelectorAll('text').forEach(function (t) {
        if (t.textContent === 'scattering angle θ (degrees)' || t.textContent === 'dN/dΩ') t.setAttribute('font-style', 'italic');
      });
      [0, 2, 4, 6].forEach(function (k) {
        var y = py(Math.pow(10, k));
        el('line', { x1: PLOT.x, x2: PLOT.x + 5, y1: y, y2: y, stroke: 'var(--cv-ink)', 'stroke-width': 1.1 }, ui.plot);
        var t = text(ui.plot, PLOT.x - 6, y, 9, 'end', 'central', '10');
        var sup = el('tspan', { dy: -5, 'font-size': (7 * PT).toFixed(1) }, t);
        sup.textContent = String(k);
      });
      var clipPlot = clipFor(svg, PLOT, nextId('cvplot'));
      var plotInner = el('g', { 'clip-path': clipPlot }, ui.plot);
      ui.theory = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT, 'stroke-dasharray': '7 4.2' }, plotInner);
      ui.puddingPts = el('path', { 'stroke-width': 1 }, plotInner);
      ui.nuclearPts = el('path', { fill: 'var(--cv-paper)', stroke: 'var(--cv-ink)', 'stroke-width': 1.3 * PT }, plotInner);
      ui.note1 = text(ui.plot, PLOT.x + 0.97 * PLOT.w, PLOT.y + 0.08 * PLOT.h, 11, 'end', 'hanging', '');
      ui.note2 = text(ui.plot, PLOT.x + 0.97 * PLOT.w, PLOT.y + 0.24 * PLOT.h, 11, 'end', 'hanging', '');
      ui.empty = el('g', null, ui.plot);
      var ey = py(0.17);
      el('line', { x1: px(12), x2: px(178), y1: ey, y2: ey, stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT }, ui.empty);
      el('line', { x1: px(12), x2: px(12), y1: ey - 4, y2: ey + 4, stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT }, ui.empty);
      el('line', { x1: px(178), x2: px(178), y1: ey - 4, y2: ey + 4, stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT }, ui.empty);
      text(ui.empty, px(95), py(0.55), 10, 'middle', 'central', 'plum pudding predicts no counts here');

      ui.ruler = el('g', null, svg);
      frameRect(ui.ruler, PLOT, 0.8);
      for (var k = -15; k <= 0; k++) {
        var x = rx(Math.pow(10, k));
        var major = (k % 3 === 0);
        el('line', { x1: x, x2: x, y1: PLOT.y + PLOT.h, y2: PLOT.y + PLOT.h - (major ? 5 : 3), stroke: 'var(--cv-ink)', 'stroke-width': 1 }, ui.ruler);
        if (major) {
          var lab = text(ui.ruler, x, PLOT.y + PLOT.h + 12, 9, 'middle', 'central', '10');
          var s2 = el('tspan', { dy: -5, 'font-size': (7 * PT).toFixed(1) }, lab);
          s2.textContent = String(k).replace('-', '−');
        }
      }
      text(ui.ruler, PLOT.x + PLOT.w / 2, PLOT.y + PLOT.h + 32, 11, 'middle', 'central', 'length (m)');
      [[1.4e-14, 'nucleus'], [2.8e-10, 'atom'], [C.screenMetres, 'screen distance']].forEach(function (pair) {
        el('line', { x1: rx(pair[0]), x2: rx(pair[0]), y1: ry(0), y2: ry(0.42), stroke: 'var(--cv-ink)', 'stroke-width': 1.4 * PT }, ui.ruler);
        text(ui.ruler, rx(pair[0]), ry(0.47), 10, 'middle', 'text-after-edge', pair[1]);
      });
      ui.rulerMarker = el('path', { fill: 'var(--cv-ink)' }, ui.ruler);
      ui.rulerLabel = text(ui.ruler, 0, ry(0.98), 10, 'middle', 'text-after-edge', 'view');
      applyColours();
    }

    function applyColours() {
      if (!ui.cloud) return;
      ui.cloud.style.setProperty('fill', mix(0.11));
      ui.layers[0].style.setProperty('stroke', mix(0.5));
      ui.layers[1].style.setProperty('stroke', mix(0.75));
      ui.direct.style.setProperty('stroke', mix(0.25));
    }

    function setMode(intro) {
      [ui.kept, ui.centreLabel, ui.beam, ui.fired, ui.screen, ui.screenLabel, ui.hits, ui.flashes].concat(ui.layers)
        .forEach(function (n) { show(n, !intro); });
      show(ui.intro, intro);
      show(ui.plot, !intro);
      show(ui.ruler, intro);
      if (intro) {
        [ui.cloud, ui.nucleus, ui.direct, ui.directLabel].forEach(function (n) { show(n, false); });
      } else {
        ui.panel.textContent = '(b) dN/dΩ';
        ui.setup.textContent = 'schematic, distances not to scale; N = ' + N + ', same beam for both models';
      }
    }

    function drawIntro(frame) {
      setMode(true);
      var exponent = zoomExponent(frame);
      var hw = Math.pow(10, exponent);
      var scale = BOX.w / (2 * hw);
      var cx = BOX.x + BOX.w / 2, cy = BOX.y + BOX.h / 2;
      ui.introNucleus.setAttribute('r', (C.nucleusMetres * scale).toFixed(3));
      ui.introAtom.setAttribute('r', (C.atomMetres * scale).toFixed(3));
      show(ui.introAtom, hw > C.atomMetres / 40);
      var sr = C.screenMetres * scale;
      ui.introScreen.setAttribute('d', arcPath(sr, -180 + C.screenGapDegrees, 180 - C.screenGapDegrees));
      show(ui.introScreen, hw > C.screenMetres / 40);
      ui.introTags.forEach(function (pair) {
        var radius = pair[1];
        show(pair[0], 0.12 * hw < radius && radius < 0.9 * hw);
        pair[0].setAttribute('y', (cy - (radius + 0.03 * hw) * scale).toFixed(1));
      });
      show(ui.unseen, C.nucleusMetres < 0.01 * hw);
      var width = Math.round(Math.log10(2 * hw));
      ui.viewNote.textContent = '';
      ui.viewNote.appendChild(document.createTextNode('view width ≈ 10'));
      var sup = el('tspan', { dy: -6, 'font-size': (8 * PT).toFixed(1) }, ui.viewNote);
      sup.textContent = String(width).replace('-', '−');
      var tail = el('tspan', { dy: 6 }, ui.viewNote);
      tail.textContent = ' m';
      if (exponent < -12.5) ui.introCaption.textContent = 'gold nucleus: about 10⁻¹⁴ m across';
      else if (exponent < -6) ui.introCaption.textContent = 'atom: about 10⁻¹⁰ m, ten thousand times wider';
      else ui.introCaption.textContent = 'screen: centimetres away, 10¹² nuclear widths';
      var mx = rx(2 * hw), my = ry(0.9);
      ui.rulerMarker.setAttribute('d', 'M' + (mx - 5.5).toFixed(1) + ' ' + (my - 5.5).toFixed(1) + 'h11l-5.5 9.5z');
      ui.rulerLabel.setAttribute('x', mx.toFixed(1));
      ui.model.textContent = '(a) real proportions';
      ui.key.textContent = 'zooming out from the nucleus';
      ui.setup.textContent = 'drawn to scale';
      ui.panel.textContent = '(b) length scale';
      ui.chartKey.textContent = 'each small tick is a factor of ten';
      ui.footer.textContent = 'the panels that follow are schematic: distances not to scale';
      ui.footer.setAttribute('font-style', 'normal');
      ui.footer.setAttribute('font-size', (12 * PT).toFixed(1));
    }

    function trails(scene, local, now) {
      var first = Math.max(0, (local - scene.flightFrames) * scene.launchPerFrame);
      var last = Math.min(N, (local + 1) * scene.launchPerFrame);
      var d = ['', '', ''];
      for (var i = first; i < last; i++) {
        var sample = Math.floor((now - scene.launch[i]) / SAMPLE_DT);
        if (sample < 1 || sample >= scene.exitIndex[i]) continue;
        var a = scene.angle[i][sample];
        var band = a > 90 ? 2 : (a > C.bendThreshold ? 1 : 0);
        var begin = band === 2 ? 0 : Math.max(0, sample - C.trailSamples[band]);
        d[band] += polylineD(scene.path[i], begin, sample);
      }
      for (var b = 0; b < 3; b++) ui.layers[b].setAttribute('d', d[b]);
      return last;
    }

    function showHits(scene, now) {
      var hits = '', flashes = '', angles = [], back = 0;
      var r = 3.5;
      for (var i = 0; i < N; i++) {
        if (scene.detect[i] > now) continue;
        var dx = scene.dir[2 * i], dy = scene.dir[2 * i + 1];
        hits += 'M' + bx(dx * scene.depth[i]).toFixed(1) + ' ' + by(dy * scene.depth[i]).toFixed(1) + 'h0';
        if (now - scene.detect[i] < 3 * C.frameDt) {
          var fx = bx(dx * C.screenRadius), fy = by(dy * C.screenRadius);
          flashes += 'M' + (fx - r).toFixed(1) + ' ' + fy.toFixed(1) + 'a' + r + ' ' + r + ' 0 1 0 ' + 2 * r + ' 0a' + r + ' ' + r + ' 0 1 0 ' + (-2 * r) + ' 0';
        }
        angles.push(scene.finalAngle[i]);
        if (scene.finalAngle[i] > 90) back += 1;
      }
      ui.hits.setAttribute('d', hits);
      ui.flashes.setAttribute('d', flashes);
      return { angles: angles, back: back };
    }

    function drawPudding(local) {
      var scene = scenes.pudding;
      var now = (local + 1) * C.frameDt;
      var fired = trails(scene, local, now);
      ui.kept.setAttribute('d', '');
      var done = showHits(scene, now);
      var detected = done.angles.length;
      var largest = detected ? Math.max.apply(null, done.angles) : 0;
      show(ui.cloud, true);
      show(ui.nucleus, false);
      show(ui.direct, false);
      show(ui.directLabel, false);
      ui.centreLabel.textContent = 'positive charge spread over the atom';
      ui.centreLabel.setAttribute('y', by(-C.puddingRadius - 0.2).toFixed(1));
      ui.model.textContent = '(a) plum pudding atom';
      ui.key.textContent = 'prediction before 1909';
      ui.chartKey.textContent = 'squares: plum pudding prediction';
      ui.footer.textContent = 'spread-out charge cannot turn an α particle around';
      ui.footer.setAttribute('font-style', 'normal');
      ui.footer.setAttribute('font-size', (12 * PT).toFixed(1));
      ui.fired.textContent = 'fired: ' + fired;
      ui.nuclearPts.setAttribute('d', '');
      ui.theory.setAttribute('d', '');
      ui.puddingPts.setAttribute('d', markerPath(puddingCentres, perSolidAngle(done.angles, C.puddingBins, puddingOmega), 'square', 6.9));
      ui.puddingPts.style.setProperty('fill', 'var(--cv-ink)');
      ui.puddingPts.style.setProperty('stroke', 'var(--cv-ink)');
      show(ui.empty, true);
      ui.note1.textContent = 'detected: ' + detected;
      ui.note2.textContent = 'largest angle: ' + largest.toFixed(1) + '°,  beyond 90°: 0';
    }

    function drawNuclear(local) {
      var scene = scenes.nuclear;
      var now = (local + 1) * C.frameDt;
      var fired = trails(scene, local, now);
      var done = showHits(scene, now);
      var kept = '';
      for (var i = 0; i < N; i++) {
        if (scene.detect[i] <= now && scene.finalAngle[i] > 90) kept += polylineD(scene.path[i], 0, scene.exitIndex[i]);
      }
      ui.kept.setAttribute('d', kept);
      var detected = done.angles.length;
      show(ui.cloud, false);
      show(ui.nucleus, true);
      show(ui.direct, true);
      show(ui.directLabel, true);
      ui.centreLabel.textContent = 'nucleus';
      ui.centreLabel.setAttribute('y', by(-0.45).toFixed(1));
      ui.model.textContent = '(a) nuclear atom';
      ui.key.textContent = 'thick: deflected beyond 90°';
      ui.chartKey.textContent = 'grey: plum pudding, circles: nuclear, dashed: theory';
      ui.footer.textContent = 'dN/dΩ  ∝  1 / sin⁴(θ/2)';
      ui.footer.setAttribute('font-style', 'italic');
      ui.footer.setAttribute('font-size', (14 * PT).toFixed(1));
      ui.fired.textContent = 'fired: ' + fired;
      ui.puddingPts.setAttribute('d', markerPath(puddingCentres, puddingFinal, 'square', 6.9));
      ui.puddingPts.style.setProperty('fill', mix(0.42));
      ui.puddingPts.style.setProperty('stroke', mix(0.42));
      ui.nuclearPts.setAttribute('d', markerPath(nuclearCentres, perSolidAngle(done.angles, C.nuclearBins, nuclearOmega), 'circle', 6.9));
      if (detected) {
        var ys = fine.map(function (t) {
          var half = t * Math.PI / 360;
          return detected * Math.pow(C.halfApproach / 2, 2) / (Math.PI * C.beamRadius * C.beamRadius * Math.pow(Math.sin(half), 4));
        });
        ui.theory.setAttribute('d', lineD(fine, ys, px, py));
      } else {
        ui.theory.setAttribute('d', '');
      }
      show(ui.empty, false);
      ui.note1.textContent = 'nuclear atom, detected: ' + detected;
      ui.note2.textContent = 'beyond 90°: ' + done.back;
    }

    return {
      prepare: function (full) {
        var chunk = 250;
        var jobs = [];
        ['pudding', 'nuclear'].forEach(function (key) {
          allocate(scenes[key]);
          for (var p = 0; p < N; p += chunk) jobs.push([scenes[key], p, Math.min(N, p + chunk)]);
        });
        if (full) {
          jobs.forEach(function (job) { integrateRange(job[0], job[1], job[2], true); });
          return Promise.resolve();
        }
        return new Promise(function (resolve) {
          var next = function () {
            var job = jobs.shift();
            if (!job) { resolve(); return; }
            integrateRange(job[0], job[1], job[2], false);
            setTimeout(next, 0);
          };
          next();
        });
      },
      build: build,
      applyColours: applyColours,
      totalFrames: function () { return lastFrame + HOLD; },
      posterFrame: function () { return lastFrame - 1; },
      draw: function (frame) {
        frame = Math.min(frame, lastFrame - 1);
        if (frame < INTRO_FRAMES) {
          drawIntro(frame);
        } else if (frame < nuclearStart) {
          setMode(false);
          drawPudding(Math.min(frame - INTRO_FRAMES, data.pudding.frames - 1));
        } else {
          setMode(false);
          drawNuclear(frame - nuclearStart);
        }
      },
      scenes: scenes
    };
  }

  /* ---------- molecular dynamics box (shared by both MB players) ---------- */

  function diskLayer(svg, count) {
    var clip = clipFor(svg, BOX, nextId('cvmd'));
    var g = el('g', { 'clip-path': clip }, svg);
    var pool = [];
    function ensure(n) {
      while (pool.length < n) {
        pool.push(el('circle', { stroke: 'var(--cv-ink)' }, g));
      }
      for (var i = 0; i < pool.length; i++) pool[i].style.display = i < n ? '' : 'none';
    }
    ensure(count);
    return {
      draw: function (positions, speeds, offset, n, box, shadeSpeed, speedScale, lineWidth) {
        var scale = BOX.w / box;
        var radius = 0.5 * scale;
        var list = [];
        for (var i = 0; i < n; i++) {
          var x = positions[2 * (offset + i)] / 65535 * box;
          var y = positions[2 * (offset + i) + 1] / 65535 * box;
          var v = speeds[offset + i] / 65535 * speedScale;
          var fill = mix(Math.min(1, Math.max(0, v / shadeSpeed)));
          list.push([x, y, fill]);
          var near = [x < 0.5, x > box - 0.5, y < 0.5, y > box - 0.5];
          if (near[0]) list.push([x + box, y, fill]);
          if (near[1]) list.push([x - box, y, fill]);
          if (near[2]) list.push([x, y + box, fill]);
          if (near[3]) list.push([x, y - box, fill]);
          if (near[0] && near[2]) list.push([x + box, y + box, fill]);
          if (near[0] && near[3]) list.push([x + box, y - box, fill]);
          if (near[1] && near[2]) list.push([x - box, y + box, fill]);
          if (near[1] && near[3]) list.push([x - box, y - box, fill]);
        }
        ensure(list.length);
        var width = (lineWidth * PT).toFixed(2);
        for (var j = 0; j < list.length; j++) {
          var c = pool[j];
          c.setAttribute('cx', (BOX.x + list[j][0] * scale).toFixed(1));
          c.setAttribute('cy', (BOX.y + BOX.h - list[j][1] * scale).toFixed(1));
          c.setAttribute('r', radius.toFixed(2));
          c.style.setProperty('fill', list[j][2]);
          c.setAttribute('stroke-width', width);
        }
      }
    };
  }

  /* fast discs take the ink colour: dark on the light theme, bright on the dark theme */
  function speedKey() {
    var inkLight = palette.ink[0] + palette.ink[1] + palette.ink[2] > palette.paper[0] + palette.paper[1] + palette.paper[2];
    return inkLight ? 'bright: high speed' : 'dark: high speed';
  }

  function formulaFooter(svg) {
    var t = text(svg, figX(0.5), figY(0.032), 12, 'middle', 'central', '', { 'font-style': 'italic' });
    t.textContent = 'P(v) = (mv / kʙT) exp(−mv² / 2kʙT)      (two dimensions)';
    return t;
  }

  function maxwellScene(data) {
    var N = data.particles;
    var positions = decodeUint16(data.positions);
    var speedsRaw = decodeUint16(data.speeds);
    var speeds = new Float64Array(speedsRaw.length);
    for (var i = 0; i < speeds.length; i++) speeds[i] = speedsRaw[i] / 65535 * data.speedScale;
    var edges = linspace(0, data.speedMax, data.binCount + 1);
    var centres = [];
    for (var j = 0; j < data.binCount; j++) centres.push(0.5 * (edges[j] + edges[j + 1]));
    var fine = linspace(0, data.speedMax, 300);
    var histograms = [];
    for (var f = 0; f < data.frames; f++) histograms.push(histogramDensity(speeds, f * N, N, edges));
    var HOLD = 2 * FPS;
    var ui = {};

    function build(svg) {
      el('rect', { x: 0, y: 0, width: W, height: H, fill: 'var(--cv-paper)' }, svg);
      ui.disks = diskLayer(svg, N);
      frameRect(svg, BOX, 1.4);
      text(svg, figX(0.12), figY(0.968), 13, 'start', 'central', '(a)');
      ui.clock = text(svg, figX(0.2), figY(0.968), 11, 'start', 'central', '', { 'font-style': 'italic' });
      ui.speedKey = text(svg, figX(0.88), figY(0.968), 11, 'end', 'central', '');
      text(svg, figX(0.88), figY(0.366), 10, 'end', 'central', 'periodic box, N = ' + N + ', ρσ² = ' + data.density.toFixed(2));
      text(svg, figX(0.14), figY(0.336), 13, 'start', 'central', '(b) P(v)');
      text(svg, figX(0.86), figY(0.336), 10, 'end', 'central', 'dashed: Maxwell–Boltzmann, solid: simulation');
      formulaFooter(svg);
      ui.axis = linearAxis(svg, PLOT, 0, data.speedMax, 0, 0.9, [0, 1, 2, 3, 4, 5], [0, 0.2, 0.4, 0.6, 0.8], 'v / (ε/m)½', 'P(v)', function (t) { return t.toFixed(1); });
      var clip = clipFor(svg, PLOT, nextId('cvplot'));
      var g = el('g', { 'clip-path': clip }, svg);
      ui.theory = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT, 'stroke-dasharray': '7 4.2' }, g);
      ui.measured = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.8 * PT }, g);
      ui.stage = text(svg, PLOT.x + 0.97 * PLOT.w, PLOT.y + 0.1 * PLOT.h, 11, 'end', 'hanging', '');
      ui.thermo = text(svg, PLOT.x + 0.97 * PLOT.w, PLOT.y + 0.28 * PLOT.h, 11, 'end', 'hanging', '');
    }

    function stageText(frame) {
      if (frame < 6) return 'every particle starts at the same speed';
      if (frame < data.relaxFrames) return 'collisions redistribute the energy';
      return 'heated: kinetic energy × 2';
    }

    function draw(frame) {
      frame = Math.min(frame, data.frames - 1);
      var start = frame >= data.relaxFrames ? data.relaxFrames : 0;
      var from = Math.max(start, frame - data.window + 1);
      var mean = new Float64Array(data.binCount);
      for (var f = from; f <= frame; f++) {
        for (var b = 0; b < data.binCount; b++) mean[b] += histograms[f][b];
      }
      for (var k = 0; k < data.binCount; k++) mean[k] /= (frame - from + 1);
      ui.disks.draw(positions, speedsRaw, frame * N, N, data.box, data.shadeSpeed, data.speedScale, 0.7);
      var t = data.temperature[frame];
      ui.measured.setAttribute('d', stepsMid(centres, mean, ui.axis.sx, ui.axis.sy));
      ui.theory.setAttribute('d', 'M' + fine.map(function (v) {
        return ui.axis.sx(v).toFixed(1) + ' ' + ui.axis.sy(mbTheory(v, t)).toFixed(1);
      }).join('L'));
      ui.speedKey.textContent = speedKey();
      ui.clock.textContent = 't = ' + (frame * data.stepsPerFrame * data.step).toFixed(2);
      ui.stage.textContent = stageText(frame);
      ui.thermo.textContent = 'kʙT/ε = ' + t.toFixed(2);
    }

    return {
      build: build,
      draw: draw,
      totalFrames: function () { return data.frames + HOLD; },
      posterFrame: function () { return data.relaxFrames - 1; },
      histograms: histograms
    };
  }

  function convergenceScene(data) {
    var stages = data.stages.map(function (s) {
      var raw = decodeUint16(s.speeds);
      var speeds = new Float64Array(raw.length);
      for (var i = 0; i < raw.length; i++) speeds[i] = raw[i] / 65535 * data.speedScale;
      return { count: s.count, box: s.box, temperature: s.temperature, running: s.runningDeviation, positions: decodeUint16(s.positions), raw: raw, speeds: speeds };
    });
    var edges = linspace(0, data.speedMax, data.binCount + 1);
    var centres = [];
    for (var j = 0; j < data.binCount; j++) centres.push(0.5 * (edges[j] + edges[j + 1]));
    var fine = linspace(0, data.speedMax, 300);
    var F = data.framesPerStage;
    var total = stages.length * F;
    var HOLD = Math.round(2.5 * FPS);
    var ui = {};

    function build(svg) {
      el('rect', { x: 0, y: 0, width: W, height: H, fill: 'var(--cv-paper)' }, svg);
      ui.disks = diskLayer(svg, 25);
      frameRect(svg, BOX, 1.4);
      text(svg, figX(0.12), figY(0.968), 13, 'start', 'central', '(a)');
      ui.count = text(svg, figX(0.2), figY(0.968), 12, 'start', 'central', '');
      ui.speedKey = text(svg, figX(0.88), figY(0.968), 11, 'end', 'central', '');
      ui.boxNote = text(svg, figX(0.88), figY(0.366), 10, 'end', 'central', '');
      text(svg, figX(0.14), figY(0.336), 13, 'start', 'central', '(b) P(v)');
      text(svg, figX(0.86), figY(0.336), 10, 'end', 'central', 'dashed: Maxwell–Boltzmann, solid: one snapshot');
      formulaFooter(svg);
      ui.axis = linearAxis(svg, PLOT, 0, data.speedMax, 0, 1, [0, 1, 2, 3, 4, 5], [0, 0.2, 0.4, 0.6, 0.8, 1.0], 'v / (ε/m)½', 'P(v)', function (t) { return t.toFixed(1); });
      var clip = clipFor(svg, PLOT, nextId('cvplot'));
      var g = el('g', { 'clip-path': clip }, svg);
      ui.theory = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.0 * PT, 'stroke-dasharray': '7 4.2' }, g);
      ui.measured = el('path', { fill: 'none', stroke: 'var(--cv-ink)', 'stroke-width': 1.8 * PT }, g);
      ui.stage = text(svg, PLOT.x + 0.97 * PLOT.w, PLOT.y + 0.1 * PLOT.h, 13, 'end', 'hanging', '');
      ui.deviation = text(svg, PLOT.x + 0.97 * PLOT.w, PLOT.y + 0.3 * PLOT.h, 11, 'end', 'hanging', '');
    }

    function draw(frame) {
      frame = Math.min(frame, total - 1);
      var stage = stages[Math.floor(frame / F)];
      var local = frame % F;
      var n = stage.count;
      ui.disks.draw(stage.positions, stage.raw, local * n, n, stage.box, data.shadeSpeed, data.speedScale, n <= 400 ? 0.7 : 0.3);
      var h = histogramDensity(stage.speeds, local * n, n, edges);
      ui.measured.setAttribute('d', stepsMid(centres, h, ui.axis.sx, ui.axis.sy));
      ui.theory.setAttribute('d', 'M' + fine.map(function (v) {
        return ui.axis.sx(v).toFixed(1) + ' ' + ui.axis.sy(mbTheory(v, stage.temperature)).toFixed(1);
      }).join('L'));
      ui.speedKey.textContent = speedKey();
      ui.count.textContent = 'N = ' + n;
      ui.boxNote.textContent = 'periodic box, ρσ² = ' + data.density.toFixed(2) + ', kʙT/ε = ' + stage.temperature.toFixed(2);
      ui.stage.textContent = 'N = ' + n;
      ui.deviation.textContent = 'rms deviation = ' + stage.running[local].toFixed(3);
    }

    return {
      build: build,
      draw: draw,
      totalFrames: function () { return total + HOLD; },
      posterFrame: function () { return total - 1; }
    };
  }

  var FACTORIES = {
    'rutherford': rutherfordScene,
    'maxwell-boltzmann': maxwellScene,
    'mb-convergence': convergenceScene
  };

  /* ---------- wiring ---------- */

  function start(root) {
    var factory = FACTORIES[root.getAttribute('data-cv')];
    if (!factory) return;
    var player = new Player(root, { build: function () {}, draw: function () {}, totalFrames: function () { return 1; } });
    players.push(player);
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var visible = false;

    fetch(root.getAttribute('data-src'))
      .then(function (response) {
        if (!response.ok) throw new Error(response.status);
        return response.json();
      })
      .then(function (data) {
        var scene = factory(data);
        return Promise.resolve(scene.prepare ? scene.prepare(false) : null).then(function () {
          player.scene = scene;
          player.ready();
          if (visible && !reduced && !player.userPaused) player.play(false);
        });
      })
      .catch(function () {
        player.loading('could not load the animation data');
      });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          visible = entry.isIntersecting;
          if (visible && !reduced && !player.userPaused) player.play(false);
          if (!visible) player.pause();
        });
      }, { threshold: 0.35 }).observe(root);
    }
    player.button.addEventListener('click', function () {
      player.userPaused = !player.playing;
    });
  }

  function init() {
    readPalette();
    document.querySelectorAll('.cv-player[data-cv]').forEach(start);
    new MutationObserver(function () {
      readPalette();
      players.forEach(function (p) {
        if (p.scene.applyColours) p.scene.applyColours();
        p.redraw();
      });
    }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  }

  if (typeof window !== 'undefined' && typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
  }

  if (typeof module !== 'undefined') {
    module.exports = { rutherfordScene: rutherfordScene, maxwellScene: maxwellScene, convergenceScene: convergenceScene, histogramDensity: histogramDensity };
  }
})();
