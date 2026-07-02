# 🎓 The NITC Wiki

Welcome to the ultimate, open-source survival guide and knowledge base for the **National Institute of Technology Calicut**. 

Navigating a campus of this scale shouldn't require relying on scattered PDFs, outdated WhatsApp forwards, or word-of-mouth. This platform was engineered to be the single, centralized source of truth for the NITC community. 

🌐 **Live Site:** [Insert your Netlify/GitHub Pages link here]

## ✨ Features
* **Comprehensive Coverage:** 90+ meticulously categorized pages covering Academics, Hostels, Student Life, Dining, and Campus Infrastructure.
* **Lightning Fast Search:** Instantly find specific rules, syllabi, or locations with the built-in predictive search engine.
* **Data Visualizations:** Complex processes (like grading systems or registration flows) are mapped out using embedded Mermaid.js diagrams.
* **Dark/Light Mode:** Seamless toggle for late-night studying.
* **Community Driven:** Built by students, for students. Anyone can contribute to keeping the wiki accurate.

## 🤝 How to Contribute (For Students)
Spotted an outdated syllabus, a closed restaurant, or a typo? You don't need to be a programmer to fix it.

1. Navigate to the page you want to update on the live website.
2. Click the **✏️ Edit this page** icon in the top right corner.
3. GitHub will automatically create a fork of this repository for you.
4. Make your text edits directly in the browser.
5. Scroll down and click **Propose Changes**, then **Create Pull Request**.
6. The maintainers will review your fix and merge it to the live site!

## 💻 Local Development (For Developers)
Want to build new features or test major structural changes locally? The wiki is built on Python using the lightning-fast [MkDocs](https://www.mkdocs.org/) framework with the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

### Prerequisites
* Python 3.x installed
* Git installed

### Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/nitc-wiki.git](https://github.com/YOUR_USERNAME/nitc-wiki.git)
   cd nitc-wiki
   ```

2. **Install the dependencies:**
   ```bash
   pip install mkdocs mkdocs-material
   ```

3. **Start the local server:**
   ```bash
   mkdocs serve
   ```
   *The site will now be running live at `http://127.0.0.1:8000`.*

4. **Build for production:**
   To generate the static HTML files into a `site/` folder for deployment:
   ```bash
   mkdocs build
   ```

## 📜 License & Disclaimer
This is an independent, student-led open-source initiative and is not officially affiliated with the administration of the National Institute of Technology Calicut. 

---
*Built with coffee and MkDocs by Jake John George (B250263CS) & the NITC Community.*
