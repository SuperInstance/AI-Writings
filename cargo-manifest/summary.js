#!/usr/bin/env node
/**
 * Quick summary reader for fleet-inventory.json
 * Usage: node summary.js [--status live] [--lang py] [--tests]
 */
const fs = require('fs');
const path = require('path');
const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'fleet-inventory.json'), 'utf8'));
const args = process.argv.slice(2);

let filtered = data;

// Filter by status
const statusIdx = args.indexOf('--status');
if (statusIdx !== -1 && args[statusIdx+1]) {
  filtered = filtered.filter(r => r.status === args[statusIdx+1]);
}

// Filter by language
const langIdx = args.indexOf('--lang');
if (langIdx !== -1 && args[langIdx+1]) {
  filtered = filtered.filter(r => r.primaryLanguage === args[langIdx+1]);
}

// Sort
const sortBy = args.find(a => a.startsWith('--sort-'));
if (sortBy) {
  const key = sortBy.replace('--sort-', '');
  filtered.sort((a,b) => (b[key] || 0) - (a[key] || 0));
}

// Print
console.log('name'.padEnd(35) + 'status'.padEnd(10) + 'commits'.padStart(8) + 'files'.padStart(8) + 'tests'.padStart(8) + 'words'.padStart(12));
console.log('-'.repeat(81));
for (const r of filtered) {
  console.log(
    r.name.padEnd(35) +
    r.status.padEnd(10) +
    String(r.commitCount).padStart(8) +
    String(r.fileCount).padStart(8) +
    String(r.testCount).padStart(8) +
    r.wordCount.toLocaleString().padStart(12)
  );
}
console.log('-'.repeat(81));
console.log('Total: ' + filtered.length + ' repos');
