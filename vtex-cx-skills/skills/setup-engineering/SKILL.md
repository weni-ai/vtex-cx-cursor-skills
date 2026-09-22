---
name: setup-engineering
description: >-
  Gera a constitution Speckit de um projeto em .specify/memory/constitution.md
  a partir das constitutions base (raiz + domínio) do repositório
  vtex-cx-engineering-constitutions. Exige specify init. Use when the user
  asks to setup engineering, gerar constitution, speckit constitution,
  setup-engineering, or bootstrap engineering rules for a backend, frontend,
  or cloud project.
---

# setup-engineering

Gera a constitution do **projeto atual** no caminho Speckit
`.specify/memory/constitution.md`. O documento é a síntese da constitution de
engenharia (raiz) com a(s) de domínio, no formato exigido pelo Speckit — não um
concat cego e não um `constitution.md` na raiz.

Esta skill **não** substitui `specify init`. Sem init, pare.

## Convenção de caminhos

Nos comandos abaixo, `$SKILL_DIR` é o diretório que contém este `SKILL.md` — o
caminho completo aparece quando a skill é carregada. Substitua antes de
executar; não presuma um caminho fixo de instalação.

O diretório de trabalho dos comandos é a **raiz do projeto atual**.

Os scripts são Python 3 (stdlib apenas). Use o interpretador disponível: `python`
no Windows, `python3` no Linux/macOS. Se um falhar por não existir, tente o
outro.

## Fonte canônica

Repositório: `https://github.com/weni-ai/vtex-cx-engineering-constitutions`
Branch: `main`

| Escopo | Caminho no repositório |
|--------|------------------------|
| Engenharia (sempre) | `base-constitution.md` |
| Backend | `backend/base-constitution.md` |
| Frontend | `frontend/base-constitution.md` |
| Cloud | `cloud/base-constitution.md` |

## Workflow

```
- [ ] 0. Verificar specify init (obrigatório; se falhar, PARE)
- [ ] 1. Inspecionar o projeto e escolher domínio(s)
- [ ] 2. Buscar as constitutions base no repositório canônico
- [ ] 3. Ler as fontes por completo (bases + constitution Speckit atual, se houver)
- [ ] 4. Sintetizar no formato Speckit
- [ ] 5. Escrever .specify/memory/constitution.md
```

### 0. Verificar specify init

Na raiz do projeto atual:

```bash
python "$SKILL_DIR/scripts/check-speckit-init.py" .
```

Se o exit code ≠ 0:

- **PARE.** Não busque bases, não crie `.specify/`, não grave constitution.
- Informe o usuário com a mensagem do script.
- Oriente a inicializar o Speckit neste repositório (`specify init --here`, ou o
  fluxo equivalente da equipe) e só então repetir `setup-engineering`.

Não “complete” o init na mão.

### 1. Inspecionar o projeto e escolher domínio(s)

Analise a raiz do workspace (linguagens, pastas, manifests, IaC). Mapeie:

| Sinal | Domínio |
|-------|---------|
| API, serviços, workers, `go.mod`, `pyproject.toml`, `pom.xml`, Django/FastAPI/Spring | `backend` |
| UI, `package.json` com React/Vue/Next, apps web | `frontend` |
| Terraform, Helm, K8s, Docker de infra, pipelines de cloud | `cloud` |

Um projeto pode ter vários domínios. Se o usuário declarar o domínio, use o
dele. Se restar ambiguidade, pergunte antes de gerar.

A constitution de engenharia (raiz) entra **sempre**. As de domínio entram só
as selecionadas.

### 2. Buscar as constitutions base

```bash
python "$SKILL_DIR/scripts/fetch-constitutions.py" backend
# vários domínios: python "$SKILL_DIR/scripts/fetch-constitutions.py" backend frontend
```

Saída: `<tmp>/vtex-cx-constitutions/<paths>` (`/tmp` no Linux/macOS, `%TEMP%` no
Windows; a última linha do script imprime o caminho). Fallback:

```bash
git clone --depth 1 --branch main https://github.com/weni-ai/vtex-cx-engineering-constitutions.git vtex-cx-engineering-constitutions
```

**Requer rede — rode fora do sandbox.** Este passo faz `git clone` do repositório
canônico, então precisa de acesso à internet com DNS funcionando. Se rodar num
ambiente sandboxed sem rede, falha com `Could not resolve host: github.com`
(erro de DNS, **não** de repositório privado). Ao disparar pelo agente do Cursor,
aprove a execução com rede irrestrita / fora do sandbox. Se o repo exigir
credencial via HTTPS, use um credential helper do git ou informe um token pela
env `CONSTITUTIONS_TOKEN` (ou `GITHUB_TOKEN` / `GH_TOKEN`).

Clone num diretório temporário fora do projeto e remova depois — não versione as
bases dentro do repositório atual.

Não invente artigos: só o que estiver nas bases + o que for específico deste
projeto.

### 3. Ler as fontes por completo

Ordem:

1. Constitution raiz
2. Cada `{domínio}/base-constitution.md` selecionado
3. Scaffold Speckit do projeto, se existir (`.specify/templates/constitution-template.md`
   ou o template resolvido pelos scripts em `.specify/scripts/`)
4. `.specify/memory/constitution.md` se já existir — atualização, não página em branco
5. Evidências do projeto (README, stack, convenções)

Preserve exceções e artigos do projeto que ainda fizerem sentido.

### 4. Sintetizar no formato Speckit

Regras de merge (conteúdo):

1. **Raiz prevalece** em conflito de política de engenharia.
2. **Domínio especializa**, não contradiz a raiz. Exceção só com justificativa
   no artigo.
3. **Camada do projeto** instancia stack, pastas e ferramentas reais.
4. Um único documento. Sem blocos “raiz vs domínio”.
5. Não omita artigos obrigatórios das bases aplicáveis.

Formato Speckit (obrigatório) — detalhe em [reference.md](reference.md):

- Destino exclusivo: `.specify/memory/constitution.md`
- Hierarquia do `constitution-template`: `# … Constitution`, `## Core Principles`
  com `###` por princípio, seções extras, `## Governance`, linha de versão
- Princípios declarativos e testáveis (`MUST` / `SHOULD`), cada um com rationale
- Sem placeholders `[ALL_CAPS]` inexplicados
- Comentário HTML no topo: Sync Impact Report + proveniência (repo, branch, domínios)
- SemVer: primeira geração `1.0.0`; emendas MAJOR/MINOR/PATCH
- Datas ISO `YYYY-MM-DD` em **Version** | **Ratified** | **Last Amended**

Não grave `constitution.md` na raiz do git. Não altere templates, scripts,
`specs/` nem código da aplicação.

### 5. Escrever o artefato

Overwrite de `.specify/memory/constitution.md` no projeto atual.

Resumo ao usuário: versão, bump, TODOs, mensagem de commit sugerida. Não
commitar a menos que o usuário peça.

## Additional resources

- Speckit, merge e init: [reference.md](reference.md)
- Gate de init: [scripts/check-speckit-init.py](scripts/check-speckit-init.py)
- Fetch: [scripts/fetch-constitutions.py](scripts/fetch-constitutions.py)
