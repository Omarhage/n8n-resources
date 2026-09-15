#!/usr/bin/env python3
"""Portable Codex setup: local repo context only; no network or borrowed Mac state."""
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import subprocess


def boot(repo, home, credentials=False):
    repo, home = repo.resolve(), home.resolve()
    if not (repo / '.cloud-layer.json').resolve().is_relative_to(repo):
        raise ValueError('Cloud scope config escapes repository')
    cfg = json.loads((repo / '.cloud-layer.json').read_text())
    scope = cfg.get('scope', 'minimal')
    brain = repo / '_brain'
    if not brain.resolve().is_relative_to(repo):
        raise ValueError('Cloud context root escapes repository')
    required = ['00-READ-FIRST.md', 'memory/MEMORY.md']
    if scope != 'minimal':
        required += ['omar-operating-brain.md', 'business-brain.md', 'shared-brain.md', 'writing-rules.md']
    missing = [name for name in required if not (brain / name).is_file()]
    if missing:
        raise ValueError('Missing cloud context: ' + ', '.join(missing))
    for p in brain.rglob('*'):
        if p.is_symlink() and not p.resolve().is_relative_to(repo):
            raise ValueError('Cloud context link escapes repository: ' + str(p.relative_to(repo)))
    # Skills stay in the repository; AGENTS names these paths explicitly, so no
    # assumption about cloud plugin discovery or the user's home is required.
    skills = sorted(p.parent.name for p in (repo / 'tools/cloud-layer/skills').glob('*/SKILL.md'))
    # The environment owner must opt in on an owner-scoped private environment.
    # Secrets exist only during setup, so materialize only this named credential.
    gws = 'not configured'
    if credentials and scope == 'owner' and os.environ.get('CODEX_ALLOW_GWS') == '1' and os.environ.get('GWS_CREDENTIALS_B64'):
        raw = base64.b64decode(os.environ['GWS_CREDENTIALS_B64'], validate=True)
        data = json.loads(raw)
        if not isinstance(data, dict) or not data.get('refresh_token'):
            raise ValueError('Invalid configured GWS credential')
        target = home / '.config/gws/credentials.json'
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if target.exists() and target.read_bytes() != raw:
            raise ValueError('Preserved a different existing GWS credential')
        if not target.exists():
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'wb') as f:
                f.write(raw)
        target.chmod(0o600)
        gws = 'configured outside repository'
    vault = 'not cloned; use repository-scoped context'
    if credentials and scope == 'owner' and os.environ.get('CODEX_ALLOW_VAULT') == '1':
        destination = home / 'Documents/Business/Business'
        if (destination / '.git').exists():
            vault = 'owner vault present'
        elif destination.exists():
            vault = 'preserved existing non-git directory; owner vault unavailable'
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                result = subprocess.run(['git', 'clone', '--depth', '1', 'https://github.com/Omarhage/business-vault.git', str(destination)],
                                        capture_output=True, timeout=60)
                vault = 'owner vault cloned' if result.returncode == 0 else 'owner vault unavailable: repository authorization or network required'
            except subprocess.TimeoutExpired:
                vault = 'owner vault unavailable: clone timed out'
    result = {'scope': scope, 'context_files_present': len(required), 'skills': skills,
              'vault': vault, 'gws': gws,
              'context_loaded_by_model': 'requires AGENTS read; setup proves files only'}
    state = repo / '.codex/cloud-status.json'
    state.parent.mkdir(exist_ok=True)
    state.write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--setup', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(boot(Path(__file__).resolve().parents[2], Path.home(), args.setup)))
    except (ValueError, OSError) as exc:
        print('Codex cloud setup failed: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
