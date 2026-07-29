# arXiv Submission Guide

## Paper Information
- **Title**: Fractal Gravity Paradigm: A Unified Framework from Spacetime Substrate to Cross-Scale Coupling
- **File**: `paper_en.tex` (1614 lines, fully English, pdflatex compatible)
- **No dependencies**: No ctex, no XeLaTeX, no external figures required

## Recommended arXiv Category
- **Primary**: `gr-qc` (General Relativity and Quantum Cosmology)
- **Cross-list**: `hep-ph` (High Energy Physics - Phenomenology)
- **Alternative**: `physics.gen-ph` (General Physics)

## Step 1: Register arXiv Account
1. Go to https://arxiv.org/user/register
2. Use your institutional email or ORCID
3. Fill in your name and affiliation
4. Wait for email verification (usually instant)

## Step 2: Obtain Endorsement (First-time submitters only)
arXiv requires endorsement for first-time submissions in a category.
1. After login, go to https://arxiv.org/authorize/endorsement
2. Request endorsement for `gr-qc`
3. You need an existing arXiv author in `gr-qc` to endorse you
4. If you don't know anyone, try:
   - Contacting authors of related papers
   - Posting on physics forums
   - Using the arXiv endorsement request system

## Step 3: Submit
1. Go to https://arxiv.org/submit
2. Select category: `gr-qc`
3. Upload `paper_en.tex`
4. Add metadata:
   - Title: Fractal Gravity Paradigm: A Unified Framework from Spacetime Substrate to Cross-Scale Coupling
   - Abstract: (copy from the paper)
   - Authors: Your name
   - Comments: 20 sections + 9 appendices, reproducible code at https://github.com/binliu-lab/fractal-gravity-paradigm
5. arXiv compiles the paper and shows a PDF preview
6. Review the preview
7. Click "Submit" to publish

## Notes
- arXiv typically takes 24-48 hours to process new submissions
- The paper uses standard `article` class with `amsmath`, `amsthm`, `physics`, etc. — all available on arXiv's TeX Live
- No `\tableofcontents` (removed for arXiv compatibility)
- No `ctex` or XeLaTeX dependency
- Bibliography is inline (`thebibliography` environment, no .bbl needed)
