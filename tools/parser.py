import re
import json

# Matches “rl … [label X]” or “ceq … [label Y]” at the start of a line
_LABEL_RE = re.compile(
    r'^(?P<kind>eq|crl|rl|ceq)\b.*?\[label\s+(?P<label>[^\]]+)\]',
    re.MULTILINE
)

def parse_labels(spec: str) -> dict:
    """
    Parse a Maude specification fragment and return a dictionary
    of rule and equation labels.

    Parameters
    ----------
    spec : str
        The text containing rules (rl) and conditional equations (ceq).

    Returns
    -------
    dict
        {'RULE': [...], 'EQ': [...]} where each list contains the
        extracted label strings.
    """
    rule_labels, eq_labels = set(), set()

    for m in _LABEL_RE.finditer(spec):
        if m.group('kind') == 'rl':
            rule_labels.add(m.group('label'))
        else:                       # 'ceq'
            eq_labels.add(m.group('label'))

    return {"Rule": rule_labels, "Eq": eq_labels}
