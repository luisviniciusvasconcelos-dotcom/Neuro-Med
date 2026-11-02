# CINEMA_STUDIO

Estúdio de produção de vídeo: comerciais, peças cinematográficas e vitrines de produto.

## Estrutura

| Pasta | Para quê |
|---|---|
| `ASSETS/` | Biblioteca compartilhada entre projetos: `footage`, `images`, `music`, `sound-effects`, `voiceovers`, `fonts`, `logos` |
| `PROJECTS/<nome>/` | Um projeto por pasta. Copie `nome-do-comercial/` e renomeie |
| `EXPORTS/` | Entregas finais: `4K`, `1080p`, `vertical` (9:16), `social-media` |
| `WORKFLOWS/` | Passo a passo de cada tipo de peça |

## Novo projeto

```bash
cp -r PROJECTS/nome-do-comercial PROJECTS/meu-comercial
```

Depois preencha `PROJECTS/meu-comercial/README.md` e siga o workflow correspondente:

- [`WORKFLOWS/commercial.md`](WORKFLOWS/commercial.md) — comercial 15/30/60s
- [`WORKFLOWS/cinematic.md`](WORKFLOWS/cinematic.md) — peça cinematográfica / institucional
- [`WORKFLOWS/product-showcase.md`](WORKFLOWS/product-showcase.md) — vitrine de produto

## Ferramentas

- **Remotion** (plugin `remotion`): composição, motion graphics, legendas animadas. Código em `PROJECTS/<nome>/src/`, assets estáticos em `PROJECTS/<nome>/public/`.
- **ffmpeg-skill** (plugin `ffmpeg-skill`): cortes, remoção de silêncio, reenquadramento, loudness, checagem de entrega — tudo com FFmpeg local.
- **video-editing** (skill do projeto): pipeline geral captura → corte → composição → áudio → acabamento.

## Mídia pesada

Vídeos, áudios, renders e exports **não vão para o git** (ver `.gitignore`); só a estrutura de pastas é versionada. Guarde os originais num drive/backup à parte.

## Convenção de nomes

`<projeto>_<peça>_<formato>_v<NN>.mp4` — ex.: `upmed_lancamento_16x9-1080p_v03.mp4`
