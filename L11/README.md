# SHA-256 Hash Performance Analyzer

This application implements the SHA-256 hashing algorithm and provides tools to analyze its performance. It features a graphical user interface built with Electron and allows users to:

1. Hash input text using SHA-256
2. Measure performance across multiple iterations
3. Export performance results to Excel

## Features

- SHA-256 hashing implementation
- Performance measurement tools
- Excel export functionality
- Modern and user-friendly interface

## Installation

1. Make sure you have Node.js installed on your system
2. Clone this repository
3. Install dependencies:
```bash
npm install
```

## Usage

1. Start the application:
```bash
npm start
```

2. Enter text in the input field
3. Click "Hash Input" to generate a hash
4. Use the Performance Test section to:
   - Set the number of iterations
   - Run performance tests
   - View results in the table
   - Export results to Excel

## Performance Analysis

The application measures:
- Hash generation time
- Input length impact on performance
- Average execution time across multiple iterations

Results are displayed in a table and can be exported to Excel for further analysis.

## Technical Details

- Built with Node.js and Electron
- Uses the native crypto module for SHA-256 implementation
- Excel export functionality using ExcelJS
- Performance measurements using high-resolution timers 