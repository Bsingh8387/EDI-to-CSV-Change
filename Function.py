import csv  # CSV writer helpers
import os  # file system utilities
from datetime import datetime  # timestamp generation

       

def split_into_segment(raw_text, segment_terminator ="~"):
    """Split raw EDI text into a list of segments using the terminator and remove empties."""
    split_segement = raw_text.split(segment_terminator)  # split text at the segment terminator
    
    clean_segements = []  # hold only valid non-empty segments

    for seg in split_segement:
        seg = seg.strip()          # removes whitespace/newlines from both ends
        if seg != "":              # skip empty strings produced by split
            clean_segements.append(seg)   # add the cleaned segment to our list

    return clean_segements  # return filtered segments


def get_segment_ids(segments, filter_ids=None):
    """Collect segment IDs from a list of segment strings, optionally filtering by allowed IDs."""
    ids = []  # result list for matching IDs
    for seg in segments:
        elements = seg.split("*")  # split segments by the element separator
        seg_id = elements[0]  # first field is the segment identifier
        if filter_ids is None or seg_id in filter_ids:
            ids.append(seg_id)  # record IDs that pass the filter
    return ids


def segment_to_dict(seg, element_separator="*"):
    """Convert one EDI segment string into a dict with its ID and remaining elements."""
    parts = seg.split(element_separator)  # separate fields inside the segment
    return {
        "segment_id": parts[0],  # segment ID from the first field
        "elements": parts[1:]     # remaining fields become element values
    }

def parse_segments(segments, element_separator="*"):
    """Parse a list of segment strings into structured dict objects for each segment."""
    parsed = []  # list for parsed segment dicts
    for seg in segments:
        parsed.append(segment_to_dict(seg, element_separator))  # parse each segment string
    return parsed


def find_segments(parsed, segment_id):
    """Return all parsed segments that match the requested segment ID."""
    matches = []  # collect matching segment dicts
    for p in parsed:
        if p["segment_id"] == segment_id:
            matches.append(p)  # append matches
    return matches



