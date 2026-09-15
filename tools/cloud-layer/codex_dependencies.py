#!/usr/bin/env python3
"""Install locked root dependencies, plus explicit additional package directories."""
import json
import os
from pathlib import Path
import shutil
import subprocess


def commands(path):
    if (path / 'pnpm-lock.yaml').exists():
        return [['corepack', 'pnpm', 'install', '--frozen-lockfile']]
    if (path / 'yarn.lock').exists():
        classic = '# yarn lockfile v1' in (path / 'yarn.lock').read_text()[:100]
        return [['corepack', 'yarn', 'install', '--frozen-lockfile' if classic else '--immutable']]
    if (path / 'package-lock.json').exists():
        return [['npm', 'ci', '--no-audit', '--no-fund']]
    if (path / 'package.json').exists():
        return [['npm', 'install', '--package-lock=false', '--no-audit', '--no-fund']]
    if (path / 'uv.lock').exists():
        return [['uv', 'sync', '--frozen']]
    if (path / 'requirements.txt').exists():
        return [['python3', '-m', 'pip', 'install', '-r', 'requirements.txt']]
    return []


if __name__ == '__main__':
    repo = Path(__file__).resolve().parents[2]
    cfg = json.loads((repo / '.cloud-layer.json').read_text())
    dirs = ['.'] + cfg.get('dependencyDirectories', [])
    if os.environ.get('CODEX_SKIP_DEPENDENCIES') == '1':
        print('Dependency installation skipped by test override')
        raise SystemExit(0)
    for name in dirs:
        path = (repo / name).resolve()
        if not path.is_relative_to(repo) or not path.is_dir():
            raise SystemExit('Invalid dependency directory')
        for command in commands(path):
            if not shutil.which(command[0]):
                raise SystemExit('Missing dependency installer: ' + command[0])
            print('Installing dependencies in ' + name, flush=True)
            subprocess.run(command, cwd=path, check=True, timeout=600)
