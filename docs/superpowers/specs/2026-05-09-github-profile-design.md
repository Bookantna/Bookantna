# GitHub Profile README Design

**Target:** `Bookantna` GitHub profile (`github.com/Bookantna`)
**Output:** Single `README.md` in the `Bookantna/Bookantna` special repository
**Style:** Energetic & bold — badges, stats widgets, animated header

---

## Structure

### 1. Header
- H1 name: `Thanawat Ueasiripracha`
- Animated typing SVG via `readme-typing-svg` (DenverCoder9):
  - Lines: `"Aspiring Data Engineer"`, `"CS Student @ Khon Kaen University"`, `"Manufacturing Intern @ Seagate"`
- One-liner tagline below: Python · SQL · ML · Deep Learning

### 2. Skills Badges
Shields.io badges grouped into rows by category:

| Category | Technologies |
|---|---|
| Languages | Python, SQL, C/C++, Java |
| ML / Data | TensorFlow, PyTorch, scikit-learn, Pandas, NumPy |
| Tools | Git, Docker, Jupyter, VS Code, Spring Framework |
| Databases | PostgreSQL, MySQL |

### 3. GitHub Stats Row
Three cards displayed side-by-side using HTML `<img>` tags in a table:
- `github-readme-stats` — Stars, commits, PRs, issues (theme: `tokyonight`)
- `github-readme-streak-stats` — Current streak / longest streak
- `github-readme-stats` top languages card

Username: `Bookantna`

### 4. Projects Showcase
Markdown table with 4 pinned projects:

| | Project | Description | Stack |
|---|---|---|---|
| 🖥️ | [Screenie](https://github.com/Bookantna/Screenie) | Fast macOS screenshot & annotation tool — menu bar, OCR, color picker, pixel ruler | Swift 6 |
| 🌸 | [Flower-Image-Colorization](https://github.com/Bookantna/Flower-Image-Colorization) | Deep learning model to colorize grayscale flower images | Python, PyTorch |
| 🎫 | [ticketDorm](https://github.com/Bookantna/ticketDorm) | Web-based dorm maintenance request system built with SOLID principles | Java, Spring Boot, JPA |
| ⚡ | [Multiprocessing](https://github.com/Bookantna/Multiprocessing) | Parallel image processing using Python multiprocessing | Python |

### 5. Footer
Centered badge row:
- LinkedIn: `https://www.linkedin.com/in/thanawatueasiripracha/`
- Email: `thanawatueasiripracha@gmail.com`
- GitHub: `Bookantna`

---

## External Services Used
- `readme-typing-svg` — `readme-typing-svg.demolab.com`
- `github-readme-stats` — `github-readme-stats.vercel.app`
- `github-readme-streak-stats` — `streak-stats.demolab.com`
- `shields.io` — badge generation

## Constraints
- Pure Markdown + HTML img tags (no JavaScript)
- All widgets load from public CDN-like services — no auth required
- Email displayed publicly per user confirmation
