# Domain Definitions & Empirical Mapping

**Audited Phase:** Phase 10  
**Status:** COMPLETE  

---

## 1. Domain Registry Mapping
All 25 test documents from `experiments/phase6/indexes/corpus_manifest.json` are partitioned into 5 balanced evaluation domains:

| Domain ID | Domain Description | Test Document IDs | Observable Features |
|---|---|---|---|
| **$D_0$** | In-Domain Control | `doc_mp_026`, `doc_mp_029`, `doc_mp_033`, `doc_mp_037`, `doc_mp_041` | Standard multi-page, balanced whitespace |
| **$D_1$** | Layout Shift | `doc_mp_027`, `doc_mp_031`, `doc_mp_035`, `doc_mp_039`, `doc_mp_043` | High table density, multi-column geometry |
| **$D_2$** | Visual Style Shift | `doc_mp_028`, `doc_mp_032`, `doc_mp_036`, `doc_mp_040`, `doc_mp_044` | Heavy scan artifacts, low contrast, high blur |
| **$D_3$** | Structure Shift | `doc_mp_030`, `doc_mp_034`, `doc_mp_038`, `doc_mp_042`, `doc_mp_046` | Irregular key-value form fields |
| **$D_4$** | Combined Shift | `doc_mp_045`, `doc_mp_047`, `doc_mp_048`, `doc_mp_049`, `doc_mp_050` | Multimodal combined stress |
