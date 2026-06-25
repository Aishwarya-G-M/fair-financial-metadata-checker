from pydantic import BaseModel, Field
from typing import Optional, List


class FinancialDatasetMetadata(BaseModel):
    identifier: str = Field(..., description="Stable identifier for the dataset")
    dataset_name: str = Field(..., description="Human-readable dataset title")
    description: str = Field(..., description="Description of dataset contents and purpose")
    owner_team: str = Field(..., description="Team responsible for the dataset")
    data_domain: str = Field(..., description="Business/domain classification")
    access_rights: str = Field(..., description="Access level such as internal or restricted")
    access_request_contact: Optional[str] = Field(
        default=None,
        description="Contact for requesting dataset access",
    )
    license_or_usage_terms: str = Field(..., description="Usage policy or license statement")
    provenance: str = Field(..., description="Origin or lineage of the dataset")
    schema_version: str = Field(..., description="Schema version for the dataset")
    domain_standard: Optional[str] = Field(
        default=None,
        description="Optional domain or metadata standard reference",
    )
    contains_pii: bool = Field(..., description="Whether the dataset contains personal data")
    retention_policy: str = Field(..., description="Retention or deletion policy")


class CheckResult(BaseModel):
    principle: str
    check_name: str
    passed: bool
    message: str

class PrincipleScore(BaseModel):
    principle: str
    total_checks: int
    passed_checks: int
    score: float

class AssessmentResponse(BaseModel):
    total_checks: int
    passed_checks: int
    score: float
    principle_scores: List[PrincipleScore]
    results: List[CheckResult]
    recommendations: List[str]
