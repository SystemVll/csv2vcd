# CSV to VCD Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust Python utility that converts CSV (Comma-Separated Values) files to VCD (Value Change Dump) format for digital waveform visualization in hardware design and verification workflows.

## Description

This tool bridges the gap between simple tabular data and industry-standard waveform viewers by transforming CSV data into VCD files. It's particularly useful for hardware engineers, FPGA developers, and digital circuit designers who need to visualize signal changes over time.

## Features

- Convert multi-signal CSV data to standard VCD format
- Configurable time units (s, ms, us, ns, ps, fs) and timesteps
- Support for various signal types (wire, reg, integer, parameter)
- Customizable signal widths (single-bit or multi-bit)
- Input validation and robust error handling
- Header row skipping option
- Automatic or custom signal identifiers

## Installation

```bash
git clone https://github.com/SystemVll/csv2vcd.git
cd csv2vcd
```

No additional dependencies required beyond Python's standard library.

## Usage

### Basic Usage

```bash
python main.py input.csv output.vcd --signal-names signal1 signal2 signal3
```

### Advanced Usage

```bash
python main.py input.csv output.vcd \
  --signal-names clock data valid \
  --timestep 1e-9 \
  --time-unit ns \
  --signal-width 1 8 1 \
  --signal-type wire \
  --skip-header
```

## Arguments

| Argument | Description |
|----------|-------------|
| `csv_file` | Input CSV file path |
| `vcd_file` | Output VCD file path |
| `--signal-names` | List of signal names |
| `--timestep` | Time between samples in seconds (default: 1e-6) |
| `--skip-header` | Skip first row of CSV file (header) |
| `--time-unit` | Time unit for VCD file: s, ms, us, ns, ps, fs (default: us) |
| `--signal-width` | List of bit widths for each signal (default: 1) |
| `--signal-type` | Type of signals: wire, reg, integer, parameter (default: wire) |

## Example

**Input CSV:**
```
0,01101100,1
1,01101101,1
0,01101101,0
...
```

**Command:**
```bash
python main.py signals.csv output.vcd --signal-names clk data valid --signal-width 1 8 1
```

**Output:**
A VCD file compatible with waveform viewers like GTKWave, ModelSim, etc.

## License

This project is licensed under the MIT License - see the LICENSE file for details.