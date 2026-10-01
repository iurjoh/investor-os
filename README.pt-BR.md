# Investor OS - Organização de investimentos com cálculos auditáveis

[English](README.md) | **Português (Brasil)**

![Estágio: antes do beta externo](https://img.shields.io/badge/stage-pre--external--beta-yellow)
![Licença: MIT](https://img.shields.io/badge/license-MIT-blue)

Carteira, dividendos, alocação e metas com cálculos transparentes e determinísticos.

**[Prévia pública](https://investor-os-app.pages.dev/)** · Código privado · Documentação conferida em **01/10/2026**.

[Snapshot: Landing pública desktop, 01/10/2026](https://drive.google.com/file/d/1nmM5L_m1S-PdOMEbbOeNIgHnR2rwDtpS/view?usp=drivesdk)

> A URL pública é uma landing page, não um dashboard funcional. Os documentos registram uma planilha V1 implementada, com beta externo e distribuição ainda pendentes. Há também uma pequena base de cálculos Python. Listar tecnologias planejadas não significa que o app de assinatura esteja implementado.

## Ideia e planejamento

Dados da carteira ficam espalhados entre corretoras e planilhas. O Investor OS busca reunir custo médio, dividendos, alocação e metas com fórmulas inspecionáveis. Começa pela planilha e por uma base de uso pessoal, não por IA financeira opaca.

| Necessidade | Resposta planejada |
| --- | --- |
| Entender o custo após venda parcial | Custo médio com taxas, impostos e câmbio. |
| Ver concentração | Alocação por ativo, setor, tipo, país/região e moeda. |
| Conferir um número importado | Fonte, momento observado, vigência e moeda. |
| Manter controle e evitar mensalidades | Local-first antes de contas hospedadas ou cobrança. |

Objetivos: cálculos claros, resumos úteis, ajustes manuais e dados auditáveis. Fora do escopo: ordens em corretoras, recomendações individuais, trading automático, declaração de impostos, cotações de alta frequência e rede social.

## Funcionalidades e escopo

**Planilha V1, conforme documentação:** posições, transações, custo médio, dividendos/conferência, câmbio, alocação, metas, gráficos e checks com dados fictícios. Preços e câmbio manuais são intencionais, não um feed ao vivo.

**Base Python existente:** Decimal, ordenação cronológica, custo de compras com taxas/impostos/câmbio, redução de custo na venda parcial, zeragem na venda total e rejeição de venda acima da posição.

**Ainda não entregue como dashboard web:** autenticação, sincronização multiusuário, corretoras, cotações automáticas, assinaturas e distribuição pública.

## Arquitetura

```mermaid
graph TD
    A[Entradas da planilha] --> B[Calculos deterministas do ledger]
    B --> C[Posicoes, alocacao, dividendos e metas]
    C --> D[Dashboard e checks]
    E[Base Python Decimal] --> F[Testes locais]
    G[Modelo PostgreSQL alvo] -. futuro .-> H[Interface e tarefas locais]
```

| Etapa | Tecnologia e situação |
| --- | --- |
| Produto V1 | Planilha compatível com Excel/LibreOffice, descrita em product/. |
| Base de cálculos | Biblioteca padrão Python e Decimal, em src/investor_os/portfolio.py. |
| Dados | Modelo PostgreSQL em database/; não comprova banco hospedado funcionando. |
| Direção pessoal | Interface local, tarefas locais, exportação CSV/JSON e backup criptografado: trabalho futuro. |
| Site público | Apresentação do produto, sem conta ou carteira funcional. |

[Arquitetura](docs/architecture.md) registra a direção atual: uso pessoal, local-first e custo zero. Propostas antigas citam Next.js, Supabase, n8n Cloud, Vercel, OpenAI e Gumroad; são opções históricas/planejadas, não serviços contratados. A direção atual rejeita cartão, trials e cobrança automática por excedente. IA não substitui aritmética financeira determinística.

## Design e snapshots

Capturas guardadas no Drive privado do dono. Os links exigem acesso; não são imagens públicas incorporadas. O upload de imagens no repo falhou nesta atualização; não foram mantidos placeholders quebrados.

A prévia atual usa fundo escuro, verde, recursos numerados e status explícito. O desenho da planilha separa entradas, fórmulas, checks e onboarding.

| Snapshot | Data | Contexto |
| --- | --- | --- |
| [Landing desktop](https://drive.google.com/file/d/1nmM5L_m1S-PdOMEbbOeNIgHnR2rwDtpS/view?usp=drivesdk) | 01/10/2026 | Introdução pública sem dados da carteira. |
| [Landing celular](https://drive.google.com/file/d/1aNNB_NO_bI5u_5ICVVCJ071dzct47EJP/view?usp=drivesdk) | 01/10/2026 | Introdução responsiva, viewport de 390px. |

Não são capturas do dashboard. Wireframes antigos e uma captura verificável da planilha ainda não estão reunidos aqui. Usar somente artefatos reais com dados sintéticos; rotular mockups como mockups.

## Processo de desenvolvimento

1. Definir objetivos, não objetivos e cálculo transparente.
2. Especificar abas, fórmulas e checks em [implementação XLSX](product/xlsx-implementation.md).
3. Construir a etapa de planilha e registrar gates em [checklist](product/release-checklist.md).
4. Estabelecer arquitetura pessoal, núcleo Python e regressões locais.
5. Restaurar repositório limpo com fixtures sintéticas em 30/09/2026. Isso descreve o repo atual, não exclusão de toda cópia ou cache possível.
6. Adicionar documentação bilíngue, snapshots e MIT em 01/10/2026.

Mudanças exatas ficam no Git. Registrar requisito, decisão, implementação, teste e imagem juntos. Não reconstruir datas ou aprovações não verificadas.

## Desempenho

Não há baseline medido de tempo do dashboard, throughput ou Core Web Vitals na documentação inspecionada. A landing não é benchmark dos cálculos.

Antes de afirmar velocidade, medir quantidade de dados, tempo de importação/cálculo, memória, hardware, versão Python/navegador e commit. Para dashboard web, acrescentar LCP/INP/CLS datados e cenários sintéticos realistas.

## Segurança e privacidade

- Somente carteiras fictícias em exemplos. Não versionar exportações de corretoras, saldos, credenciais ou identificadores privados.
- A árvore restaurada atual usa dados sintéticos; não se afirma exclusão de todas as cópias/cache antigos.
- Fórmulas determinísticas. Organização de carteira, não recomendação de investimento ou certificado tributário.
- [Tracker beta](product/beta-tracker.md) deve ser anonimizado; conferir o arquivo antes de compartilhar.
- Segredos fora do Git. Local-first e backup criptografado são requisitos-alvo, não prova de criptografia de todo artefato atual.
- Esta documentação não ativou serviços pagos nem CI hospedado. Manter Actions desligado até verificar billing, conforme arquitetura.

## Testes e execução local

O [checklist](product/release-checklist.md) registra 20 casos de planilha usados na validação, mas testers externos e publicação continuam pendentes. Esta atualização não obteve nem executou a planilha e não certifica esses 20 resultados de forma independente.

`tests/test_portfolio.py` contém quatro testes: venda parcial, câmbio/taxas/impostos, zeragem na venda total e rejeição de venda excessiva. **4/4 passaram localmente em 01/10/2026 com o código recuperado do repo.** É validação limitada do núcleo, não teste completo do produto.

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
# Alternativa equivalente:
sh run_tests.sh
```

O módulo inspecionado usa apenas a biblioteca padrão Python. Consultar [XLSX](product/xlsx-implementation.md) para a planilha. Não existe app `npm run dev` neste repo.

## Publicação e próximos passos

- [ ] Beta controlado com 5-10 testers.
- [ ] Revisar feedback e corrigir usabilidade.
- [ ] Completar distribuição, entrega e instruções de exportação/backup.
- [ ] Validar MVP pessoal: importação, ajustes de preço/câmbio, dashboard e checks.
- [ ] Ampliar regressões e medir desempenho.
- [ ] Considerar contas hospedadas, múltiplos usuários e cobrança só após validar uso pessoal e demanda.

Não rotular a planilha como produção antes do gate externo e dos testes de cálculo. Publicar README não equivale a publicar produto.

### Guia do repositório

- [Arquitetura](docs/architecture.md)
- [Implementação XLSX](product/xlsx-implementation.md)
- [Checklist](product/release-checklist.md)
- [Escopo beta](product/private-beta.md)
- [Guia do tester](product/beta-tester-guide.md)
- [Feedback](product/beta-feedback.md)
- [Procedimento beta](product/beta-launch-sop.md)
- [Rascunho do convite](product/beta-invitation.md)
- [Tracker anonimizado](product/beta-tracker.md)
- [Gates públicos](product/public-launch-readiness.md)

## Créditos e licença

Iuri Johansson. Núcleo Python com biblioteca padrão; planilha destinada a Excel/LibreOffice. Terceiros mantêm seus próprios termos.

[MIT](LICENSE), copyright 2026 Iuri Johansson. Repositório permanece privado.
