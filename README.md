# VTEX CX Engineering Skills

Skills de engenharia VTEX CX distribuídas como plugins do Cursor. Este
repositório é o marketplace: cada skill é um plugin instalável, versionado aqui
e entregue ao time via team marketplace.

## Estrutura

```
.cursor-plugin/
└── marketplace.json               # lista os plugins deste repo
setup-engineering/                 # um plugin
├── .cursor-plugin/
│   └── plugin.json                # manifest do plugin
└── skills/
    └── setup-engineering/
        ├── SKILL.md
        ├── reference.md
        └── scripts/
```

O Cursor lê `marketplace.json`, resolve cada entrada pelo campo `source` e
descobre os componentes dentro da pasta do plugin por convenção (`skills/`,
`rules/`, `commands/`).

## Skills disponíveis

| Plugin | O que faz |
|--------|-----------|
| `setup-engineering` | Gera a constitution Speckit do projeto em `.specify/memory/constitution.md` a partir das constitutions base de [vtex-cx-engineering-constitutions](https://github.com/weni-ai/vtex-cx-engineering-constitutions) |

## Instalação

O time instala pelo team marketplace: **Customize** na barra lateral, localizar
o plugin e escolher o escopo (projeto ou usuário).

Registro do marketplace (admin, uma vez): **Dashboard → Plugins → Team
Marketplaces → Add Marketplace → Import from Repo**, apontando para este
repositório. Com *Auto Refresh* e o Cursor GitHub App instalado no repo, cada
push na branch rastreada reindexa os plugins.

## Desenvolvimento

Teste local antes de publicar. O Cursor carrega plugins de
`~/.cursor/plugins/local/`, então um symlink por plugin evita cópia manual:

```bash
ln -s "$PWD/setup-engineering" ~/.cursor/plugins/local/setup-engineering
```

Depois rode `Developer: Reload Window` e confirme a skill em **Customize**. Em
Teams e Enterprise isso depende de *Allow Local Plugin Imports* estar
habilitado.

Se você mantinha a skill como skill pessoal em `~/.cursor/skills/`, remova a
cópia após instalar o plugin — duas versões da mesma skill divergem sem aviso.

## Adicionar uma skill nova

1. Crie a pasta do plugin na raiz: `<nome-do-plugin>/`.
2. Adicione `<nome-do-plugin>/.cursor-plugin/plugin.json` com `name`,
   `description` e `version`.
3. Escreva a skill em `<nome-do-plugin>/skills/<nome-da-skill>/SKILL.md`.
4. Registre a entrada em `.cursor-plugin/marketplace.json` com `source`
   apontando para a pasta do plugin.

Convenções para o conteúdo da skill:

- `name` em kebab-case, igual ao nome da pasta.
- `description` em terceira pessoa, dizendo **o que** faz e **quando** usar —
  é o que o agente usa para decidir se aciona a skill.
- `SKILL.md` enxuto; detalhamento vai em arquivos irmãos referenciados a um
  nível de profundidade.
- Scripts em `scripts/`, invocados por caminho relativo ao diretório da skill.
  Nunca fixe um caminho de instalação como `~/.cursor/skills/...`: o diretório
  muda conforme o plugin é instalado.

## Versionamento

`version` no `plugin.json` segue SemVer e é o que o time vê ao atualizar. Faça o
bump no mesmo PR que altera o comportamento da skill.
