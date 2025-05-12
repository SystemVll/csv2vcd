import csv
import sys
import os
from datetime import datetime

def csv_to_vcd(csv_file, vcd_file, signal_names, timestep=1e-6, skip_header=False, 
               time_unit='us', signal_width=None, signal_type='wire', custom_ids=None):
    """
    Convert CSV data to VCD format with enhanced stability and features
    
    Args:
        csv_file: Input CSV file path
        vcd_file: Output VCD file path
        signal_names: List of signal names
        timestep: Time between samples in seconds
        skip_header: Whether to skip the first row of CSV
        time_unit: Time unit for VCD file ('s', 'ms', 'us', 'ns', 'ps', 'fs')
        signal_width: List of bit widths for each signal (defaults to 1 if None)
        signal_type: Type of signal ('wire', 'reg', etc.)
        custom_ids: Custom identifiers for signals (uses automatic if None)
    """
    num_signals = len(signal_names)
    values = []

    # Set default signal widths if not provided
    if signal_width is None:
        signal_width = [1] * num_signals
    elif len(signal_width) != num_signals:
        raise ValueError(f"Signal width list length ({len(signal_width)}) doesn't match signal names ({num_signals})")

    # Validate input files
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    try:
        # Read CSV data
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            
            # Skip header if requested
            if skip_header:
                next(reader, None)
                
            for row_num, row in enumerate(reader, start=1):
                if not row:  # Skip empty rows
                    continue
                    
                if len(row) != num_signals:
                    raise ValueError(f"Row {row_num} has {len(row)} values, expected {num_signals}")
                
                # Validate values before adding
                validated_row = []
                for i, val in enumerate(row):
                    val = val.strip()
                    # For 1-bit signals, ensure values are 0, 1, x, z, X, Z
                    if signal_width[i] == 1 and val not in ['0', '1', 'x', 'z', 'X', 'Z']:
                        print(f"Warning: Row {row_num}, Signal {signal_names[i]}: Invalid value '{val}' converted to 'x'")
                        val = 'x'
                    validated_row.append(val)
                
                values.append(validated_row)
                
        if not values:
            raise ValueError("No data found in CSV file")
            
        # Validate time unit
        valid_units = ['s', 'ms', 'us', 'ns', 'ps', 'fs']
        if time_unit not in valid_units:
            raise ValueError(f"Invalid time unit: {time_unit}. Must be one of {', '.join(valid_units)}")
            
        # Create IDs for signals
        ids = []
        if custom_ids and len(custom_ids) == num_signals:
            ids = custom_ids
        else:
            # Generate IDs using printable ASCII characters (33-126)
            for i in range(num_signals):
                if i < 94:  # Number of printable ASCII chars (127-33)
                    signal_id = chr(33 + i)
                else:
                    # For more than 94 signals, use multi-character IDs
                    signal_id = f"s{i}"
                ids.append(signal_id)
                
        # Start writing VCD
        with open(vcd_file, 'w') as f:
            f.write(f"$date\n    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n$end\n")
            f.write("$version\n    Enhanced csv_to_vcd v2.0\n$end\n")
            f.write(f"$timescale 1 {time_unit} $end\n")
            f.write("$scope module logic $end\n")

            # Write signal declarations
            for i, name in enumerate(signal_names):
                f.write(f"$var {signal_type} {signal_width[i]} {ids[i]} {name} $end\n")

            f.write("$upscope $end\n$enddefinitions $end\n")
            
            # Initial values
            f.write("$dumpvars\n")
            for i, sig_id in enumerate(ids):
                if signal_width[i] == 1:
                    f.write(f"{values[0][i]}{sig_id}\n")
                else:
                    f.write(f"b{values[0][i]} {sig_id}\n")
            f.write("$end\n")

            # Calculate time multiplier based on time_unit
            time_multipliers = {'s': 1, 'ms': 1e3, 'us': 1e6, 'ns': 1e9, 'ps': 1e12, 'fs': 1e15}
            time_mult = time_multipliers[time_unit]
            
            # Write time steps and changes
            prev_values = values[0]
            for t, row in enumerate(values):
                timestamp = int(t * timestep * time_mult)
                f.write(f"#{timestamp}\n")
                
                # Only write values that changed for efficiency
                for i, val in enumerate(row):
                    if val != prev_values[i]:
                        if signal_width[i] == 1:
                            f.write(f"{val}{ids[i]}\n")
                        else:
                            f.write(f"b{val} {ids[i]}\n")
                            
                prev_values = row
                
            print(f"Successfully converted {csv_file} to {vcd_file} with {num_signals} signals and {len(values)} timesteps")
            
    except Exception as e:
        print(f"Error converting CSV to VCD: {str(e)}", file=sys.stderr)
        raise


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert a CSV file to VCD format")
    parser.add_argument("csv_file", help="Input CSV file")
    parser.add_argument("vcd_file", help="Output VCD file")
    parser.add_argument("--timestep", type=float, default=1e-6, help="Time between samples in seconds (default: 1e-6)")
    parser.add_argument("--signal-names", nargs='+', required=True, help="List of signal names")
    parser.add_argument("--skip-header", action="store_true", help="Skip first row of CSV file (header)")
    parser.add_argument("--time-unit", default="us", choices=["s", "ms", "us", "ns", "ps", "fs"], 
                        help="Time unit for VCD file (default: us)")
    parser.add_argument("--signal-width", type=int, nargs='+', help="List of bit widths for each signal (default: 1)")
    parser.add_argument("--signal-type", default="wire", choices=["wire", "reg", "integer", "parameter"],
                        help="Type of signals (default: wire)")
    
    args = parser.parse_args()

    try:
        csv_to_vcd(args.csv_file, args.vcd_file, args.signal_names, args.timestep,
                  args.skip_header, args.time_unit, args.signal_width, args.signal_type)
    except Exception as e:
        sys.exit(1)  # Exit with error code