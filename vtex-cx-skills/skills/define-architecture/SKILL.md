---
name: define-architecture
description: >-
  Gera ou emenda o Architecture Document de uma feature no repositório de
  specs do produto: avalia se ele é necessário, lê a Product Spec fixada por
  tag e as constitutions de cada repositório impactado (submodules em
  engineering/), conduz as decisões transversais com a referência técnica e
  produz os contratos legíveis por máquina (OpenAPI, JSON Schema) que
  frontend e backend implementam em paralelo. Use when the user asks to
  define architecture, definir arquitetura, for an architecture document,
  documento de arquitetura, technical design, contrato entre frontend e
  backend, architecture triage, or define-architecture.
---

# define-architecture

Produz `specs/<feature>/architecture.md` e `specs/<feature>/contracts/` no
**repositório de specs do produto**. O documento é a cola entre os
repositórios que implementam a mesma Product Spec: decide o que atravessa uma
fronteira (contratos, ownership de dados, consistência, NFRs vinculantes,
sequência de entrega) e deixa o resto para a Engineering Spec de cada repo.

Não é uma spec: não passa por plan, tasks nem implement. Mas mantém a
rastreabilidade de uma spec — herda a Product Spec por tag, é fixado por tag
própria e muda por emenda.

O diretório de trabalho é a **raiz do repositório de specs do produto**.

## Workflow

```
- [ ] 0. Confirmar que é um repositório de specs do produto
- [ ] 1. Gate 0: localizar e fixar a Product Spec (bloqueante)
- [ ] 2. Ler a Product Spec por completo
- [ ] 3. Detectar documento existente (criação ou emenda)
- [ ] 4. Avaliar a necessidade e registrar o veredito
- [ ] 5. Levantar os repositórios impactados e suas constitutions
- [ ] 6. Conduzir as decisões com a referência técnica
- [ ] 7. Escrever o documento e os contratos
- [ ] 8. Validar (contratos + checklist)
- [ ] 9. Reportar e orientar PR, aprovação e tag
```

### 0. Confirmar o repositório

O repositório precisa ter `specs/` e `.gitmodules` com os repositórios de
engenharia em `engineering/`. Sem isso, **PARE**: esta skill não roda dentro
de um repositório de engenharia — lá não há visão dos outros lados do
contrato.

Monte o inventário do passo 5:

```bash
git submodule status
```

- Prefixo `-`: submodule não inicializado (não há código no disco).
- Prefixo `+`: o checkout difere do commit registrado; avise o usuário.
- Descrição de cada repo: `engineering[]` em `.specify/bootstrap.json`, se
  existir.
- Constitution: `engineering/<repo>/.specify/memory/constitution.md`; a versão
  está na linha `**Version**:`.

### 1. Gate 0 — Product Spec

Sem Product Spec commitada e taggeada não há o que herdar.

1. Obtenha o caminho da Product Spec pela mensagem do usuário
   (`specs/NNN-<feature>/spec.md`). Se não estiver lá, pergunte e **espere**.
   Não adivinhe a feature.
2. Resolva a referência imutável:

   ```bash
   git remote get-url origin
   git rev-parse HEAD
   git tag --points-at HEAD
   git status --porcelain -- specs/NNN-<feature>/spec.md
   git rev-list --count HEAD..@{u}
   ```

   - **Tag**: use uma tag que aponte para HEAD e **não** termine em
     `/arch-vN` — essas são do Architecture Document, não da Product Spec.
     Sem tag válida, fixe no SHA completo do HEAD e avise que a herança ficou
     num commit, não numa tag.
   - **Permalink**: `https://<host>/<owner>/<repo>/blob/<commit>/<path>`.
     Normalize remote SSH (`git@github.com:owner/repo.git`) para HTTPS, remova
     `.git` final e qualquer credencial embutida na URL.

3. **PARE** sem criar nenhum arquivo, dizendo o que destrava, quando:
   - o arquivo não existe ou não está commitado;
   - `status --porcelain` mostra mudança — o conteúdo lido não é o da versão
     fixada;
   - `rev-list` mostra o clone atrás do upstream e o usuário não confirmou
     qual versão é a autoritativa.

### 2. Ler a Product Spec

Leia **inteira**. Extraia e mantenha:

- `Scope` e `Roles & Permissions` — o que a feature cobre e para quem.
- `Inputs for Architecture & Engineering` — é a entrada principal: superfícies
  afetadas, times, dados, interações, volume, privacidade, rollout e as
  hipóteses técnicas (não vinculantes) do trio.
- `Binding Decisions` (`BD-*`) — o documento herda e **não pode contradizer**.
- `Non-Functional Requirements`, `Privacy & Data Protection`, `Key Entities`,
  `Edge Cases`.
- `Success Criteria` (`SC-*`) — só para referência; não são reescritos aqui.

Se `Decisions to Validate in the FDD` não estiver `None`, avise: a Product
Spec ainda pode mudar e o documento vai precisar de emenda.

### 3. Criação ou emenda

