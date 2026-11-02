# Workflow — Comercial (15 / 30 / 60s)

## 1. Brief → `brief/`
- Objetivo, público, mensagem única, CTA, prazo, formatos de entrega.
- Referências visuais e sonoras.

## 2. Roteiro → `scripts/`
- Estrutura: **gancho (0–3s) → problema → solução/produto → prova → CTA + logo**.
- Contar palavras da locução: ~2,5 palavras/segundo (30s ≈ 75 palavras).

## 3. Storyboard → `storyboard/`
- Um quadro por plano, com duração, enquadramento, movimento e texto na tela.
- Planejar já as versões 16:9 e 9:16 (área segura para texto no centro).

## 4. Captação / seleção → `footage/`
- Copiar material bruto; inspecionar com `probe.py` (ffmpeg-skill): resolução, fps, duração, áudio.
- Padronizar fps do projeto (24 ou 30) antes de editar.

## 5. Corte bruto
- Cortes sem recompressão onde possível (`cut.py`), remover silêncios da locução (`silence.py`).
- Bater cortes na trilha (beats) quando houver música.

## 6. Composição (Remotion) → `src/`, `public/`
- Texto animado, lower thirds, logo, CTA, transições.
- Duração e fps da composição vindos do `probe` do material.

## 7. Áudio → `audio/`
- Locução limpa, trilha com ducking sob a voz, SFX nos cortes.
- Loudness: **−14 LUFS / −1 dBTP** (web/social); **−23 LUFS** se for para TV (EBU R128).

## 8. Revisão → `renders/`
- Render de revisão 1080p com versão no nome (`_v01`, `_v02`…).
- Registrar feedback na tabela de versões do README do projeto.

## 9. Entrega → `EXPORTS/`
| Destino | Formato |
|---|---|
| `4K/` | 3840×2160, H.264/H.265, alta taxa |
| `1080p/` | 1920×1080, H.264 |
| `vertical/` | 1080×1920 (9:16) — Reels, TikTok, Shorts |
| `social-media/` | 1080×1080 (1:1) e 1080×1350 (4:5) |

- Reenquadrar com `fit.py --aspect 9:16` e conferir texto na área segura.
- Checar cada arquivo final (`check.py`): duração, codec, loudness, sem frames pretos.
