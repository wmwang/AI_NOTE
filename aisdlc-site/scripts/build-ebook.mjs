#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { loadCourse, composeEbook } from './lib/compose-ebook.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');

const args = process.argv.slice(2);
const mdOnly = args.includes('--md-only');
const noDocx = args.includes('--no-docx');
const noPdf = args.includes('--no-pdf');

function mdToHtml(md) {
  let html = md
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^---$/gm, '<hr/>')
    .replace(/^\[(.+?)\]\((.+?)\)$/gm, '<a href="$2">$1</a>')
    .replace(/^!\[(.+?)\]\((.+?)\)$/gm, '<img src="$2" alt="$1" style="max-width:100%;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.1);margin:12px 0;"/>')
    .replace(/^\| (.+) \|$/gm, (_, row) => {
      const cells = row.split(' | ').map(c => c.trim());
      return '<tr>' + cells.map(c => `<td style="border:1px solid #ddd;padding:8px;">${c}</td>`).join('') + '</tr>';
    })
    .replace(/(<tr>.*<\/tr>)/gs, (match) => {
      if (match.includes('<th')) return match;
      return match;
    })
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>');
  return html;
}

async function main() {
  await fs.promises.mkdir(DIST, { recursive: true });

  console.log('Loading course data...');
  const course = await loadCourse();
  console.log('Composing markdown...');
  const md = await composeEbook(course);

  const mdPath = path.join(DIST, 'master.md');
  await fs.promises.writeFile(mdPath, md, 'utf8');
  console.log('Written:', mdPath);
  if (mdOnly) { console.log('--md-only, stopping'); return; }

  // Build HTML wrapper
  const css = `
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700;800;900&display=swap');
    @page { margin: 20mm; }
    @page :first { margin: 0; }
    body { font-family: 'Nunito', sans-serif; max-width: 780px; margin: 0 auto; padding: 40px 20px; color: #222; line-height: 1.7; }
    h1 { font-size: 28px; color: #1a1a1a; border-bottom: 3px solid #2196F3; padding-bottom: 10px; margin-top: 40px; }
    h2 { font-size: 20px; color: #333; margin-top: 32px; }
    h3 { font-size: 16px; color: #555; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    th { background: #f0f0f0; font-weight: 700; border: 1px solid #ddd; padding: 8px 12px; }
    td { border: 1px solid #ddd; padding: 8px 12px; }
    code { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
    pre { background: #1a1a1a; color: #e0e0e0; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 16px 0; }
    blockquote { border-left: 4px solid #2196F3; margin: 16px 0; padding: 12px 16px; background: #f0f7ff; border-radius: 4px; }
    img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 16px 0; }
    hr { border: none; border-top: 1px solid #ddd; margin: 24px 0; }
    p { margin: 8px 0; }
    strong { color: #111; }
    li { margin: 4px 0; }
  `;

  const bodyHtml = mdToHtml(md);
  const fullHtml = `<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/><title>全自動化 AI SDLC</title><style>${css}</style></head><body>${bodyHtml}</body></html>`;
  const htmlPath = path.join(DIST, 'ebook.html');
  await fs.promises.writeFile(htmlPath, fullHtml, 'utf8');
  console.log('HTML wrapper written');

  if (!noDocx) {
    console.log('Building DOCX via pandoc...');
    const { spawn } = await import('child_process');
    const outPath = path.join(DIST, '全自動化AI_SDLC.docx');
    const pandocArgs = [mdPath, '-f', 'gfm+attributes+raw_html', '-t', 'docx', '--standalone', '--toc', '--toc-depth=2', '--resource-path', DIST, '-o', outPath];
    try {
      const p = spawn('pandoc', pandocArgs);
      p.on('close', code => { if (code === 0) console.log('DOCX done:', outPath); else console.error('pandoc exit:', code); });
      p.on('error', e => console.error('pandoc error:', e.message));
    } catch (e) { console.error('pandoc not found, skipping DOCX'); }
  }

  if (!noPdf) {
    console.log('Building PDF via Playwright...');
    const { chromium } = await import('playwright');
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto(`file://${path.resolve(htmlPath)}`, { waitUntil: 'networkidle' });
    const pdfPath = path.join(DIST, '全自動化AI_SDLC.pdf');
    await page.pdf({
      path: pdfPath, format: 'A4', printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<div></div>',
      footerTemplate: `<div style="font-size:9pt;width:100%;text-align:center;color:#666;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>`,
      margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' },
    });
    await browser.close();
    console.log('PDF done:', pdfPath);
  }

  console.log('All done!');
}

main().catch(e => { console.error(e); process.exit(1); });