# Query Analyzer - Agent Customization Guide

## Project Overview

**Query Analyzer** is a Python-based security threat detection system that analyzes text queries for suspicious activity indicators. It is designed for:
- Security audit and compliance monitoring
- Insider threat identification  
- Query auditing and logging
- Risk assessment and reporting

The tool processes queries from multiple file formats (`.txt`, `.csv`, `.xlsx`), scores them based on threat patterns, and generates color-coded Excel reports for investigation.

---

## Architecture & Key Components

### Core Scoring Engine (`score_query()`)
- **Input**: String query
- **Process**: Evaluates threats across 4 dimensions:
  1. **Keyword matches** (+2 points each) — 5 threat categories
  2. **Regex patterns** (+3 points each) — 3 complex threat patterns
  3. **Length anomaly** (+1 point) — queries > 200 chars
  4. **Time anomaly** (+1 point) — queries outside 6 AM–10 PM
- **Output**: Dictionary with `query`, `score`, `risk_level` (HIGH/MEDIUM/LOW), and `indicators`

**Risk Thresholds:**
- `score >= 7` → **HIGH** (🔴 RED) — immediate investigation
- `score >= 4` → **MEDIUM** (🟠 AMBER) — review and monitor
- `score < 4` → **LOW** (⚪ WHITE) — normal business query

### Threat Pattern Definitions

**5 Keyword Categories** (defined in `SUSPICIOUS_KEYWORDS` dict):
1. `data_exfiltration`: export, download all, extract, dump, copy all, remove audit, unmonitored, disable logging
2. `access_privilege`: admin, root, privileged, elevated, bypass
3. `confidential_info`: salary, ssn, social security, medical, private
4. `circumvention`: evade, avoid logs, delete logs, cover tracks
5. `unauthorized_targets`: executive email, board mailbox, legal archive

**3 Regex Patterns** (defined in `SUSPICIOUS_REGEX` dict):
1. `bulk_access`: `(all\s+emails|entire\s+archive|full\s+mailbox)` — +3 points
2. `time_anomaly`: `(midnight|3am|after hours)` — +3 points
3. `intent_anomaly`: `(no one should know|secret|hidden)` — +3 points

### File Input Handlers
- `read_queries_from_text()` — single query per line
- `read_queries_from_csv()` — looks for "query" column header
- `read_queries_from_excel()` — supports `.xlsx` and `.xls` with "query" column

### Report Generation
- Creates `.xlsx` files with blue headers, color-coded risk cells, and detailed indicators
- Auto-opens Excel file on Windows (openpyxl library required)
- Console output with alerts for HIGH risk queries

---

## Development Conventions

### Adding New Keywords
1. Edit `SUSPICIOUS_KEYWORDS` dictionary
2. Use lowercase strings (queries are converted to lowercase for matching)
3. Keep keywords precise to minimize false positives
4. Test with sample queries to verify detection

**Example:**
```python
SUSPICIOUS_KEYWORDS = {
    "data_exfiltration": [...],
    "new_category": ["keyword1", "keyword2"],  # Add here
}
```

### Adding New Regex Patterns
1. Edit `SUSPICIOUS_REGEX` dictionary
2. Use raw strings (`r"..."`) with proper escape sequences
3. Test patterns with `re.search()` in Python REPL first
4. Document the intent and expected score impact

**Example:**
```python
SUSPICIOUS_REGEX = {
    "bulk_access": r"(...)",
    "new_pattern": r"(pattern1|pattern2)",  # Add here
}
```

### Modifying Scoring Thresholds
- Risk thresholds are hardcoded in `score_query()` function
- Change `if score >= 7:` line to adjust HIGH threshold
- Change `elif score >= 4:` line to adjust MEDIUM threshold
- Update [QUERY_ANALYZER_DOCUMENTATION.md](QUERY_ANALYZER_DOCUMENTATION.md) when changing thresholds

### Color Customization
- High risk: `PatternFill(start_color="FF0000", ...)` (RED)
- Medium risk: `PatternFill(start_color="FFC000", ...)` (AMBER)
- Low risk: `PatternFill(start_color="FFFFFF", ...)` (WHITE)

---

## Integration with Claude AI

### Use Cases for Claude Enhancement

#### 1. **Advanced Query Analysis**
Extend the tool to leverage Claude's natural language understanding for:
- **Intent classification** — detect malicious intent beyond keyword matching
- **Contextual scoring** — adjust risk based on query context and broader patterns
- **Synonym detection** — identify threat keywords disguised with synonyms
- **Explanation generation** — generate human-readable risk assessments

