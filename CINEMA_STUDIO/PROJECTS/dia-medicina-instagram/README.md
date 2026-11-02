# dia-medicina-instagram — "29.10 · Um dia de medicina"

Edição dinâmica 16:9 para Instagram a partir do material de 29/10/2026 (12h21 → 17h28).
Proposta criativa completa em [`brief/proposta.md`](brief/proposta.md).

## Ficha

| Campo | Valor |
|---|---|
| Workflow | cinematic / day-in-the-life |
| Duração | 30 s |
| Formato | 16:9 — 3840×2160 master · 1920×1080 Instagram |
| Trilha | Original, sintetizada para o projeto (sem direitos de terceiros) |
| Status | **v02 renderizada** — aguardando aprovação |

## Decisões aprovadas
- Conceito "o relógio do dia": horários reais (metadados dos arquivos) como tipografia.
- Cirurgia aberta só em flashes curtos (< 1 s), sem identificação do paciente.
  **Publicação depende de autorização do paciente/hospital (CFM).**
- Trilha original 120 BPM em Ré menor, cortes na batida.

## Como reconstruir

```bash
# 1. imagem (cortes, velocidade, cor, layout, push-in) → renders/work/picture.mp4
cd src/edit && python3 build_picture.py
# 2. trilha + efeitos → audio/music.wav, audio/sfx.wav
cd ../audio && python3 score.py
# 3. mixagem com som direto, -14 LUFS / -1 dBTP → audio/mix.wav
python3 mix.py
# 4. tipografia (Remotion, alpha 4K) → src/remotion/out/type.mov
cd ../remotion && npm install && npm run render
# 5. finalização + exportações → renders/
cd ../edit && python3 finish.py v01
```

Requisitos: ffmpeg ≥ 6, Python 3 com numpy + scipy, Node 18+, fontes Inter Display e JetBrains Mono.

## Arquivos-fonte editáveis
- `src/edit/edl.py` — lista de cortes (in/out, duração, velocidade, zoom, layout), correção de cor por clipe e look geral, horários exibidos.
- `src/edit/build_picture.py` — render dos segmentos e concatenação.
- `src/edit/finish.py` — flashes nos impactos, grão, vinheta, sobreposição da tipografia, exportação.
- `src/audio/score.py` — composição da trilha e do sound design (cada instrumento é uma função).
- `src/audio/mix.py` — som direto dos clipes, automação de volume e normalização de loudness.
- `src/remotion/src/Type.tsx` — título, relógio com dígitos rolando a cada corte, cartela final.

## Pastas
- `footage/raw/` — cópias dos 11 clipes originais (fora do git); `footage/photos/` — 4 fotos.
- `audio/` — stems e mix (fora do git).
- `renders/` — renders de revisão (fora do git); entregas finais em `CINEMA_STUDIO/EXPORTS/`.

## Versões

| Versão | Data | Mudanças | Aprovado? |
|---|---|---|---|
| v01 | 02/11/2026 | Primeira montagem completa; QC ok (720 frames, 30,0 s, −14,6 LUFS, pico −1,4 dBFS, sem quadros pretos acidentais) | aguardando |
| v02 | 02/11/2026 | Trilha remixada para alto-falante de celular: na v01 ~95% da energia estava abaixo de 250 Hz e o vídeo soava mudo no celular. Graves mais leves, harmônicos no baixo, ostinato na região média, percussão mais presente, EQ de master. Faixa 400 Hz–8 kHz de −27,7 → −21,7 dB. Imagem idêntica à v01. | aguardando |
