#!/usr/bin/env python3
"""Generate a public-safe empty context baseline; never imports personal sources."""
from pathlib import Path
import sys


DOCUMENTS = {
        '00-READ-FIRST.md': '# Repository cloud context\n\nThis repository has minimal scope. Read its AGENTS.md and CLAUDE.md when present. No personal or other-client brain is included. Record this repository\'s facts only.\n',
        'memory/MEMORY.md': '# Repository memory\n\nNo imported personal context. Keep repository-specific facts in new named files here.\n',
        'inbox/00-HOW-TO-USE.md': '# Cloud corrections\n\nFor a durable correction, add a new dated Markdown file here naming its intended destination and the evidence. Commit it with the work. Preserve existing memory files until the owning session reviews the correction. Never include credentials or another client\'s data.\n',
    }


def generate(repo):
    brain = Path(repo) / '_brain'
    for name, content in DOCUMENTS.items():
        p = brain / name
        p.parent.mkdir(parents=True, exist_ok=True)
        if name == 'memory/MEMORY.md' and p.exists():
            continue
        if not p.exists() or p.read_text() != content:
            p.write_text(content)


if __name__ == '__main__':
    generate(sys.argv[1])
