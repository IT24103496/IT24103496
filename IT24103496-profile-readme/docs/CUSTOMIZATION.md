# Customize the Signal Shield theme

The design theme is **Signal Shield**: deep navy surfaces, teal network signals, indigo routing accents and lime security indicators.

## Update verified details

Edit the human-written sections of `README.md` and `profile.config.json` when Dasun wants to add confirmed certifications, projects, contact channels or a portfolio. Avoid presenting technology badges as skills unless he wants those technologies public.

## Highlight future projects

Add future public repository names to `highlight_repositories` in `profile.config.json`:

```json
"highlight_repositories": ["builtsmart", "Vehical-Rental-Service", "new-secure-project"]
```

The next **Profile Bot** run will prioritize those public repositories in its generated table.

## Avatar and photography

The README currently displays Dasun's public GitHub avatar dynamically, so changes made on GitHub appear automatically. To use a separate portrait later, add an approved optimized image to `assets/` and replace only the avatar element in `README.md`.
