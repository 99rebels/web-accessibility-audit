# Report Styling Reference

Full example output for a client report and freelancer notes. Use this as the canonical style guide.

See [example-client-report.md](example-client-report.md) for the Walmart example.
See [example-freelancer-notes.md](example-freelancer-notes.md) for the matching internal notes.

## Key Style Rules

### Client Report
- Prefix: `♿ **Client Report**`
- Finding titles in **UPPERCASE**
- `●` bullets throughout (not `•` or `-`)
- Code blocks: `HTML` language tag, line numbers, `<!-- Before -->` / `<!-- After -->` labels
- No `Impact:` field — fold impact reasoning into `Detail:`
- No `Pages` column in compliance checklist
- Bold effort estimates: `— **Estimated effort: X hours**`
- Roadmap priority headers are **bold**, not `###`
- Narrative executive summary (prose paragraphs, not bullets)
- `---` dividers between major sections

### Freelancer Notes
- Prefix: `🔧 **Freelancer Notes — Internal**`
- Same `●` bullet style
- Section headers in **bold** (not markdown headers) for subsections
- Include `Severity Adjustments` section if any severities were changed
- Include `Consolidated Findings` section if duplicates were merged
- Include `False Positive Notes` with reasoning

### Anti-Hallucination
- Every finding must come from the script's JSON output
- Score and grade must match the script exactly
- Legal statistics must use only the numbers in the SKILL.md reference section
- Never fabricate elements, URLs, or page counts
- Never add findings the script didn't detect
- Never inflate severity to make the report seem more urgent
- Fix code must address the actual reported element, not generic examples
- When unsure, include the finding and flag in freelancer notes
