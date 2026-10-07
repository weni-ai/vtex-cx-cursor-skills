# Architecture Document: regras

## Regra da fronteira

Uma decisão pertence ao Architecture Document **se, e somente se, atravessa
uma fronteira**: mudá-la obriga outro repositório, outro time ou outro serviço
a mudar, ou ela tem impacto de plataforma (custo, compliance, novo datastore,
nova infra). Se ela pode mudar sem que ninguém fora do repositório perceba,
pertence à Engineering Spec.

Teste prático: "quem precisa aprovar se isto mudar?". Se a resposta é "só o
time do repositório", a decisão sai do documento.

| Decisão | Onde mora |
|---------|-----------|
| Qual serviço é dono de qual entidade | Architecture Document |
| Novo datastore, fila, cache ou serviço | Architecture Document |
| Consistência entre serviços (síncrona, eventual, saga) | Architecture Document |
| Payload de API, evento ou mensagem host ↔ microfrontend | Architecture Document (contrato) |
| Modelo de erro, autorização vista pelo cliente, idempotência | Architecture Document (contrato) |
| Classificação de dado pessoal, retenção, LGPD | Architecture Document |
| Pico, latência-alvo e orçamento de erro de um fluxo entre serviços | Architecture Document |
| Ordem de deploy entre repositórios, flags compartilhadas | Architecture Document |
| Colunas, índices e migrations internas de um serviço | Engineering Spec |
| Módulos, camadas, componentes internos | Engineering Spec |
| Bibliotecas e frameworks dentro do serviço | Constitution do repo + Engineering Spec |
| Tasks e estimativas | Fora dos dois (plan/tasks) |

Fixar schema interno aqui transforma toda mudança trivial de coluna em emenda
transversal — e o time para de respeitar o processo.

## Avaliação

Critérios, cada um com evidência da Product Spec (seção ou ID):

1. **Mais de um repositório ou time muda** — `Affected product surfaces and
   modules`, `Teams and products involved`.
2. **Uma interface pública entre repositórios muda** — endpoint novo ou
   alterado, evento, mensagem host ↔ microfrontend. Feature fullstack com
   endpoint novo quase sempre cai aqui.
3. **Novo serviço, datastore, fila ou infraestrutura** — `Data and persistence
   expectations`, hipóteses técnicas.
4. **Dado de um serviço lido ou escrito por outro** — `Interactions with other
   modules or products`, `Key Entities`.
5. **Impacto de segurança, privacidade ou compliance** — `Privacy & Data
   Protection`, `Privacy and security impact`.
6. **Escala além do que os serviços afetados suportam hoje** — `Volume and
   scale`, NFRs. Confronte com o estado atual do código.

Veredito:

- Só o critério 1 e/ou 2 → `contract-only`.
- Qualquer um de 3–6 → `full`.
- Nenhum (um único repositório, nenhuma interface entre repos muda) →
  `not-required`.

O veredito `contract-only` existe para o documento não virar cerimônia: sem
ele, toda feature fullstack exigiria o documento completo, ou o contrato
ficaria sem dono.

## Contratos

Os arquivos em `specs/<feature>/contracts/` são a fonte da verdade. Frontend
gera mocks e tipos deles; backend testa contra eles.

A tabela `Contracts` do documento é o **índice completo** desses arquivos,
com caminho relativo ao documento (`contracts/openapi.yaml`). O
`/speckit.specify` de cada repositório recebe só o documento e descobre os
contratos por essa tabela: lê os arquivos das linhas em que o repositório é
produtor ou consumidor. Arquivo fora da tabela não é lido por ninguém; linha
sem arquivo bloqueia a Engineering Spec.

| Kind | Arquivo |
|------|---------|
| HTTP | `contracts/openapi.yaml` (OpenAPI 3.1; um arquivo por produtor se houver mais de um: `openapi.<repo>.yaml`) |
| Evento / fila | `contracts/events/<event-name>.schema.json` (JSON Schema 2020-12) ou `contracts/asyncapi.yaml` quando houver vários canais |
| Mensagem host ↔ microfrontend | `contracts/messages/<message-name>.schema.json` |

Regras:

- Só o que **atravessa** a fronteira. Endpoint usado apenas internamente pelo
  serviço não entra.
- Recurso já existente que a feature altera: descreva só o delta, e diga na
  tabela `Contracts` qual versão atual ele estende.
- Versione em SemVer (`info.version` no OpenAPI, `$id` versionado no schema) e
  declare compatibilidade — a constitution raiz (*Versioned Contracts*) vale
  para o próprio contrato.
