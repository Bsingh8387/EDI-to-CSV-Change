import csv  # CSV writer helpers
import os  # file system utilities
from datetime import datetime  # timestamp generation
from Function import split_into_segment, parse_segments

def read_edi_file(file_name):
    """Read EDI file from the system"""
    with open(file_name, "r", encoding="utf-8") as f:
        return f.read()  # read all text from the EDI file


def validate_edi(validate):
    """Inspect the first segment of the EDI text and print the element separator type."""
    element_separator = validate[3]  # element separator is defined by the 4th character in the ISA segment

    if element_separator == "" or element_separator.isspace():
        print("Element Seprator Looks Invalide.")  # missing or whitespace separator
    elif element_separator == "*":
        print("Standard element separator detected (*).")
    elif element_separator == "|":
        print("Pipe separator detected (|)")
    elif element_separator == "^":
        print("Caret separator detected (^)")
    else:
        print(f"Non-standard element separator detected: {element_separator!r}")


def make_unique_csv_path(base_name="my_first_edi_output", extension=".csv", output_dir=r"d:\Project\ED to CSV\output"):
    """Create a timestamped file path inside the target output folder."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"{base_name}_{timestamp}{extension}")

def write_csv(parsed, output_path):
    """Write parsed segment data into a CSV file with one row per element value."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)  # create CSV writer
        writer.writerow(["segment_id", "element_position", "value"])  # header row

        for p in parsed:
            for i, value in enumerate(p["elements"], start=1):
                writer.writerow([p["segment_id"], i, value])  # write each element row

raw = read_edi_file(r"d:\Project\ED to CSV\sample_837.edi")

validate_edi(raw)

segement = split_into_segment(raw)
parsed = parse_segments(segement)

output_path = make_unique_csv_path()
write_csv(parsed, output_path)
print(f"Done — check {output_path}")
