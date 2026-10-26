# Ticket Triage

A lightweight Python tool that automatically categorizes support tickets, assigns priority levels, and identifies potential SLA breaches from CSV data.

## Features

- Classifies tickets by category using keyword matching.
- Assigns priority levels to help teams decide what to handle first.
- Flags tickets that have breached their service-level agreement (SLA).
- Exports processed tickets to a CSV report.
- Includes demo mode for quick testing.
- Uses only the Python standard library.

## Requirements

- Python 3.8 or later

## Usage

Run the demo:

```bash
python ticket_triage.py --demo
```

The tool generates sample ticket data, processes the tickets, and creates `triaged.csv`.

## Output

- `triaged.csv` — classified tickets with assigned priorities and SLA status.

## How It Works

The tool analyzes ticket text using keyword-based rules, assigns a category and priority, and checks whether each ticket has breached its SLA.

This is a simple rule-based prototype. Its classifications depend on the keywords and rules defined in the code.

## Important Notes

- Demo mode may generate or overwrite sample data files.
- Test the tool with sample data before using real support tickets.
- Review classifications before relying on them for operational decisions.
- The tool does not connect to a live customer support platform.

## Future Improvements

- Add configurable classification rules.
- Improve handling of empty or malformed CSV files.
- Support customizable SLA thresholds.
- Add more detailed reporting and summary statistics.
- Integrate with customer support platforms.

## License

MIT
