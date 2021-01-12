from typing import Any

from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from omigami.data_structures import RandomState
from omigami.models.estimator import Estimator
from omigami.models.pls_classifier import PLSClassifier
from omigami.models.sklearn_estimator import ScikitLearnPipeline, ScikitLearnEstimator


class ESTIMATORS:
    RFC = "RFC"
    XGBC = "XGBC"
    PLSC = "PLSC"


def make_estimator(estimator: Any, random_state: RandomState) -> Estimator:
    """Factory of Estimator classes based on an input `estimator`. So far, this method
    supports input strings or scikitlearn-like objects (e.g. xgboost.XGBClassifier).
    If a string is provided it must be one of `estimator.ESTIMATORS`

    Parameters
    ----------
    estimator : Any
        Input estimator. It can be a scikitlearn model or a string
    random_state : RandomState
        random state instance to control reproducibility

    Returns
    -------
    Estimator
        An instance of the Estimator class

    Raises
    ------
    ValueError
        if estimator does not comply with the aforementioned types
    """
    if isinstance(estimator, str):
        return _make_estimator_from_string(estimator, random_state)
    if isinstance(estimator, Pipeline):
        return ScikitLearnPipeline(estimator, random_state)
    if isinstance(estimator, BaseEstimator):
        return ScikitLearnEstimator(estimator, random_state)
    raise ValueError("Unknown type of estimator")


def _make_estimator_from_string(estimator: str, random_state: RandomState) -> Estimator:
    if estimator == ESTIMATORS.RFC:
        rfc = RandomForestClassifier(n_estimators=150)
        return ScikitLearnEstimator(rfc, random_state)
    if estimator == ESTIMATORS.PLSC:
        plsc = PLSClassifier()
        return ScikitLearnEstimator(plsc, random_state)
    if estimator == ESTIMATORS.XGBC:
        xgbc = XGBClassifier()
        return ScikitLearnEstimator(xgbc, random_state)
    raise ValueError("Unknown type of estimator")
