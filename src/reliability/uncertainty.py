"""src/reliability/uncertainty.py
Computation and normalization of the 8-Dimensional Observable Uncertainty Vector.
"""

from src.reliability.schema import UncertaintyVector
from src.reliability.signals import ObservableSignals


class UncertaintyCalculator:
    """Calculates normalized uncertainty vector U in [0, 1]^8 from observable signals."""

    @staticmethod
    def compute_uncertainty_vector(signals: ObservableSignals) -> UncertaintyVector:
        # High quality/retrieval/sufficiency/spatial/table/agreement = low uncertainty
        u_ret = max(0.0, min(1.0, 1.0 - signals.retrieval_score))
        u_sem = max(0.0, min(1.0, 1.0 - signals.semantic_score))
        u_spat = max(0.0, min(1.0, 1.0 - signals.spatial_score))
        
        # Numeric discrepancy is directly an uncertainty indicator
        u_num = max(0.0, min(1.0, signals.numeric_discrepancy))
        
        u_tab = max(0.0, min(1.0, 1.0 - signals.table_alignment_score))
        u_suff = max(0.0, min(1.0, 1.0 - signals.sufficiency_score))
        u_qual = max(0.0, min(1.0, 1.0 - signals.quality_score))
        u_agr = max(0.0, min(1.0, 1.0 - signals.agreement_score))

        return UncertaintyVector(
            u_retrieval=u_ret,
            u_semantic=u_sem,
            u_spatial=u_spat,
            u_numeric=u_num,
            u_table=u_tab,
            u_sufficiency=u_suff,
            u_quality=u_qual,
            u_agreement=u_agr,
        )
