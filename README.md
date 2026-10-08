# Luv Visualz — Remote Video Editing

Standalone bilingual (ES/EN) commercial landing page for recurring remote video editing.

## What's included

- `index.html`: Spanish landing page (Spain-friendly phrasing, no country-exclusive jargon)
- `en/index.html`: English landing page
- `assets/style.css`: responsive visual system based on the **public** Luv Visualz site
- `assets/app.js`: accessible slide-out navigation, playable video samples and scroll motion
- `build.py`: optional generator for both localized pages; `python build.py` creates static HTML
- `prepare_assets.py`: optional, one-time migration of real videos, covers, logo and fonts from the public original site into this independent project
- `.nojekyll`: tells GitHub Pages to serve the files without Jekyll

**No dependencies, npm, external database or local server are needed after publishing.**

## IMPORTANT: portfolio media and logo

For accuracy, the first build uses verified existing Luv Visualz project posters and videos from the original site's *public* GitHub Pages at `https://luvvisualz.github.io/work/...`, and uses its existing logo from `/brand/luv-visualz-logo.webp`.

This DOES NOT change or redirect visitors to the original website. However, these shared media resources mean that the new website is not yet fully independent of the original site. To make it **fully independent**, run `python prepare_assets.py` with internet access, then `python build.py`. The generator automatically selects downloaded local copies of the logo and media. Existing production videos may be large, so consider whether GitHub Pages bandwidth is appropriate. Preserve all originals on the old website.

The projects used are Conoflex, Bienestar & Soluciones, Lupart and a Luv personal edit. **Bunker Jump is deliberately excluded** because the original public portfolio explicitly credits that project's edit to Bunker Jump.

Review project-specific role descriptions before commercial launch. The website does not invent client metrics, international work history, reviews or prices.

## Publish with GitHub Pages — independent repository

1. In GitHub, choose **New repository**. Example name: `luv-visualz-editing`. Set Public and create it. **Do not select or reuse `LuvVisualz.github.io`.**
2. Unzip this delivery locally. For complete media independence, run `python prepare_assets.py` and then `python build.py` **before uploading**; this downloads the existing logo, fonts, covers, and four videos without touching the original. If you skip this step, real videos and branding still load from the public original site. Upload the files at the repository root and preserve `en/` and `assets/`.
3. Go to **Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save**.
4. After GitHub finishes deployment, the expected URL has the form `https://luvvisualz.github.io/luv-visualz-editing/`. This is an **example based on the suggested repository name**, not a verified live address.
5. Verify home, `/en/`, menu, WhatsApp and videos from your phone. Once URL is known, update HTML canonical and `hreflang` tags for SEO.
6. If you skipped the asset migration, perform it before treating the site as fully autonomous.

The main website is never modified by any of these steps.

## Content to validate

- Confirm edits and exact roles for each of the 4 videos.
- Confirm which video samples best demonstrate ongoing agency editing rather than on-location filming.
- Add extra examples of YouTube / recurrent video editing if available.
- Finalize a dedicated contact email if desired (current CTAs use the public WhatsApp on the original site).
- Copy media / logo / fonts to independent hosting, and finalize canonical SEO URLs after the first deploy.

## Technical notes

- HTML is static and indexable in both languages; no client-side hydration.
- Language switch stays inside the new site's path.
- Uses semantic sections, keyboard accessible navigation, `prefers-reduced-motion` and lazy cover images.
- Real sample videos are opened only after a user click (`preload=none`), to avoid large mobile downloads.
- No cross-links to the filmmaker portfolio and no quoted rates.

