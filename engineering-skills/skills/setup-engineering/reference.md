# Speckit, merge e init

## Gate: specify init

`setup-engineering` só roda em repositório já inicializado pelo Speckit.

Sinais de init (o script exige todos):

- `.specify/`
- `.specify/memory/`
- `.specify/templates/` com ao menos um de `spec-template.md`, `plan-template.md`, `tasks-template.md`, `constitution-template.md`
- `.specify/scripts/`

Não trate pasta `.specify` vazia ou só com `memory/` como init. Não crie essa
árvore. A constitution do projeto **não** substitui templates nem scripts.

Comando típico (o usuário escolhe a integração): `specify init --here`.

## Artefato

| Item | Valor |
|------|--------|
| Caminho | `.specify/memory/constitution.md` |
| Features Speckit | `specs/<feature>/` (não escrever aqui) |
| Runtime Speckit | `.specify/templates/`, `.specify/scripts/` (não modificar) |

## Estrutura do markdown (Speckit)

Siga o `constitution-template` (no projeto, se houver; senão o canônico do Speckit):

```markdown
<!--
Sync Impact Report:
- Version change: none → 1.0.0
- Modified principles: …
- Added sections: …
- Removed sections: …
- Follow-up TODOs: …

Provenance:
- Source: weni-ai/vtex-cx-engineering-constitutions (main)
- Domains: backend
-->

# {Project name} Constitution

## Core Principles

### I. {Principle name}

{Regras MUST/SHOULD.}

**Rationale:** {por quê.}

## {Seção extra, se as bases exigirem}

## Governance

{Emenda, SemVer de governança, compliance. Plans usam Constitution Check;
/speckit.analyze trata conflito com MUST como CRITICAL.}

**Version**: 1.0.0 | **Ratified**: YYYY-MM-DD | **Last Amended**: YYYY-MM-DD
```

- Não rebaixe/promova headings em relação ao template.
- Número de princípios: o que as bases + o projeto exigirem, não travar em 5.
- Primeira geração: Version `1.0.0`, Ratified = Last Amended = hoje.
- Atualização: preserve Ratified; Last Amended = hoje; bump SemVer
  (MAJOR = remove/redefine princípio; MINOR = princípio/seção nova; PATCH =
  clarificação).

## Precedência de conteúdo

```
constitution raiz  >  constitution de domínio  >  adaptação do projeto
```

O envelope Speckit (headings, Governance, Version) é fixo. O texto dos
princípios vem das bases aplicadas a este repo.

## O que não fazer

- Concatenar os markdowns das bases sem reescrever.
- Gerar `constitution.md` na raiz.
- Rodar ou simular `specify init`.
- Incluir domínio não detectado e não pedido.
- Suavizar artigo da base sem exceção explícita.
- Deixar `[PLACEHOLDER]` sem `TODO(CAMPO): motivo` no Sync Impact Report.

## Detecção de domínio

**backend:** `cmd/`, `internal/`, `apps/api`, OpenAPI, filas, migrations.

**frontend:** `src/components`, design system, i18n/`locales`, bundler.

**cloud:** `terraform/`, `helm/`, `k8s/`, Pulumi, IAM/rede.

Monorepo: um `constitution.md` Speckit, princípios cobrindo cada domínio
presente.

## Exemplo de síntese

Base raiz: “toda mudança em contrato público exige versionamento”.

Base backend: “APIs HTTP permanecem backward-compatible no mesmo major”.

Projeto (`orders-api` em Go): um princípio MUST sobre versionar `/v1` em
`internal/http`, changelog e testes de contrato no CI — uma vez só, com
rationale.
