#!/usr/bin/env python3
"""
Session linter and fixer for research-cognition-os.
Checks:
- Frontmatter present
- Three required sections: Did, Found, Next
- Bullet points in each section (starting with '- ')
Optional:
- Related section (encouraged)
Usage:
  python session_linter.py [--fix] [--path /path/to/project/research-cognition-os]
If --fix is provided, will rewrite files to conform.
"""
import argparse
import os
import re
import sys
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Lint and fix session files')
    parser.add_argument('--fix', action='store_true', help='Rewrite files to conform')
    parser.add_argument('--path', type=str, default=None, help='Path to research-cognition-os directory')
    return parser.parse_args()

def find_session_dirs(base_path):
    """Yield paths to sessions directories under base_path."""
    for root, dirs, files in os.walk(base_path):
        if os.path.basename(root) == 'sessions':
            yield root

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_sections(content):
    """Return dict of section name -> content (excluding header line)."""
    # Pattern to match section headers - case insensitive for DID/FOUND/NEXT, case sensitive for Related
    pattern = re.compile(r'^## (DID|FOUND|NEXT|Related)\n', re.MULTILINE)
    matches = list(pattern.finditer(content))
    sections = {}
    for i, m in enumerate(matches):
        name = m.group(1).lower()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        sect = content[start:end].strip()
        sections[name] = sect
    return sections

def has_frontmatter(content):
    return content.startswith('---') and content.count('---') >= 2

def extract_frontmatter_and_body(content):
    if not has_frontmatter(content):
        return None, content
    # find second ---
    first = content.find('---')
    second = content.find('---', first+3)
    front = content[first+3:second].strip()
    body = content[second+3:]
    return front, body

def make_frontmatter(date_str=None):
    from datetime import date
    if date_str is None:
        date_str = date.today().isoformat()
    return f'''---
type: session
status: active
created: {date_str}
tags: [cog/session]
---'''

def ensure_bullets(section_text):
    """Ensure section text consists of bullet points starting with '- '.
    If empty, return '- ...'
    If a line already starts with '- ' (after optional spaces), keep it (normalize leading spaces to none).
    Otherwise, add '- ' prefix.
    """
    lines = [ln.rstrip() for ln in section_text.split('\n') if ln.strip()!='']
    if not lines:
        return '- ...'
    out_lines = []
    for ln in lines:
        stripped = ln.lstrip()
        if stripped.startswith('- '):
            # Already a bullet, ensure no extra leading spaces
            out_lines.append('- ' + stripped[2:].lstrip())
        else:
            out_lines.append('- ' + stripped)
    return '\n'.join(out_lines)

def fix_session(content, filename):
    """Return fixed content and list of changes made."""
    changes = []
    # Extract date from filename if possible (YYYY-MM-DD.md)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', os.path.basename(filename))
    date_str = date_match.group(1) if date_match else None
    
    # Frontmatter
    fm, body = extract_frontmatter_and_body(content)
    if fm is None:
        changes.append('Added frontmatter')
        fm = make_frontmatter(date_str)
        body = content
    else:
        # Ensure required fields exist (type, status, created, tags)
        # For simplicity, we just keep existing frontmatter; could validate but skip.
        pass
    
    # Sections
    sections = extract_sections(body)
    # Ensure Did, Found, Next exist
    for sec in ['did', 'found', 'next']:
        if sec not in sections:
            changes.append(f'Added missing section: {sec.upper()}')
            sections[sec] = ''
    # Ensure Related section optional; we keep if present.
    
    # Convert each section to bullet format
    for sec in ['did', 'found', 'next']:
        old = sections.get(sec, '')
        new = ensure_bullets(old)
        if new != old:
            changes.append(f'Fixed bullet format in {sec.upper()}')
            sections[sec] = new
    # Related: optionally ensure bullet format if present
    if 'related' in sections:
        old_rel = sections['related']
        new_rel = ensure_bullets(old_rel)
        if new_rel != old_rel:
            changes.append(f'Fixed bullet format in RELATED')
            sections['related'] = new_rel
    
    # Reconstruct body
    # Order: Did, Found, Next, Related (if present)
    ordered = ['did', 'found', 'next']
    if 'related' in sections:
        ordered.append('related')
    body_parts = []
    for sec in ordered:
        body_parts.append(f'## {sec.upper()}\n{sections[sec]}')
    body = '\n\n'.join(body_parts)
    
    # Combine
    if fm is not None and fm != make_frontmatter(date_str):  # We extracted existing frontmatter
        # fm is the content between delimiters, so wrap it back
        new_content = f'---\n{fm}\n---\n\n{body}'
    else:
        # fm is either None (we made new frontmatter) or it's the newly made frontmatter
        new_content = f'{fm}\n\n{body}'
    if new_content.strip() != content.strip():
        changes.append('Overall content changed')
    return new_content, changes

def main():
    args = parse_args()
    if args.path:
        base = args.path
    else:
        # Default to searching for research-cognition-os under /home/huangrui
        base = None
    if base is None:
        # Find all research-cognition-os directories
        import subprocess
        result = subprocess.run(['find', '/home/huangrui', '-type', 'd', '-name', 'research-cognition-os'], 
                                capture_output=True, text=True)
        dirs = [d.strip() for d in result.stdout.split('\n') if d.strip() and 'hermes/skills' not in d]
        if not dirs:
            print('No research-cognition-os directories found')
            return 1
        # We'll process each
        for d in dirs:
            sessions_dir = os.path.join(d, 'sessions')
            if not os.path.isdir(sessions_dir):
                continue
            process_sessions_dir(sessions_dir, args.fix)
    else:
        sessions_dir = os.path.join(base, 'sessions')
        if not os.path.isdir(sessions_dir):
            print(f'Sessions directory not found: {sessions_dir}')
            return 1
        process_sessions_dir(sessions_dir, args.fix)
    return 0

def process_sessions_dir(sessions_dir, fix):
    print(f'Processing {sessions_dir}')
    for fname in os.listdir(sessions_dir):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(sessions_dir, fname)
        content = read_file(fpath)
        new_content, changes = fix_session(content, fpath)
        if changes:
            print(f'{fpath}: {"; ".join(changes)}')
            if fix:
                write_file(fpath, new_content)
                print(f'  -> Fixed')
        else:
            print(f'{fpath}: OK')

if __name__ == '__main__':
    sys.exit(main())