const ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6";
const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync } = require('child_process');

// Read token from wrangler config
const tokenRaw = fs.readFileSync(path.join(require('os').homedir(), '.config/.wrangler/config/default.toml'), 'utf8');
const TOKEN = tokenRaw.match(/oauth_token = "([^"]+)"/)[1];

function generateImage(prompt, outfile, steps = 4) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({ prompt, steps });
    const options = {
      hostname: 'api.cloudflare.com',
      path: `/client/v4/accounts/${ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell`,
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.success && json.result && json.result.image) {
            const dir = path.dirname(outfile);
            if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
            fs.writeFileSync(outfile, Buffer.from(json.result.image, 'base64'));
            const size = fs.statSync(outfile).size;
            console.log(`  ✓ ${path.basename(outfile)} (${(size/1024).toFixed(0)}KB)`);
            resolve(true);
          } else {
            console.log(`  ✗ ${path.basename(outfile)}: ${JSON.stringify(json.errors || 'unknown')}`);
            resolve(false);
          }
        } catch(e) {
          console.log(`  ✗ ${path.basename(outfile)}: ${e.message}`);
          resolve(false);
        }
      });
    });
    req.on('error', (e) => { console.log(`  ✗ ${path.basename(outfile)}: ${e.message}`); resolve(false); });
    req.write(body);
    req.end();
  });
}

// Batch generator with rate limiting
async function generateBatch(jobs) {
  const BATCH_SIZE = 3; // CF can handle ~3 concurrent
  const DELAY_MS = 500;
  let success = 0;
  let fail = 0;
  
  for (let i = 0; i < jobs.length; i += BATCH_SIZE) {
    const batch = jobs.slice(i, i + BATCH_SIZE);
    console.log(`\n=== Batch ${Math.floor(i/BATCH_SIZE)+1}/${Math.ceil(jobs.length/BATCH_SIZE)} ===`);
    
    const results = await Promise.all(
      batch.map(job => generateImage(job.prompt, job.file))
    );
    
    success += results.filter(r => r).length;
    fail += results.filter(r => !r).length;
    
    if (i + BATCH_SIZE < jobs.length) {
      await new Promise(r => setTimeout(r, DELAY_MS));
    }
  }
  
  console.log(`\n=== Complete: ${success} succeeded, ${fail} failed ===`);
  return { success, fail };
}

// Export for require
module.exports = { generateImage, generateBatch };

// CLI mode: read jobs from JSON file
if (require.main === module) {
  const jobsFile = process.argv[2];
  if (!jobsFile) {
    console.error('Usage: node cf-image-gen.js <jobs.json>');
    process.exit(1);
  }
  const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
  generateBatch(jobs).then(({success, fail}) => {
    process.exit(fail > success ? 1 : 0);
  });
}
