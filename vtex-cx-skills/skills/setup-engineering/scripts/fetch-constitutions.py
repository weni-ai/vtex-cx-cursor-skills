#!/usr/bin/env python3
"""Baixa as constitutions base do repositório canônico via git (clone shallow).

Uso: fetch-constitutions.py <domain> [domain...]
Domínios: backend frontend cloud

Saída: markdown em CONSTITUTIONS_OUT (padrão: <tmp>/vtex-cx-constitutions).
Multiplataforma (Linux, macOS, Windows) — usa apenas a stdlib + git.

Env:
- CONSTITUTIONS_REF: ref/branch do repo (padrão: main)
- CONSTITUTIONS_OUT: diretório de saída
- CONSTITUTIONS_REPO_URL: URL do repo (padrão: HTTPS; use SSH se preferir)
- CONSTITUTIONS_TOKEN / GITHUB_TOKEN / GH_TOKEN: token p/ HTTPS em repo privado
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "weni-ai/vtex-cx-engineering-constitutions"
DEFAULT_REPO_URL = f"https://github.com/{REPO}.git"
DOMAINS = ("backend", "frontend", "cloud")


def resolve_url() -> str:
    url = os.environ.get("CONSTITUTIONS_REPO_URL", DEFAULT_REPO_URL)
    # Injeta token em URLs HTTPS do GitHub (repo privado sem credential helper).
    token = (
        os.environ.get("CONSTITUTIONS_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
    )
    if token and url.startswith("https://") and "@" not in url:
        url = url.replace("https://", f"https://x-access-token:{token}@", 1)
    return url


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def clone(url: str, ref: str, dest: Path) -> None:
    try:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                ref,
                url,
                str(dest),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        safe = re.sub(r"//[^@/]+@", "//***@", url)
        die(exc.stderr.strip() or f"git clone failed for {safe}", exc.returncode)


def copy(src_root: Path, path: str, out: Path) -> None:
    src = src_root / path
    if not src.is_file():
        die(f"missing in repo: {path}")
    dest = out / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)


def main() -> None:
    args = sys.argv[1:]
    if not args:
        die(
            f"usage: {Path(sys.argv[0]).name} <domain> [domain...]\n"
            f"domains: {' '.join(DOMAINS)}"
        )

    for domain in args:
        if domain not in DOMAINS:
            die(f"unknown domain: {domain}")

    if shutil.which("git") is None:
        die("git is required to fetch the constitutions repo")

    url = resolve_url()
    ref = os.environ.get("CONSTITUTIONS_REF", "main")
    out = Path(
        os.environ.get(
            "CONSTITUTIONS_OUT", Path(tempfile.gettempdir()) / "vtex-cx-constitutions"
        )
    )

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "repo"
        clone(url, ref, repo_dir)

        copy(repo_dir, "base-constitution.md", out)
        for domain in args:
            copy(repo_dir, f"{domain}/base-constitution.md", out)

    print(f"fetched to {out}")
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        print(path)


if __name__ == "__main__":
    main()
