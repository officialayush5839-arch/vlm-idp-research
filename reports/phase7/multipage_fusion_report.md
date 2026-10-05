# Multi-Page Evidence Aggregation and Fusion Report

## 1. Methodology
Long documents present unique challenges where supporting evidence spans multiple pages (e.g. definitions on page 1, tables on page 10, footnotes on page 15). The multi-page aggregator (`src/evidence/multipage_aggregator.py`):
- Groups atomic evidence units by 1-indexed page number.
- Preserves fine-grained region coordinates and individual unit hashes across all pages.
- Calculates normalized Shannon entropy to quantify cross-page evidence dispersion:
  $$H = -\sum_{p=1}^P \frac{N_p}{N_{\text{total}}} \log_2 \left(\frac{N_p}{N_{\text{total}}}\right), \quad \text{Score}_{\text{cross-page}} = \frac{H}{\log_2 P}$$

## 2. Experimental Observations
In 50-page documents with multi-page queries, the multi-page aggregator successfully linked header regions on page 1 with tabular evidence on page 45 without dropping page provenance. Every citation retained its exact document and page identifier.
