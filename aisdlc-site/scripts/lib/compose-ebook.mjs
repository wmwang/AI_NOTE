import fs from 'fs';
import path from 'path';
import vm from 'node:vm';

export async function loadCourse() {
  const dataPath = path.resolve('./course-data.js');
  const code = await fs.promises.readFile(dataPath, 'utf8');
  const sandbox = { window: {}, console };
  vm.createContext(sandbox);
  vm.runInContext(code, sandbox);
  return sandbox.window.COURSE;
}

export function coverMeta(meta) {
  const dayLines = meta.days.map(d => `- **${d.title}**（${d.hours}）`).join('\n');
  return `# 全自動化 AI SDLC\n## Workflow 與知識庫閉環\n\n---
\n**課程對象**：${meta.subtitle}\n**總時數**：${meta.format}\n**完課條件**：${meta.completion.join('、')}\n\n### 每日主題\n${dayLines}\n\n---
`;
}

export function composeChapter(dayId, course) {
  const d = course[dayId];
  const meta = course.meta.days.find(x => x.id === dayId);
  let md = `\n\n# ${d.title}\n\n`;
  md += `> ${d.learningGoal}\n\n`;

  for (const u of d.units) {
    md += `\n## ${u.title}\n\n`;
    if (u.goals?.length) {
      md += `**學習目標**：\n`;
      for (const g of u.goals) md += `- ${g}\n`;
      md += '\n';
    }
    if (u.concepts) {
      for (const c of u.concepts) {
        if (c.heading) md += `### ${c.heading}\n\n`;
        if (c.body) md += `${c.body}\n\n`;
        if (c.list) {
          for (const [k, v] of c.list) md += `- **${k}**${v ? ` — ${v}` : ''}\n`;
          md += '\n';
        }
        if (c.table) {
          md += '| ' + c.table.head.join(' | ') + ' |\n';
          md += '| ' + c.table.head.map(() => '---').join(' | ') + ' |\n';
          for (const r of c.table.rows) md += '| ' + r.join(' | ') + ' |\n';
          md += '\n';
        }
        if (c.note) md += `> **Note**: ${c.note}\n\n`;
      }
    }
    if (u.tasks?.length) {
      md += `**任務**：\n`;
      for (const t of u.tasks) md += `- ☐ ${t.label}\n`;
      md += '\n';
    }
    if (u.faq?.length) {
      md += `**常見疑問**：\n`;
      for (const [q, a] of u.faq) md += `- **${q}** ${a}\n`;
      md += '\n';
    }
    if (u.illustrations?.length) {
      const hasHero = u.illustrations.find(i => i.kind === 'hero' || i.kind === 'diagram' || i.kind === 'screenshot');
      if (hasHero) {
        md += `\n![${hasHero.alt}](./assets/illustrations/${hasHero.name}.svg)\n\n`;
      }
    }
  }
  return md;
}

export async function composeEbook(course) {
  let md = coverMeta(course.meta);
  for (const day of course.meta.days) {
    md += composeChapter(day.id, course);
  }
  md += '\n\n---\n\n## 七堂課總回顧\n\n';
  md += '| 堂數 | 主題 | 核心技能 |\n';
  md += '|---|---|---|\n';
  const rows = [
    [1, '企業級 AI 基礎建設', 'CLAUDE.md、架構邊界'],
    [2, '解構大廠 Agent 底層', 'Agentic Loop、Error Recovery'],
    [3, '專屬 SRE 兵器庫', 'MCP Server、AI-Friendly 腳本'],
    [4, '擴充 GitAgent 生態', 'Skill 開發、防呆 Schema'],
    [5, 'AI 系統分析實戰', '逆向工程、規格萃取'],
    [6, 'AI 架構重構實戰', 'Agentic TDD、Clean Architecture'],
    [7, '全自動化 AI SDLC', '端到端 Workflow、知識庫閉環'],
  ];
  for (const [n, t, s] of rows) md += `| ${n} | ${t} | ${s} |\n`;

  md += '\n\n> **🏆 AI Coding Agent 三大紀律**：架構先行 / 規格驅動 / 人機協作\n';
  md += '\n> **🎓 結業不是結束**：把你學到的 Skill 貢獻到團隊 Repo，讓全團隊的 AI 都能受益。\n';
  return md;
}