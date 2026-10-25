/**
 * QuiltCell — A cell with witness log, rendered as an HTML widget
 *
 * This is the "Quilt in Makepad" demo — using HTML/CSS/WebGL as the
 * substrate-free renderer (which is what makepad compiles to anyway).
 */

export class QuiltCell {
  constructor(id, options = {}) {
    this.id = id;
    this.op = options.op || 'BIND';
    this.data = options.data || '';
    this.witnessCount = 0;
    this.position = options.position || [0, 0];
    this.size = options.size || [80, 80];
    this.linked = new Set();
    this.color = this.colorFromWitness();
    this.timestamp = Date.now();
    this.element = null;
  }

  colorFromWitness() {
    const hue = (this.witnessCount * 37) % 360;
    return `hsl(${hue}, 70%, 60%)`;
  }

  bind(neighborId, data = '') {
    this.linked.add(neighborId);
    this.witnessCount++;
    this.color = this.colorFromWitness();
    this.timestamp = Date.now();
    return {
      op: 'BIND',
      cellId: this.id,
      target: neighborId,
      data,
      witness: this.witnessCount,
      timestamp: this.timestamp
    };
  }

  tick() {
    this.witnessCount++;
    this.color = this.colorFromWitness();
    this.timestamp = Date.now();
    return {
      op: 'TICK',
      cellId: this.id,
      witness: this.witnessCount,
      timestamp: this.timestamp
    };
  }

  render(container) {
    const div = document.createElement('div');
    div.className = 'quilt-cell';
    div.style.left = this.position[0] + 'px';
    div.style.top = this.position[1] + 'px';
    div.style.width = this.size[0] + 'px';
    div.style.height = this.size[1] + 'px';
    div.style.background = this.color;
    div.textContent = `${this.id}\nw:${this.witnessCount}`;
    div.dataset.cellId = this.id;
    this.element = div;
    if (container) container.appendChild(div);
    return div;
  }

  update() {
    if (!this.element) return;
    this.element.style.background = this.color;
    this.element.textContent = `${this.id}\nw:${this.witnessCount}`;
  }
}

export class QuiltLattice {
  constructor() {
    this.cells = new Map();
    this.witnesses = [];
    this.tick = 0;
  }

  add(cell) {
    this.cells.set(cell.id, cell);
    return cell;
  }

  bind(fromId, toId, data = '') {
    const from = this.cells.get(fromId);
    const to = this.cells.get(toId);
    if (!from || !to) return null;
    const w = from.bind(toId, data);
    this.witnesses.push(w);
    return w;
  }

  tickAll() {
    this.tick++;
    for (const cell of this.cells.values()) {
      const w = cell.tick();
      this.witnesses.push(w);
    }
    return this.tick;
  }

  render(container) {
    for (const cell of this.cells.values()) {
      cell.render(container);
    }
  }

  update() {
    for (const cell of this.cells.values()) {
      cell.update();
    }
  }

  witnessesFor(cellId) {
    return this.witnesses.filter(w => w.cellId === cellId);
  }

  recentWitnesses(n = 10) {
    return this.witnesses.slice(-n);
  }

  rootHash() {
    if (this.witnesses.length === 0) return '0'.repeat(64);
    let hash = '0'.repeat(64);
    for (const w of this.witnesses) {
      hash = simpleHash(hash + JSON.stringify(w));
    }
    return hash;
  }
}

function simpleHash(s) {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = ((h << 5) - h) + s.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h).toString(16).padStart(8, '0').repeat(8).slice(0, 64);
}
