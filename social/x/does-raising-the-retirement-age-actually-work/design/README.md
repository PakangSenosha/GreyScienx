# Policy dossier poster template

This campaign-local template replaces the uniform stacked-card layout with an asymmetric research-poster system. It retains the GreyScienx black, warm-white and coral palette, outlined wordmark, sharp rules, square geometry and evidence-first editorial hierarchy.

## Structure

- Black editorial field for the headline and model-status stamp.
- Narrow evidence rail for public-facing model scope or scenario metadata; campaign sequence numbers stay internal to filenames and the manifest.
- Warm-white evidence desk with a coral entry rule.
- One of four evidence modes: `stat`, `bars`, `steps`, or `chartImage`.
- Visible qualification, interpretation caption, source and display URL.

## Render

```powershell
python social/x/does-raising-the-retirement-age-actually-work/design/render_poster.py `
  social/x/does-raising-the-retirement-age-actually-work/design/template-preview.json `
  social/x/does-raising-the-retirement-age-actually-work/design/template-preview.png `
  --html-out social/x/does-raising-the-retirement-age-actually-work/design/template-preview.html
```

The renderer embeds the approved outlined GreyScienx wordmark from the repository skill assets. Final PNGs are fixed at 1080 x 1350 and checked against the ordinary 5 MB X image ceiling.
