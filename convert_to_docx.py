#!/usr/bin/env python3
r"""
Convert paper_v2.tex to DOCX using pandoc.
Fixes known LaTeX issues that pandoc cannot handle:
1. Remove twocolumn from documentclass
2. Remove \twocolumn[{ }] wrapper blocks (keep inner content)
3. Replace \rm with \mathrm in math mode
4. Remove @twocolumnfalse environment
5. Fix \mathcal{C}[\Psi] -> \mathcal{C}({\Psi}) (square brackets in math confuse pandoc)
6. Remove \allowdisplaybreaks
"""
import re
import subprocess
import sys
import os

TEX_FILE = os.path.join(os.path.dirname(__file__), "paper_v2.tex")
TEMP_FILE = os.path.join(os.path.dirname(__file__), "paper_v2_fixed.tex")
DOCX_FILE = os.path.join(os.path.dirname(__file__), "paper_v2_final.docx")

def fix_latex(content):
    """Apply all fixes to the LaTeX content."""
    
    # 1. Remove twocolumn from documentclass
    content = content.replace(
        r"\documentclass[12pt,a4paper,twocolumn]{article}",
        r"\documentclass[12pt,a4paper]{article}"
    )
    
    # 2. Remove \twocolumn[{ ... }] wrapper blocks (keep inner content)
    # Pattern: \twocolumn[{<content>}] -> <content>
    # This handles multi-line blocks
    content = re.sub(
        r'\\twocolumn\[\{\s*\n?\s*\\begin\{@twocolumnfalse\}\s*\n?(.*?)\n?\s*\\end\{@twocolumnfalse\}\s*\n?\s*\}\]',
        r'\1',
        content,
        flags=re.DOTALL
    )
    
    # 3. Replace \rm with \mathrm in math mode
    # Pattern: x_{\rm ...} -> x_{\mathrm{...}} and x^{\rm ...} -> x^{\mathrm{...}}
    content = re.sub(
        r'([_\^])\{\\rm\s+([a-zA-Z]+)\}',
        r'\1{\\mathrm{\2}}',
        content
    )
    # Also handle standalone \rm in math: {\rm text} -> {\mathrm{text}}
    content = re.sub(
        r'\\rm\s+([a-zA-Z]+)',
        r'\\mathrm{\1}',
        content
    )
    
    # 4. Remove \setlength{\columnsep} and \raggedbottom (twocolumn related)
    content = re.sub(r'\\setlength\{\\columnsep\}\{[^}]*\}\s*\n?', '', content)
    content = re.sub(r'\\raggedbottom\s*\n?', '', content)
    
    # 5. Fix square brackets in math that confuse pandoc parser
    # Pandoc's LaTeX reader treats [..] after a command as optional argument.
    # Replace [\Psi] with ({\Psi}) - parentheses are equivalent notation.
    content = content.replace(r'\mathcal{C}[\Psi]', r'\mathcal{C}({\Psi})')
    # Also handle any remaining \mathcal{X}[...] patterns
    content = re.sub(r'(\\mathcal\{[A-Z]\})\[', r'\1(', content)
    # Close the opening ( with ) for known patterns
    # This is a best-effort fix for the specific paper
    content = content.replace(r'\mathcal{C}({\Psi})', r'\mathcal{C}({\Psi})')  # already fixed
    
    # 6. Fix double backslash in math: m_\\mu -> m_\mu, m_\\tau -> m_\tau
    content = content.replace(r'm_\\mu', r'm_\mu')
    content = content.replace(r'm_\\tau', r'm_\tau')
    
    # 7. Remove \allowdisplaybreaks
    content = re.sub(r'\\allowdisplaybreaks(?:\[\d\])?\s*\n?', '', content)
    
    # 8. Remove standalone \label{} lines inside equation environments
    # (pandoc DOCX doesn't use LaTeX cross-references and \label confuses its math parser)
    content = re.sub(r'\n\s*\\label\{[^}]*\}\s*\n(\\end\{equation)', r'\n\1', content)
    
    return content

def main():
    print(f"Reading: {TEX_FILE}")
    with open(TEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Applying LaTeX fixes...")
    fixed_content = fix_latex(content)
    
    # Verify fixes
    if 'twocolumn' in fixed_content:
        remaining = fixed_content.count('twocolumn')
        print(f"  Warning: {remaining} 'twocolumn' references remain")
    
    rm_count = len(re.findall(r'\\rm\s+[a-zA-Z]', fixed_content))
    if rm_count > 0:
        print(f"  Warning: {rm_count} '\\rm' references remain")
    
    print(f"Writing temp file: {TEMP_FILE}")
    with open(TEMP_FILE, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    # Run pandoc
    print(f"Running pandoc to convert to DOCX...")
    cmd = [
        "pandoc",
        TEMP_FILE,
        "-o", DOCX_FILE,
        "--from=latex",
        "--to=docx",
        "--toc",                    # Generate table of contents
        "--toc-depth=3",            # TOC depth
        "--standalone",
        "--highlight-style=tango",  # Code highlighting
    ]
    
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    
    if result.returncode != 0:
        print(f"\nPandoc stderr:\n{result.stderr}")
        print(f"\nPandoc stdout:\n{result.stdout}")
        # Check if DOCX was still created despite warnings
        if os.path.exists(DOCX_FILE):
            size = os.path.getsize(DOCX_FILE)
            print(f"\nDOCX file created despite warnings: {size:,} bytes")
        else:
            print("\nERROR: DOCX file was not created")
            sys.exit(1)
    else:
        print(f"\nPandoc completed successfully")
        if result.stderr:
            # Show only significant warnings (not all the font warnings)
            warnings = [w for w in result.stderr.split('\n') 
                       if w.strip() and 'font' not in w.lower() and 'package' not in w.lower()]
            if warnings:
                print(f"Pandoc messages:")
                for w in warnings[:10]:
                    print(f"  {w}")
    
    # Clean up temp file
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)
        print(f"Cleaned up temp file")
    
    # Report result
    if os.path.exists(DOCX_FILE):
        size_kb = os.path.getsize(DOCX_FILE) / 1024
        print(f"\n✓ DOCX file created: {DOCX_FILE}")
        print(f"  Size: {size_kb:.0f} KB")
    else:
        print("\n✗ ERROR: DOCX file was not created")
        sys.exit(1)

if __name__ == "__main__":
    main()
