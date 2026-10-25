#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const PROJECTS_DIR = '/home/eileen/projects';
const OUTPUT_DIR = '/home/eileen/projects/ai-writings/cargo-manifest';

function git(repoPath, ...args) {
  try {
    return execSync('git -C "' + repoPath + '" ' + args.join(' '), {
      encoding: 'utf8', timeout: 10000, stderr: 'pipe'
    }).trim();
  } catch { return null; }
}

function getLanguageBreakdown(repoPath) {
  const files = git(repoPath, 'ls-files');
  if (!files) return {};
  const exts = {};
  for (const f of files.split('\n').filter(Boolean)) {
    const ext = path.extname(f).toLowerCase().slice(1);
    if (ext) exts[ext] = (exts[ext] || 0) + 1;
  }
  return exts;
}

function getWordCount(repoPath) {
  const mdFiles = git(repoPath, 'ls-files', '*.md');
  if (!mdFiles) return 0;
  let total = 0;
  for (const f of mdFiles.split('\n').filter(Boolean)) {
    try {
      const content = fs.readFileSync(path.join(repoPath, f), 'utf8');
      total += content.split(/\s+/).filter(Boolean).length;
    } catch {}
  }
  return total;
}

function getLineCount(repoPath) {
  const files = git(repoPath, 'ls-files');
  if (!files) return 0;
  let total = 0;
  const codeExts = ['js','ts','jsx','tsx','lua','py','rs','go','java','c','cpp','h','rb','sh','sql','html','css','json','toml','yaml','yml'];
  for (const f of files.split('\n').filter(Boolean)) {
    const ext = path.extname(f).toLowerCase().slice(1);
    if (codeExts.includes(ext)) {
      try {
        const content = fs.readFileSync(path.join(repoPath, f), 'utf8');
        total += content.split('\n').length;
      } catch {}
    }
  }
  return total;
}

function hasCI(repoPath) {
  const files = git(repoPath, 'ls-files');
  if (!files) return false;
  return files.split('\n').some(f =>
    f.startsWith('.github/workflows/') || f.includes('.gitlab-ci') || f === 'Jenkinsfile'
  );
}

function getTestCount(repoPath) {
  const files = git(repoPath, 'ls-files');
  if (!files) return 0;
  let count = 0;
  const testPatterns = [/\.test\.[jt]sx?$/, /\.spec\.[jt]sx?$/, /_test\.go$/, /_test\.py$/, /test_.*\.py$/, /\.test\.lua$/, /Test.*\.java$/];
  for (const f of files.split('\n').filter(Boolean)) {
    if (testPatterns.some(p => p.test(f))) {
      try {
        const content = fs.readFileSync(path.join(repoPath, f), 'utf8');
        const matches = content.match(/\b(describe|it|test)\s*\(/g);
        count += matches ? matches.length : 1;
      } catch { count += 1; }
    }
  }
  return count;
}

function classifyRepo(repo) {
  const d = repo.lastCommitDays, c = repo.commitCount, f = repo.fileCount;
  if (f > 500 && c <= 2) return 'archive';
  if (c <= 2 && f < 30) return 'blueprint';
  if (d > 90) return 'derelict';
  if (d > 30) return 'dormant';
  if (c >= 10 && d <= 7) return 'live';
  if (c >= 5 && d <= 7) return 'active';
  if (d <= 30) return 'active';
  return 'dormant';
}

function scanRepo(repoPath, name) {
  const commitCount = parseInt(git(repoPath, 'rev-list', '--count', 'HEAD') || '0');
  const lastCommitDate = git(repoPath, 'log', '-1', '--format=%ci');
  const lastDate = lastCommitDate ? new Date(lastCommitDate.split(' ')[0]) : new Date(0);
  const daysSince = Math.floor((new Date() - lastDate) / 86400000);
  const fileCount = (git(repoPath, 'ls-files') || '').split('\n').filter(Boolean).length;
  const mdFiles = (git(repoPath, 'ls-files', '*.md') || '').split('\n').filter(Boolean).length;
  const languages = getLanguageBreakdown(repoPath);
  const hasReadme = (git(repoPath, 'ls-files') || '').split('\n').some(f => f.toLowerCase() === 'readme.md' || f.toLowerCase() === 'readme');
  const repo = {
    name, commitCount,
    lastCommitDate: lastCommitDate ? lastCommitDate.split(' ')[0] : 'unknown',
    lastCommitDays: daysSince, fileCount,
    lineCount: getLineCount(repoPath), mdFiles,
    wordCount: getWordCount(repoPath),
    testCount: getTestCount(repoPath),
    hasCI: hasCI(repoPath), hasReadme,
    languages, primaryLanguage: Object.entries(languages).sort((a,b) => b[1]-a[1])[0]?.[0] || 'unknown',
  };
  repo.status = classifyRepo(repo);
  return repo;
}

function scanAll() {
  const entries = fs.readdirSync(PROJECTS_DIR, { withFileTypes: true });
  const repos = [];
  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const fullPath = path.join(PROJECTS_DIR, entry.name);
    if (!fs.existsSync(path.join(fullPath, '.git'))) continue;
    process.stderr.write('  Scanning ' + entry.name + '...\n');
    try { repos.push(scanRepo(fullPath, entry.name)); }
    catch (e) { process.stderr.write('  ERROR: ' + e.message + '\n'); }
  }
  return repos;
}

