# Itzak's Selection — Movies & Books

[🇨🇳 中文](README_CN.md)

Aggregates award data from Wikipedia in real time. Browse award-winning films and books from major international prizes — no signup, no algorithm, just real awards.

## Usage

**Live site (recommended):** [itzak89.github.io/itzak-movie-book-selection](https://itzak89.github.io/itzak-movie-book-selection/)

Run locally:

```bash
git clone https://github.com/itzak89/itzak-movie-book-selection.git
open index.html
```

## Features

**Movies**
- 22 award categories: Cannes, Venice, Berlin, Oscars (incl. Best International Film)
- Filter by award source / year, keyword search
- Posters (Wikipedia + TMDb fallback), detail modal
- Favorites & watched markers (localStorage)
- Random draw mode

**Books**
- 8 literary prizes: Booker, Nobel, Pulitzer, International Booker, etc.
- Filter by prize / year, keyword search
- Chinese translation availability notes

## Tech

Vanilla HTML/CSS/JS, zero dependencies. Data fetched from Wikipedia REST API with incremental caching (1 API call per refresh).
