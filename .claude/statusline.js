#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ANSI colors
const green = '\x1b[38;5;114m';
const orange = '\x1b[38;5;215m';
const red = '\x1b[38;5;203m';
const gray = '\x1b[38;5;242m';
const lGray = '\x1b[38;5;250m';
const cyan = '\x1b[38;5;111m';
const purple = '\x1b[38;5;183m';
const reset = '\x1b[0m';

function main() {
  // Read JSON input from stdin
  let inputData = '{}';
  try {
    inputData = fs.readFileSync(0, 'utf-8');
  } catch {
    inputData = '{}';
  }

  let data = {};
  try {
    data = JSON.parse(inputData);
  } catch {
    data = {};
  }

  const cwd = data.cwd || process.cwd();
  const modelName = data.model?.display_name || 'unknown';

  // Model short name with version
  const modelId = data.model?.id || '';
  let modelShort = 'unknown';
  const versionMatch = modelId.match(/(\d+[\-\.]\d+)/);
  const version = versionMatch ? versionMatch[1].replace('-', '.') : '';
  if (modelName.toLowerCase().includes('opus')) {
    modelShort = version ? `opus ${version}` : 'opus';
  } else if (modelName.toLowerCase().includes('sonnet')) {
    modelShort = version ? `sonnet ${version}` : 'sonnet';
  } else if (modelName.toLowerCase().includes('haiku')) {
    modelShort = version ? `haiku ${version}` : 'haiku';
  }

  // Context usage from built-in data
  const progressPctRaw = data.context_window?.used_percentage || 0;
  const progressPct = progressPctRaw.toFixed(1);
  const progressPctInt = Math.min(Math.floor(progressPctRaw), 100);

  const totalTokens = data.context_window?.total_input_tokens || 0;
  const contextSize = data.context_window?.context_window_size || 200000;
  const formattedTokens = totalTokens ? `${Math.floor(totalTokens / 1000)}k` : '~';
  const formattedLimit = `${Math.floor(contextSize / 1000)}k`;

  // Progress bar (10 blocks)
  const filledBlocks = Math.min(Math.floor(progressPctInt / 10), 10);
  const emptyBlocks = 10 - filledBlocks;

  let barColor = green;
  if (progressPctInt >= 80) {
    barColor = red;
  } else if (progressPctInt >= 50) {
    barColor = orange;
  }

  const progressBar =
    barColor + '\u2588'.repeat(filledBlocks) +
    gray + '\u2591'.repeat(emptyBlocks) +
    reset + ` ${lGray}${progressPct}% (${formattedTokens}/${formattedLimit})${reset}`;

  // Git info from single command
  let gitBranchInfo = null;
  let upstreamInfo = null;
  let totalEdited = 0;
  try {
    const status = execSync(`git -C "${cwd}" status --porcelain -b 2>/dev/null`, { encoding: 'utf-8' });
    const lines = status.split('\n');
    const headerLine = lines[0] || '';

    // Parse branch header: "## branch...upstream [ahead N, behind M]"
    const branchMatch = headerLine.match(/^## (.+?)(?:\.\.\.(\S+))?(?:\s+\[(.+)\])?$/);
    if (branchMatch) {
      const branch = branchMatch[1];
      if (branch === 'HEAD (no branch)') {
        const commit = execSync(`git -C "${cwd}" rev-parse --short HEAD 2>/dev/null`, { encoding: 'utf-8' }).trim();
        gitBranchInfo = `${lGray}@${commit} [detached]${reset}`;
      } else {
        gitBranchInfo = `${lGray}\u{F062C} ${branch}${reset}`;
      }

      // Parse ahead/behind from bracket info
      const tracking = branchMatch[3];
      if (tracking) {
        const parts = [];
        const aheadMatch = tracking.match(/ahead (\d+)/);
        const behindMatch = tracking.match(/behind (\d+)/);
        if (aheadMatch) parts.push(`\u2191${aheadMatch[1]}`);
        if (behindMatch) parts.push(`\u2193${behindMatch[1]}`);
        if (parts.length > 0) {
          upstreamInfo = `${orange}${parts.join('')}${reset}`;
        }
      }
    }

    // Count changed files (all non-header, non-empty lines)
    totalEdited = lines.slice(1).filter(l => l.trim()).length;
  } catch {
    // not a git repo
  }

  // Project name
  const projectName = path.basename(cwd);

  // --- Build output ---

  // Line 1: progress bar | model
  const modelPart = `${purple}${modelShort}${reset}`;
  console.log(`${progressBar} | ${modelPart}`);

  // Line 2: project | edited files + upstream | git branch
  const projectPart = `${cyan}${projectName}${reset}`;
  const uncommittedParts = [`${orange}\u270E ${totalEdited}${reset}`];
  if (upstreamInfo) uncommittedParts.push(upstreamInfo);
  const uncommittedStr = uncommittedParts.join(' ');

  const line2Parts = [projectPart, uncommittedStr];
  if (gitBranchInfo) line2Parts.push(gitBranchInfo);
  console.log(line2Parts.join(' | '));
}

main();