function generateMarkdown(repos) {
  const statusOrder = ['live','active','dormant','derelict','blueprint','archive'];
  const emoji = { live:'🟢', active:'🔵', dormant:'🟡', derelict:'🔴', blueprint:'📐', archive:'📦' };
  const totalRepos = repos.length;
  const totalFiles = repos.reduce((s,r) => s+r.fileCount, 0);
  const totalLines = repos.reduce((s,r) => s+r.lineCount, 0);
  const totalWords = repos.reduce((s,r) => s+r.wordCount, 0);
  const totalTests = repos.reduce((s,r) => s+r.testCount, 0);
  const totalMd = repos.reduce((s,r) => s+r.mdFiles, 0);
  const withCI = repos.filter(r => r.hasCI).length;
  const withReadme = repos.filter(r => r.hasReadme).length;
  const byStatus = {};
  for (const s of statusOrder) byStatus[s] = repos.filter(r => r.status === s);

  let md = '# The Cargo Manifest\n\n';
  md += '**Generated:** ' + new Date().toISOString().split('T')[0] + '\n';
  md += '**Scanner:** The Quartermaster v1.0\n';
  md += '**Motto:** *The hold is what the hold holds, not what the manifest claims.*\n\n---\n\n';
  md += '## Fleet Summary\n\n';
  md += '| Metric | Honest Count | Previously Claimed |\n';
  md += '|--------|-------------|-------------------|\n';
  md += '| Repositories | ' + totalRepos + ' | 32 |\n';
  md += '| Total Files | ' + totalFiles.toLocaleString() + ' | — |\n';
  md += '| Code Lines | ' + totalLines.toLocaleString() + ' | — |\n';
  md += '| Markdown Files | ' + totalMd.toLocaleString() + ' | 4,850 |\n';
  md += '| Creative Words | ' + totalWords.toLocaleString() + ' | — |\n';
  md += '| Test Cases | ' + totalTests.toLocaleString() + ' | 13,012 |\n';
  md += '| With CI/CD | ' + withCI + '/' + totalRepos + ' | — |\n';
  md += '| With README | ' + withReadme + '/' + totalRepos + ' | — |\n\n';
  md += '### Status Distribution\n\n| Status | Count | % |\n|--------|-------|---|\n';
  for (const s of statusOrder) {
    md += '| ' + emoji[s] + ' ' + s + ' | ' + byStatus[s].length + ' | ' + ((byStatus[s].length/totalRepos)*100).toFixed(1) + '% |\n';
  }
  md += '\n';
  for (const status of statusOrder) {
    const group = byStatus[status];
    if (!group.length) continue;
    md += '---\n\n## ' + emoji[status] + ' ' + status.toUpperCase() + ' (' + group.length + ')\n\n';
    md += '| Repo | Commits | Files | Lines | Tests | Last Commit | Lang |\n|------|---------|-------|-------|-------|-------------|------|\n';
    group.sort((a,b) => b.commitCount - a.commitCount);
    for (const r of group) {
      md += '| ' + r.name + ' | ' + r.commitCount + ' | ' + r.fileCount.toLocaleString() + ' | ' + r.lineCount.toLocaleString() + ' | ' + r.testCount + ' | ' + r.lastCommitDate + ' | ' + r.primaryLanguage + ' |\n';
    }
    md += '\n';
  }
  md += '---\n\n## Largest Repos by File Count\n\n| Repo | Files | Status |\n|------|-------|--------|\n';
  for (const r of [...repos].sort((a,b) => b.fileCount - a.fileCount).slice(0,15)) {
    md += '| ' + r.name + ' | ' + r.fileCount.toLocaleString() + ' | ' + emoji[r.status] + ' ' + r.status + ' |\n';
  }
  md += '\n---\n\n## Most Active (by commits)\n\n| Repo | Commits | Files | Status |\n|------|---------|-------|--------|\n';
  for (const r of [...repos].sort((a,b) => b.commitCount - a.commitCount).slice(0,15)) {
    md += '| ' + r.name + ' | ' + r.commitCount.toLocaleString() + ' | ' + r.fileCount.toLocaleString() + ' | ' + emoji[r.status] + ' ' + r.status + ' |\n';
  }
  md += '\n---\n\n## Creative Output\n\n| Repo | MD Files | Words | Status |\n|------|----------|-------|--------|\n';
  for (const r of [...repos].filter(r => r.wordCount > 0).sort((a,b) => b.wordCount - a.wordCount).slice(0,15)) {
    md += '| ' + r.name + ' | ' + r.mdFiles.toLocaleString() + ' | ' + r.wordCount.toLocaleString() + ' | ' + emoji[r.status] + ' ' + r.status + ' |\n';
  }
  md += '\n---\n\n## The Quartermaster\'s Observations\n\n';
  md += '1. **The fleet is smaller than it appears.** ' + totalRepos + ' repos, but only ' + byStatus.live.length + ' truly live. ' + (byStatus.derelict.length + byStatus.dormant.length + byStatus.archive.length) + ' dormant, derelict, or archive.\n';
  md += '2. **The creative engine is real.** ' + totalMd.toLocaleString() + ' markdown files, ' + totalWords.toLocaleString() + ' words — the fleet\'s actual cargo.\n';
  md += '3. **Tests are concentrated.** ' + totalTests.toLocaleString() + ' test cases in ' + repos.filter(r => r.testCount > 0).length + ' repos. Most have zero.\n';
  md += '4. **CI is rare.** ' + withCI + ' of ' + totalRepos + ' repos have CI. Most ships sail without instruments.\n';
  md += '5. **Archives inflate the count.** ' + byStatus.archive.length + ' repos are data dumps — cargo, not ships.\n';
  md += '\n---\n\n*Generated by The Quartermaster. It does not aspire. It counts.*\n';
  return md;
}

const args = process.argv.slice(2);
process.stderr.write('Scanning fleet...\n');
const repos = scanAll();
process.stderr.write('Scanned ' + repos.length + ' repos.\n');
repos.sort((a,b) => {
  const order = ['live','active','dormant','derelict','blueprint','archive'];
  const sd = order.indexOf(a.status) - order.indexOf(b.status);
  return sd !== 0 ? sd : a.name.localeCompare(b.name);
});
const md = generateMarkdown(repos);
fs.writeFileSync(path.join(OUTPUT_DIR, 'fleet-inventory.md'), md);
fs.writeFileSync(path.join(OUTPUT_DIR, 'fleet-inventory.json'), JSON.stringify(repos, null, 2));
console.log('Written to ' + path.join(OUTPUT_DIR, 'fleet-inventory.md'));
const sc = {};
for (const r of repos) sc[r.status] = (sc[r.status]||0)+1;
console.log('\n=== Fleet Status ===');
for (const [s,c] of Object.entries(sc).sort()) console.log('  ' + s + ': ' + c);
console.log('  TOTAL: ' + repos.length);
