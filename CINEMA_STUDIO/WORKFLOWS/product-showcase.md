# Workflow — Vitrine de produto (Product Showcase)

Vídeo que apresenta um produto físico ou digital (app, plataforma, curso).

## 1. Brief → `brief/`
- Produto, 3 benefícios principais (no máximo), público, CTA (comprar, testar, baixar).
- Coletar logos, fontes e cores da marca em `ASSETS/logos` e `ASSETS/fonts`.

## 2. Roteiro → `scripts/`
- **Gancho visual → produto em destaque → benefício 1, 2, 3 → prova social / números → CTA**.
- Cada benefício = um plano + uma frase curta na tela.

## 3. Storyboard → `storyboard/`
- Produto físico: hero shot, detalhes (macro), em uso, comparativo.
- Produto digital: gravação de tela, zoom nas funções, mockup em dispositivo.

## 4. Material → `footage/`, `ASSETS/images`
- Produto físico: fundo limpo, luz suave, giro 360°.
- Produto digital: gravar tela em resolução alta (≥ 1440p), cursor limpo, dados de exemplo realistas.

## 5. Composição (Remotion) → `src/`, `public/`
- Mockups de dispositivo, zoom/pan suave sobre a tela, destaque de cliques.
- Callouts e textos curtos sincronizados com a locução.
- Componentes reutilizáveis: `ProductHero`, `FeatureCallout`, `CTA`, `LogoEnd`.

## 6. Áudio → `audio/`
- Trilha leve e positiva; SFX sutis em cliques e transições.
- Loudness −14 LUFS / −1 dBTP.

## 7. Legendas
- Sempre legendar (a maioria assiste sem som nas redes).
- Legendas animadas / karaokê (`caption.py` ou Remotion).

## 8. Entrega → `EXPORTS/`
- 16:9 (site, YouTube), 9:16 (Reels/TikTok/Shorts), 1:1 e 4:5 (feed).
- Versões curtas de 6s e 15s para anúncios.
- Checagem final com `check.py`.
