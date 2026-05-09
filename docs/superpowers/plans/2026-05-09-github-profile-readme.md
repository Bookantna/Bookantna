# GitHub Profile README Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a professional, energetic GitHub profile README for `Bookantna` with animated header, skill badges, GitHub stats widgets, and project showcase.

**Architecture:** Single `README.md` in the `Bookantna/Bookantna` special repository. Pure Markdown + HTML img tags — no JavaScript. All widgets served from public CDN-like services (readme-typing-svg, github-readme-stats, streak-stats, shields.io).

**Tech Stack:** Markdown, HTML img/div tags, shields.io, readme-typing-svg, github-readme-stats, streak-stats.demolab.com

---

## File Structure

- Create: `README.md` — the entire GitHub profile page

---

### Task 1: Initialize repo and create skeleton

**Files:**
- Create: `README.md`

- [ ] **Step 1: Initialize git repo**

```bash
git init
git branch -M main
```

- [ ] **Step 2: Create README.md skeleton with section placeholders**

```markdown
<!-- HEADER -->

---

<!-- SKILLS -->

---

<!-- STATS -->

---

<!-- PROJECTS -->

---

<!-- FOOTER -->
```

- [ ] **Step 3: Initial commit**

```bash
git add README.md
git commit -m "chore: init github profile readme skeleton"
```

---

### Task 2: Add animated header section

**Files:**
- Modify: `README.md` — replace `<!-- HEADER -->` block

- [ ] **Step 1: Replace header placeholder with animated header**

Replace `<!-- HEADER -->` with:

```markdown
<div align="center">

# 👋 Hi, I'm Thanawat Ueasiripracha

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=58A6FF&center=true&vCenter=true&width=500&lines=Aspiring+Data+Engineer;CS+Student+%40+Khon+Kaen+University;Manufacturing+Intern+%40+Seagate" alt="Typing SVG" />

<p>Python · SQL · ML · Deep Learning</p>

</div>
```

- [ ] **Step 2: Verify render**

Open `README.md` in GitHub or a Markdown previewer. Confirm:
- H1 name displays
- Typing SVG image loads (blue text, Fira Code font)
- Tagline shows below

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: add animated header with typing SVG"
```

---

### Task 3: Add skills badges section

**Files:**
- Modify: `README.md` — replace `<!-- SKILLS -->` block

- [ ] **Step 1: Replace skills placeholder with badge grid**

Replace `<!-- SKILLS -->` with:

```markdown
## 🛠️ Tech Stack

**Languages:**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)
![C/C++](https://img.shields.io/badge/C%2FC%2B%2B-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)

**ML / Data:**

![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

**Tools:**

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Spring](https://img.shields.io/badge/Spring-6DB33F?style=for-the-badge&logo=spring&logoColor=white)

**Databases:**

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
```

- [ ] **Step 2: Verify render**

Preview README. Confirm all 4 badge groups appear with correct colors and logos.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: add skills badges section"
```

---

### Task 4: Add GitHub stats row

**Files:**
- Modify: `README.md` — replace `<!-- STATS -->` block

- [ ] **Step 1: Replace stats placeholder with three-card row**

Replace `<!-- STATS -->` with:

```markdown
## 📊 GitHub Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=Bookantna&show_icons=true&theme=tokyonight&hide_border=true" height="165" alt="GitHub Stats" />
<img src="https://streak-stats.demolab.com?user=Bookantna&theme=tokyonight&hide_border=true" height="165" alt="GitHub Streak" />
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Bookantna&layout=compact&theme=tokyonight&hide_border=true" height="165" alt="Top Languages" />

</div>
```

- [ ] **Step 2: Verify render**

Preview README. Confirm:
- Three stat cards display side-by-side (may wrap on narrow screens — acceptable)
- All three load without broken image icons
- Theme is `tokyonight` (dark blue/purple)

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: add github stats, streak, and top languages cards"
```

---

### Task 5: Add projects showcase table

**Files:**
- Modify: `README.md` — replace `<!-- PROJECTS -->` block

- [ ] **Step 1: Replace projects placeholder with showcase table**

Replace `<!-- PROJECTS -->` with:

```markdown
## 🚀 Featured Projects

| | Project | Description | Stack |
|:---:|---|---|---|
| 🖥️ | [Screenie](https://github.com/Bookantna/Screenie) | Fast macOS screenshot & annotation tool — menu bar app with OCR, color picker, and pixel ruler | Swift 6 |
| 🌸 | [Flower-Image-Colorization](https://github.com/Bookantna/Flower-Image-Colorization) | Deep learning model to colorize grayscale flower images | Python, PyTorch |
| 🎫 | [ticketDorm](https://github.com/Bookantna/ticketDorm) | Web-based dorm maintenance request system built with SOLID principles | Java, Spring Boot |
| ⚡ | [Multiprocessing](https://github.com/Bookantna/Multiprocessing) | Parallel image processing pipeline using Python multiprocessing | Python |
```

- [ ] **Step 2: Verify render**

Preview README. Confirm:
- Table renders with 4 rows
- All project links are clickable
- Emojis show in first column

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "feat: add featured projects showcase table"
```

---

### Task 6: Add footer with contact links

**Files:**
- Modify: `README.md` — replace `<!-- FOOTER -->` block

- [ ] **Step 1: Replace footer placeholder with contact badges**

Replace `<!-- FOOTER -->` with:

```markdown
## 📬 Connect With Me

<div align="center">

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/thanawatueasiripracha/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:thanawatueasiripracha@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Bookantna)

</div>
```

- [ ] **Step 2: Verify render**

Preview README. Confirm:
- Three badges display centered
- LinkedIn badge links to `https://www.linkedin.com/in/thanawatueasiripracha/`
- Email badge opens `mailto:thanawatueasiripracha@gmail.com`
- GitHub badge links to `https://github.com/Bookantna`

- [ ] **Step 3: Final full-page visual check**

Read through the complete README top to bottom. Verify:
- Header → Skills → Stats → Projects → Footer flows cleanly
- No placeholder comments (`<!-- ... -->`) remain
- No broken image URLs

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: add footer contact badges — profile readme complete"
```

---

### Task 7: Push to GitHub

- [ ] **Step 1: Create `Bookantna/Bookantna` repo on GitHub if not exists**

Go to `https://github.com/new`, set repository name to `Bookantna` (must match username exactly). Set to Public. Do NOT initialize with README.

- [ ] **Step 2: Add remote and push**

```bash
git remote add origin https://github.com/Bookantna/Bookantna.git
git push -u origin main
```

- [ ] **Step 3: Verify profile**

Visit `https://github.com/Bookantna`. Confirm the README renders on the profile page with all sections visible.