- Exemplos (`examples`) em toda resposta e evento: são eles que viram mocks.
- Respeite a constitution de **cada lado** só no lado dela. Exemplos comuns:
  - Backend *Bounded Retry Over REST* → operação com retry precisa de
    `Idempotency-Key` ou chave de deduplicação no contrato.
  - Backend *Never Trust the Client* → o contrato define o erro que o cliente
    recebe quando a autorização falha.
  - Frontend *API and Data Boundaries* → o frontend normaliza no adapter; o
    contrato segue a convenção do produtor, sem negociar casing.
  - Frontend *Async State Correctness* → a guarda contra envio duplicado
    combina com a idempotência do backend.
  - Frontend Platform *Communication* → mensagens host ↔ microfrontend têm
    schema próprio.

## Checklist

Grave em `specs/<feature>/checklists/architecture.md`:

```markdown
# Architecture Document Checklist: [FEATURE NAME]

**Purpose**: Validate the architecture document before approval
**Created**: [DATE]
**Document**: [link to architecture.md]

## Inheritance

- [ ] Exactly one Product Spec is referenced, pinned by commit or tag
- [ ] Every BD-* that constrains the design is listed
- [ ] Nothing redefines problem, scope, journeys or success criteria
- [ ] No decision contradicts a BD-*; Divergences is `none` or links to an amendment

## Assessment

- [ ] Every criterion has evidence from the Product Spec
- [ ] The verdict follows from the criteria and was confirmed by the user
- [ ] Only the sections required by the verdict are present

## Boundaries

- [ ] Every impacted repository appears in the Impact Map with its role
- [ ] Every decision crosses a boundary (no internal schema, modules or frameworks)
- [ ] Every decision lists alternatives and consequences
- [ ] Every binding decision names who decided it

## Contracts

- [ ] Every contract has a machine-readable file, a producer and its consumers
- [ ] The Contracts table is the complete index: every file under `contracts/` has a row, and every row's file exists
- [ ] Every contract file passed lint, or the report says lint did not run
- [ ] Every response and event has examples usable as mocks
- [ ] Error model, authorization failure, idempotency and correlation ID are defined
- [ ] Each side's constitution is honored on its own side of the contract
- [ ] Compatibility and deprecation are stated for every changed contract

## Delivery

- [ ] What each repository can build in parallel against mocks is stated
- [ ] Deploy order, flags and compatibility window are stated
- [ ] Binding NFRs are quantified, with peak and window (full only)
- [ ] Data ownership and consistency are stated for every shared entity (full only)
```

## Emendas

O documento muda durante a implementação — isso é esperado. A emenda precisa
ser leve, senão os times desviam em silêncio.

1. **Origem.** Uma Engineering Spec que precisa contradizer uma decisão
   `binding` ou um contrato daqui não implementa o desvio: registra em
   `Divergences` dela, apontando para a emenda **neste documento**.
2. **Dono.** Emenda técnica é aprovada pela referência técnica e pelos tech
   leads do mapa de impacto — **não pelo trio**. Se a emenda tocar um `BD-*`,
   aí sim vira emenda na Product Spec.
3. **Execução.** Atualize o documento e os contratos, adicione uma linha no
   `Amendment Log` com as Engineering Specs que precisam re-fixar, bump de
   `Version` (`arch-v2`, …) e `Last amended`.
4. **Re-fixação.** Após o merge, nova tag `<feature-dir>/arch-vN`. Toda
   Engineering Spec consumidora atualiza `Architecture doc` para a nova tag.
5. **Product Spec emendada.** Nova tag da Product Spec → re-fixe a herança
   deste documento pelo mesmo Gate 0 do `SKILL.md` e registre no
   `Amendment Log`, mesmo que nada mais mude.

Status `Superseded by <link>` só quando outra feature substitui o desenho
inteiro; o documento antigo não é apagado.

## Tags

- Product Spec e Architecture Document usam namespaces de tag separados, para
  que uma emenda num não crie uma versão "fantasma" do outro.
- Architecture Document: `<feature-dir>/arch-vN` (ex.: `002-internal-ticket/arch-v1`).
- Ao fixar a Product Spec, ignore tags `*/arch-v*`; ao fixar este documento,
  considere só essas.

## Consumo pelas Engineering Specs

| Seção da Engineering Spec | Deriva de |
|---------------------------|-----------|
| `Architecture doc` (herança) | Permalink + tag `<feature-dir>/arch-vN` |
| `Inherited binding decisions` | `BD-*` da Product Spec + `AD-*` marcados `binding` |
| `Scope in This Repository` | Linha do repo no `Impact Map` |
| `Contracts` | Referencia, por permalink no commit fixado, os arquivos de `contracts/` em que o repo é produtor ou consumidor; não os redefine |
| `Peak Load` | `Binding Non-Functional Requirements` |
| `Rollout and Rollback` | `Delivery Sequence and Parallelism` |

## Nome

O artefato da feature é **pontual**: congela após a entrega e é substituído
por documentos futuros, no estilo ADR. Não confunda com um contexto
arquitetural **permanente** de um repositório (ex.: `.specify/context/`), que
descreve o sistema e não uma feature.
