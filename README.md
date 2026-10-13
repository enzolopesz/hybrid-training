# HYBRID Training 2.0

Aplicativo web de treino híbrido (musculação + corrida) feito em HTML, CSS e JavaScript, sem dependências e compatível com GitHub Pages.

## Atualizar o repositório existente

Repositório: https://github.com/enzolopesz/hybrid-training

1. **Faça um backup primeiro.** Na versão anterior do aplicativo, abra **Backup → Baixar backup (.json)** e guarde o arquivo no iPhone/Drive, especialmente se já registrou pesos. **Não limpe os dados do navegador.**
2. Extraia `hybrid-training-v2.zip`.
3. Faça upload **do conteúdo da pasta**, não da própria pasta ZIP, para a **raiz** do repositório `hybrid-training`: `index.html`, `styles.css`, `app.js`, `sw.js`, `manifest.webmanifest`, três ícones, `.nojekyll` e opcionalmente `README.md` e `tests/`.
4. GitHub → **Code → Add file → Upload files → Commit changes**. Se estiver usando VS Code, copie os arquivos para a raiz do repositório, faça commit e push na branch que publica o Pages (normalmente `main`).
5. Se o Pages já estiver configurado, NÃO precisa recriá-lo. Caso contrário, configure Settings → Pages → Deploy from a branch → `main` → `/(root)`.
6. Abra https://enzolopesz.github.io/hybrid-training/ . Se carregar a versão antiga, atualize a página, feche e reabra o ícone do aplicativo, ou use **Ajustes → Verificar atualização do app**. Não limpe o armazenamento local para forçar atualização.
7. Se o histórico não aparecer automaticamente, acesse **Ajustes → Restaurar backup v1 ou v2** e selecione o JSON salvo no passo 1.

**Importante:** a migração automática lê a chave antiga `hybridTrainingPersonalV1` e grava a nova `hybridTrainingV2`. O conteúdo antigo não é excluído. Isso só funciona quando as duas versões usam a mesma origem/armazenamento do navegador; o Safari e o aplicativo instalado podem manter armazenamentos separados em algumas situações. Se ocorrer, restaure o backup JSON dentro da versão nova.

## Recursos da versão 2.0

- Início: resumo da semana e acesso rápido aos treinos.
- Treinar: registro de séries (carga, reps, concluído), autofill do treino anterior, controles +/−, notas, RIR e finalização.
- Timer de descanso automático por exercício, pausa, +/− 30 s e aviso sonoro opcional enquanto o aplicativo está ativo.
- Progressão sugerida quando todas as séries anteriores atingem o limite superior de reps; você decide se aumenta após conferir a execução e o RIR.
- Editor de fichas de musculação: adicionar, excluir, reordenar ou modificar exercícios, séries, faixas de repetição, descanso e incremento de peso. Registros já iniciados preservam cópia dos exercícios.
- Agenda: calendário, escolha do treino por data (com salvamento), corridas cadastradas com base nos prints do Runna e importação **manual** de arquivo `.ics` com eventos de corrida. A prova de 8 km em 15/11/2026 e a recuperação posterior têm atenção especial.
- Evolução: gráficos de cargas, volume semanal de musculação, quilômetros realizados por semana, recordes de cargas, medidas corporais e histórico.
- Dados locais: armazenamento local, exportação em JSON (backup completo) e CSV (consultar séries); restauração JSON v1/v2.
- PWA: ícone na tela inicial e disponibilidade offline **após o primeiro carregamento com internet e instalação do service worker**.

## Limitações nesta versão

- **Supabase fica para a fase final.** Não há conta/login, banco remoto ou sincronização entre aparelhos. O GitHub Pages hospeda a interface, não guarda os seus pesos.
- O Runna não está conectado à sua conta; o calendário é uma **transcrição dos prints** e pode ser complementado com importação `.ics` ou cadastro manual. Consulte o Runna para confirmar alterações da prescrição.
- No iPhone, avisos sonoros do timer dependem do aplicativo ativo e da permissão do sistema para áudio; não há notificação push em segundo plano.
- A progressão é uma sugestão, não uma prescrição automática. Monitore dores e recuperação e mantenha o treino leve ou reduzido na semana da prova.
- Recomenda-se exportar backup JSON periodicamente — idealmente após cada sessão importante ou pelo menos semanalmente.

## iPhone

Safari → https://enzolopesz.github.io/hybrid-training/ → Compartilhar → Adicionar à Tela de Início → Abrir como App, quando disponível.

## Rodar localmente

Basta servir os arquivos estáticos por HTTP (em Python: `python -m http.server 8000` na pasta). Em acesso local por `http://localhost` o service worker pode ser instalado. Abrir o `index.html` como arquivo ainda exibe a interface, mas não reproduz exatamente a hospedagem do GitHub.

Testar a lógica com Node.js 18+: `node tests/smoke-test.cjs`.

## Estrutura

- `index.html`: documento principal, navegação e metadados.
- `styles.css`: interface responsiva, dark mode e layout para iPhone.
- `app.js`: lógica e persistência dos registros.
- `sw.js`: cache e disponibilidade offline com prioridade aos arquivos mais recentes enquanto online.
- `manifest.webmanifest`, `icon-*.png`, `apple-touch-icon.png`: instalação como PWA.
- `tests/smoke-test.cjs`: testes automatizados básicos sem dependências.