Se `specs/<feature>/architecture.md` já existe, é **emenda**, não página em
branco: siga o fluxo de emenda em [reference.md](reference.md#emendas). Não
reescreva decisões aprovadas sem registrar no `Amendment Log`.

### 4. Avaliar a necessidade

Aplique os critérios de [reference.md](reference.md#avaliação) com evidência
tirada da Product Spec (cite as seções e IDs). O veredito é um de:

| Veredito | Quando | O que o documento contém |
|----------|--------|--------------------------|
| `full` | Decisões transversais além do contrato: novo serviço ou datastore, ownership de dados entre serviços, consistência distribuída, compliance, escala nova | Todas as seções do template |
| `contract-only` | Mais de um repo muda, mas a única coisa transversal é a interface entre eles | Herança, avaliação, aprovação, mapa de impacto, contratos, sequência de entrega, riscos, emendas |
| `not-required` | Um único repositório muda e nenhuma interface pública entre repos muda | Só herança e avaliação |

Apresente o veredito com a evidência e confirme com o usuário (AskQuestion)
antes de seguir. O veredito é registrado **sempre**, inclusive
`not-required`: é ele que justifica `Architecture doc: none` nas Engineering
Specs. Em `not-required`, escreva o documento mínimo e pule para o passo 9.

### 5. Levantar os repositórios impactados

A partir de `Affected product surfaces and modules` e `Teams and products
involved`, escolha os submodules impactados no inventário do passo 0.

- Submodule não inicializado: peça para rodar
  `git submodule update --init engineering/<repo>` (requer rede). Não leia um
  repositório que não está no disco.
- Leia `engineering/<repo>/.specify/memory/constitution.md` de **cada**
  impactado. Constitution ausente: registre em `Risks and Open Questions`,
  recomende `setup-engineering` naquele repo e trate as bases raiz + domínio
  como o mínimo.
- Mapeie o estado atual com caminhos reais: endpoints, modelos, eventos,
  filas e componentes que a feature toca, e a funcionalidade análoga mais
  próxima. Leia `AGENTS.md`/`CLAUDE.md` do repo, se houver.
- Não altere nada dentro dos submodules.

Impacto fora dos submodules (outro produto, outro time): entra no mapa de
impacto como dependência externa, com dono nomeado.

### 6. Conduzir as decisões

Aqui o comportamento é o **oposto** do `/speckit.specify`: o raio de impacto é
grande, então o agente **propõe e a referência técnica decide**.

1. Liste as decisões candidatas e filtre pela regra da fronteira
   ([reference.md](reference.md#regra-da-fronteira)). O que não atravessa
   fronteira sai do documento e fica para a Engineering Spec.
2. Para cada decisão restante, apresente 2–3 opções com trade-offs e a
   recomendação, ancoradas no estado atual e nas constitutions dos dois lados.
   Use AskQuestion, agrupando decisões independentes numa rodada.
3. Marque cada decisão como `binding` (as Engineering Specs herdam) ou
   `guidance` (recomendação). Só a referência técnica promove a `binding`.
4. Uma decisão que contradiz um `BD-*` da Product Spec é **divergência**: não
   decida, registre em `Divergences` e oriente emenda na Product Spec (trio).
   Siga com o que não depende dela.

Não há limite fixo de perguntas, mas não pergunte o que o código ou as
constitutions já respondem.

### 7. Escrever o documento e os contratos

1. Copie [template.md](template.md) para `specs/<feature>/architecture.md` e
   preencha as seções do veredito. Remova as que o veredito não exige; não
   deixe "N/A".
2. Headings em inglês, como no template (são verificáveis por máquina). O
   conteúdo segue o idioma da Product Spec.
3. Contratos em `specs/<feature>/contracts/`, legíveis por máquina, conforme
   [reference.md](reference.md#contratos). A tabela `Contracts` do documento
   aponta para cada arquivo; a prosa não redefine o que o arquivo diz.
4. Diagramas em Mermaid (componentes e sequências, incluindo caminhos de
   falha).
5. `Version` começa em `arch-v1` na criação.

### 8. Validar

1. **Contratos**: valide a sintaxe de cada arquivo. Para OpenAPI, se houver
   Node: `npx --yes @redocly/cli lint specs/<feature>/contracts/openapi.yaml`
   (requer rede). Sem ferramenta disponível, faça revisão estrutural e diga
   ao usuário que o lint não rodou.
2. **Checklist**: crie `specs/<feature>/checklists/architecture.md` com os
   itens de [reference.md](reference.md#checklist), avalie cada um citando a
   seção do documento e corrija o que falhar (máx. 3 iterações). Item de
   herança falhando é bloqueante: resolva com o usuário antes de concluir.

### 9. Reportar

Informe:

- Caminho do documento e dos contratos, veredito e `Version`.
- Product Spec herdada e versão fixada.
- Resultado do checklist e do lint.
- Divergências abertas.
- Próximos passos:
  1. Commit e PR no repositório de specs, com aprovação da referência técnica
     e do tech lead de cada repo do mapa de impacto.
  2. Após o merge, tag própria: `git tag <feature-dir>/arch-v1` (namespace
     separado do da Product Spec) e `git push origin <tag>`.
  3. Cada Engineering Spec passa o caminho deste documento ao
     `/speckit.specify`, que fixa `Architecture doc` pela tag.

Não commite, não abra PR e não crie tag a menos que o usuário peça.

## O que não fazer

- Alterar a Product Spec ou qualquer arquivo dentro de `engineering/`.
- Redefinir problema, escopo, jornadas ou success criteria.
- Fixar schema interno, módulos, frameworks ou tasks de um repositório.
- Ler a constitution de um repo para impor regra ao outro: cada constitution
  restringe só o lado dela do contrato.
- Decidir sozinho uma decisão `binding`.

## Additional resources

- Regras (fronteira, avaliação, contratos, checklist, emendas): [reference.md](reference.md)
- Template do documento: [template.md](template.md)