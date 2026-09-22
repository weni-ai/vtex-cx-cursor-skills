#!/usr/bin/env python3
"""Gate de specify init: valida a árvore .specify/ do projeto atual.

Exit code 0 se o Speckit está inicializado; != 0 com mensagem em stderr se não.
Multiplataforma (Linux, macOS, Windows) — usa apenas a stdlib.
"""
import sys
from pathlib import Path

TEMPLATES = (
    "spec-template.md",
    "plan-template.md",
    "tasks-template.md",
    "constitution-template.md",
)


def fail(detail: str) -> None:
    print(
        "setup-engineering: Speckit ainda não foi inicializado neste repositório.",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print(detail, file=sys.stderr)
    print("", file=sys.stderr)
    print(
        "Rode specify init neste projeto (ex.: specify init --here) e execute "
        "setup-engineering de novo.",
        file=sys.stderr,
    )
    print("Esta skill não cria .specify/ nem substitui o init.", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    specify = root / ".specify"
    memory = specify / "memory"
    templates = specify / "templates"
    scripts = specify / "scripts"

    if not specify.is_dir():
        fail("Ausente: .specify/")
    if not memory.is_dir():
        fail("Ausente: .specify/memory/ (esperado após specify init).")
    if not templates.is_dir():
        fail("Ausente: .specify/templates/ (esperado após specify init).")
    if not scripts.is_dir():
        fail("Ausente: .specify/scripts/ (esperado após specify init).")

    if not any((templates / name).is_file() for name in TEMPLATES):
        fail(
            ".specify/templates/ existe, mas sem templates Speckit "
            "(spec/plan/tasks/constitution)."
        )

    print(f"speckit init OK: {specify}")
    for path in (memory, templates, scripts):
        print(path)


if __name__ == "__main__":
    main()
