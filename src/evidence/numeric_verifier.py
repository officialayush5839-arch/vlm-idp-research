"""
Numeric and Unit Verification Module for Phase 7 Evidence Grounding.
Performs strict token, unit, scale, and formatting alignment between
numeric answer claims and extracted evidence units.
"""

import re
from typing import Dict, Any, List, Optional, Tuple


# Unit normalization map
UNIT_EQUIVALENCES = {
    "$": "USD",
    "dollar": "USD",
    "dollars": "USD",
    "usd": "USD",
    "€": "EUR",
    "eur": "EUR",
    "euro": "EUR",
    "£": "GBP",
    "gbp": "GBP",
    "pound": "GBP",
    "%": "PERCENT",
    "percent": "PERCENT",
    "percentage": "PERCENT",
    "m": "MILLION",
    "million": "MILLION",
    "millions": "MILLION",
    "b": "BILLION",
    "billion": "BILLION",
    "billions": "BILLION",
    "k": "THOUSAND",
    "thousand": "THOUSAND",
    "thousands": "THOUSAND",
}

NUMERIC_PATTERN = re.compile(
    r"""(?P<prefix>[$€£])?
        \s*
        (?P<sign>[-+])?
        (?P<num>\d+(?:,\d{3})*(?:\.\d+)?)
        \s*
        (?P<suffix>[%mMbBkK]|million|billion|thousand|percent)?
    """,
    re.VERBOSE | re.IGNORECASE
)


class NumericVerifier:
    """
    Verifies that numeric figures, signs, units, and scales
    asserted in candidate answers match supporting evidence.
    """

    @classmethod
    def extract_numeric_tokens(cls, text: str) -> List[Dict[str, Any]]:
        """
        Extract structured numeric tokens from text.
        """
        matches = []
        for m in NUMERIC_PATTERN.finditer(text):
            raw_num = m.group("num")
            if not raw_num:
                continue
            clean_num_str = raw_num.replace(",", "")
            try:
                val = float(clean_num_str)
            except ValueError:
                continue

            prefix = m.group("prefix") or ""
            suffix = m.group("suffix") or ""
            sign = m.group("sign") or ""

            # Standardize unit
            units = []
            if prefix and prefix.lower() in UNIT_EQUIVALENCES:
                units.append(UNIT_EQUIVALENCES[prefix.lower()])
            if suffix and suffix.lower() in UNIT_EQUIVALENCES:
                units.append(UNIT_EQUIVALENCES[suffix.lower()])

            # Decimal precision
            decimals = len(clean_num_str.split(".")[1]) if "." in clean_num_str else 0

            matches.append({
                "raw": m.group(0).strip(),
                "value": -val if sign == "-" else val,
                "units": set(units),
                "decimals": decimals,
                "has_sign": bool(sign),
                "sign": sign
            })
        return matches

    def verify_numeric_support(
        self,
        answer_text: str,
        evidence_text: str,
        allow_scale_equivalence: bool = True
    ) -> Dict[str, Any]:
        """
        Verify if numeric values asserted in answer are present in evidence text.
        """
        ans_nums = self.extract_numeric_tokens(answer_text)
        if not ans_nums:
            # Not a numeric question/answer claim
            return {
                "is_numeric_claim": False,
                "is_verified": True,
                "matches": [],
                "reason": "No numeric tokens detected in answer"
            }

        ev_nums = self.extract_numeric_tokens(evidence_text)
        if not ev_nums:
            return {
                "is_numeric_claim": True,
                "is_verified": False,
                "matches": [],
                "reason": "Evidence contains no numeric tokens to support claim"
            }

        # For every numeric token in answer, seek matching token in evidence
        all_matched = True
        matched_details = []

        for a_tok in ans_nums:
            matched = False
            a_val = a_tok["value"]
            a_units = a_tok["units"]

            for e_tok in ev_nums:
                e_val = e_tok["value"]
                e_units = e_tok["units"]

                # Case 1: Exact numerical equality and compatible units
                if abs(a_val - e_val) < 1e-5:
                    if not a_units or not e_units or not a_units.isdisjoint(e_units):
                        matched = True
                        matched_details.append({"answer": a_tok["raw"], "evidence": e_tok["raw"], "type": "exact"})
                        break

                # Case 2: Scale equivalence ($48.7M vs 48,700,000)
                if allow_scale_equivalence:
                    # check millions
                    if "MILLION" in a_units and abs(a_val * 1e6 - e_val) < 1e-2:
                        matched = True
                        matched_details.append({"answer": a_tok["raw"], "evidence": e_tok["raw"], "type": "scale_million"})
                        break
                    elif "MILLION" in e_units and abs(e_val * 1e6 - a_val) < 1e-2:
                        matched = True
                        matched_details.append({"answer": a_tok["raw"], "evidence": e_tok["raw"], "type": "scale_million"})
                        break
                    # check thousands
                    if "THOUSAND" in a_units and abs(a_val * 1e3 - e_val) < 1e-2:
                        matched = True
                        matched_details.append({"answer": a_tok["raw"], "evidence": e_tok["raw"], "type": "scale_thousand"})
                        break
                    elif "THOUSAND" in e_units and abs(e_val * 1e3 - a_val) < 1e-2:
                        matched = True
                        matched_details.append({"answer": a_tok["raw"], "evidence": e_tok["raw"], "type": "scale_thousand"})
                        break

            if not matched:
                all_matched = False

        return {
            "is_numeric_claim": True,
            "is_verified": all_matched,
            "matches": matched_details,
            "reason": "All numeric tokens verified" if all_matched else "Unmatched numeric tokens in evidence"
        }
