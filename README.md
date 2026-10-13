# HYBRID Training 2.3 — Fitness Neon (prévia visual)

Esta versão é um **teste visual** inspirado em interfaces de treino premium: fundo preto OLED, cards grafite, tipografia Montserrat para títulos/números e Inter para interface, com verde (força), rosa (corrida) e azul (atividade/recuperação). Não é um produto Apple nem é afiliado ao Apple Fitness+.

## O que inclui

- **Todas as funcionalidades da versão 2.2**, inclusive tudo que havia na 2.1 (Agenda sem redirecionamento, símbolos SVG, descanso automático, campos corrigidos, configuração da rotina semanal, registro de cargas, gráficos, editor, calendário e backup).
- **Identidade visual nova:** cores, tipografia, cards, botões, calendário, navegação e cronômetro.
- **Anéis da semana na página inicial**, calculados a partir de sua rotina configurada e dos registros reais. Contam sessões registradas, não calorias nem esforço fisiológico.
- **Fontes via Google Fonts:** carregam com internet. Offline ou indisponíveis, o app volta às fontes do sistema, sem bloquear as funções.
- **Compatível com os dados anteriores**, chave local `hybridTrainingV2` inalterada e sem alterações de schema. O app segue sem Supabase.

## Testar antes de publicar

Abra `index.html` localmente num navegador de computador para prévia (alguns recursos PWA requerem HTTPS). Se quiser testar no iPhone como app instalado, publique os arquivos no GitHub Pages. Faça backup JSON de seus treinos antes de substituir os arquivos atuais.

Para instalar, extraia e envie o **conteúdo** desta pasta à raiz do mesmo repositório. `index.html`, `app.js`, `styles.css`, `fitness-theme.css`, `sw.js`, `manifest.webmanifest`, ícones e pasta `tests` ficam na raiz. O service worker atualiza o cache para `hybrid-static-v2.3.0`.

## Acessibilidade

Inputs mantêm tamanho mínimo para toque e contraste em dark mode. Respeita `prefers-reduced-motion`, utiliza SVGs sem emoji e continua utilizável mesmo sem conexão com as fontes.
