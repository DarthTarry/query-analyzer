# Query Analyzer

A Python-based security threat detection utility that analyzes text queries for suspicious activity indicators and generates a color-coded Excel report.

## Features

- Threat keyword detection across multiple categories
- Regex-based pattern matching for suspicious intent
- Risk scoring and classification
- Excel report generation with highlighted risk levels
- Batch processing for query files

## Requirements

```bash
pip install openpyxl
```

## Usage

```bash
python query_analyzer.py
```

Then select a `.txt`, `.csv`, or `.xlsx` file containing queries.

## Risk levels

- `HIGH` : score >= 7
- `MEDIUM` : score >= 4
- `LOW` : score < 4

## License

MIT
