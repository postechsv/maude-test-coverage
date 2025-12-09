import re
import json

_KIND_RE = re.compile(
    r'^\s*(?P<kind>eq|crl|rl|ceq)\b(?P<rest>.*)$',
    re.MULTILINE
)

_LABEL_RE_FORMAT_1 = re.compile(r'^\s*\[(?P<label>[^\]]+)\]\s*:')

_LABEL_RE_FORMAT_2 = re.compile(r'\[label\s+(?P<label>[^\]]+)\]')

def parse_labels(spec: str, target_labels: dict) -> dict:
    """
    Parse a Maude specification fragment and return a dictionary
    of rule and equation labels.

    This version handles two common label formats:
    1. eq [label-name] : ...
    2. eq ... [label label-name] .

    Parameters
    ----------
    spec : str
        The text containing rules (rl, crl) and equations (eq, ceq).

    Returns
    -------
    dict
        {'Rule': [...], 'Eq': [...]} where each list contains the
        extracted label strings, sorted alphabetically.
    """

    for m_kind in _KIND_RE.finditer(spec):
        kind = m_kind.group('kind')
        rest_of_line = m_kind.group('rest')
        
        label = None
        
        m_label_1 = _LABEL_RE_FORMAT_1.match(rest_of_line)
        if m_label_1:
            label = m_label_1.group('label')
        else:
            m_label_2 = _LABEL_RE_FORMAT_2.search(rest_of_line)
            if m_label_2:
                label = m_label_2.group('label')
        
        if label:
            if kind in ('rl', 'crl') and label in target_labels['Rule']:
                target_labels['Rule'][label] = True
            elif kind in ('eq', 'ceq') and label in target_labels['Eq']:
                target_labels['Eq'][label] = True
    return target_labels

# --- Example -------------------------------------------------------------
if __name__ == "__main__":
    sample = """
    *********** rule (Format 1)
    rl [aa] : Test2 => Test3 .

    *********** equation (Format 1)
    eq [bb] : Test = Test2 .

    *********** equation (Format 2)
    ceq Hi(N) = Hi(100) if N =/= 100 = true [label test1] .
    
    *********** rule (Format 2)
    rl BYE(N) => Hi(N) [label test2] .

    *********** indented rule (Format 1)
    crl [indented-rule] : A => B if C .

    *********** rule with no label
    rl NoLabel => Other .
    """
    # print(json.dumps(parse_labels(sample), indent=2))