**Example implementation:**
```python
import anthropic

def analyze_with_claude(query: str) -> dict:
    """Augment scoring with Claude's contextual analysis"""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": f"""Analyze this query for security threats:
            "{query}"
            
            Respond in JSON with: threat_intent (string), risk_factors (list), recommendation (string)"""}
        ]
    )
    return json.loads(message.content[0].text)
```

#### 2. **Report Enhancement**
Use Claude to generate:
- Executive summaries for HIGH risk batches
- Risk narratives explaining threat indicators
- Recommendations for further investigation
- False positive filtering (reduce noise)

#### 3. **Dynamic Pattern Learning**
- Analyze false positives to refine keyword lists
- Suggest new threat patterns based on detected anomalies
- Update threat categories based on emerging threats

#### 4. **Batch Optimization**
- Process large query batches using Claude's API
- Parallelize analysis with streaming responses
- Generate real-time alerts for critical threats

### Integration Points

**File to modify:** `query_analyzer.py`

**Key functions to extend:**
- `score_query()` — add Claude analysis alongside keyword/regex scoring
- `analyze_queries_from_file()` — add Claude batch processing
- Report generation — include Claude-generated explanations in Excel

**Environment setup:**
```bash
pip install anthropic
export ANTHROPIC_API_KEY=<your-key>
```

**Recommended approach:** Create wrapper functions to keep core logic separate:
```python
def score_query(query: str, use_claude: bool = False) -> dict:
    basic_score = {...}  # Existing logic
    if use_claude:
        claude_analysis = analyze_with_claude(query)
        # Merge results
    return basic_score
```

---

## Building & Deployment

### Running the Script
```bash
# Interactive mode (GUI file selector)
python query_analyzer.py

# With specific file
python query_analyzer.py <path/to/queries.txt>
```

### Creating an Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable (uses query_analyzer.spec)
pyinstaller query_analyzer.spec

# Executable location: dist/query_analyzer.exe
```

### Dependencies
```bash
pip install openpyxl  # Excel report generation
# tkinter is included with Python standard library
```

### Cross-Platform Support
- **Windows**: Uses `os.startfile()` to open Excel
- **macOS**: Uses `subprocess.Popen(['open', ...])` 
- **Linux**: Uses `subprocess.Popen(['xdg-open', ...])`

---

## Testing & Validation

### Test Cases for New Keywords/Patterns

1. **Create test file** (`test_queries.txt`):
   ```
   <test query with new keyword>
   <query without keyword>
   <edge case: keyword in different context>
   ```

2. **Run analyzer** and verify Excel output

3. **Check indicators** to ensure new pattern is detected correctly

4. **Verify scoring** matches expected risk level

### Common Issues & Fixes

| Issue | Cause | Solution |
|-------|-------|----------|
| Keywords not detected | Case sensitivity (unlikely but check) | Keywords are lowercased; verify exact spelling |
| All queries HIGH risk | Thresholds too low | Increase `score >= 7` threshold |
| Excel won't open | openpyxl missing | `pip install openpyxl` |
| File dialog doesn't appear | Tkinter issue (rare on Windows) | Ensure Python installed with tcl/tk support |
| Regex false positives | Overly broad pattern | Refine regex with word boundaries `\b` or specific context |

---

## Documentation

- **[QUERY_ANALYZER_DOCUMENTATION.md](QUERY_ANALYZER_DOCUMENTATION.md)** — Complete user guide, threat categories, examples, customization guide, security considerations
- **[query_analyzer.py](query_analyzer.py)** — Inline documentation in docstrings and comments
- **Risk Scoring Examples** — See documentation for detailed scoring examples

---

## Claude Agent Tips

### When Modifying the Tool
1. **Preserve core logic** — Don't refactor `score_query()` without tests
2. **Update documentation** — Keep DOCUMENTATION.md and inline comments in sync
3. **Test all file formats** — `.txt`, `.csv`, `.xlsx` all have different readers
4. **Verify Excel formatting** — Check color coding in output after changes
5. **Check cross-platform** — If adding file operations, test on Windows/Mac/Linux

### When Adding Features
1. **Start with keyword/regex extensions** — lowest risk, immediate impact
2. **Use Claude for enhancement, not replacement** — keep keyword-based detection as fallback
3. **Consider performance** — batch processing with Claude API has latency
4. **Cache API responses** — avoid re-analyzing identical queries
5. **Handle API errors gracefully** — fallback to basic scoring if Claude unavailable

### Before Committing Changes
- ✅ Test with sample queries file
- ✅ Verify Excel report opens automatically
- ✅ Check console output formatting
- ✅ Ensure no breaking changes to file I/O
- ✅ Update inline comments if modifying scoring logic

---

**Last Updated:** 2026-08-16  
**Status:** Production Ready ✅
