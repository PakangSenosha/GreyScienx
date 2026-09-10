# GreyScienx

Semi-professional research press. Each researcher has a home. Each paper becomes a site.

Built by Pakang Senosha, MSc Epidemiology and Biostatistics, University of Pretoria.

## Addresses

- Press: `greyscienx.com`
- Researcher: `pakangsenosha.greyscienx.com`
- Paper: `pakangsenosha.greyscienx.com/searching-for-trading-edges`

Until a custom domain is attached, the same structure is served on Vercel as:

- `/`
- `/r/pakang-senosha`
- `/r/pakang-senosha/searching-for-trading-edges`
- `/r/pakang-senosha/wits-staff-education`

## Local

```bash
npm install
npm run dev
```

Optional: copy `.env.example` to `.env.local` and set `XAI_API_KEY` so `/submit` distills with a model. Without a key, GreyScienx still builds a preview site from the pasted manuscript.
