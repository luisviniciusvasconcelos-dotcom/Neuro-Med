# Workflow — Cinematográfico

Peças com foco em atmosfera: institucional, manifesto, teaser, curta.

## 1. Conceito → `brief/`
- Tema, emoção dominante, referências de filmes/fotografia, paleta de cores.
- Definir aspecto: 2.39:1 (scope), 1.85:1 ou 16:9.

## 2. Roteiro e narrativa → `scripts/`
- Arco em três atos, mesmo em 60s: abertura, tensão, resolução.
- Locução opcional; deixar espaço para silêncio e som ambiente.

## 3. Storyboard e shot list → `storyboard/`
- Planos abertos para estabelecer, fechados para emoção, detalhes para ritmo.
- Anotar movimento de câmera, lente e luz de cada plano.

## 4. Material → `footage/`
- Preferir 24 fps; captar em perfil log quando possível.
- Inspecionar com `probe.py`; separar takes bons.

## 5. Montagem
- Ritmo mais lento: planos de 3–6s, cortes no movimento ou no som.
- J-cuts e L-cuts (som antecipa/estende a imagem).

## 6. Cor
- Converter log → Rec.709 com LUT (`color.py` do ffmpeg-skill, que também faz HDR→SDR) e depois grade criativa.
- Manter consistência de pele e de preto entre planos.
- Barras de letterbox para 2.39:1 sobre entrega 16:9, se necessário.

## 7. Textura e finalização (Remotion) → `src/`
- Títulos discretos, tipografia serifada ou condensada, fades longos.
- Grão de filme, vinheta leve, glow nos realces (presets Fusion da skill `video-editing`, se usar DaVinci).

## 8. Desenho de som → `audio/`
- Camadas: ambiente + foley + trilha + voz.
- Dinâmica maior que num comercial; loudness final −14 LUFS (web) ou −23 LUFS (broadcast).

## 9. Entrega → `EXPORTS/`
- Master 4K, versão 1080p, teaser vertical de 15–30s para redes.
- Checagem final com `check.py`.
