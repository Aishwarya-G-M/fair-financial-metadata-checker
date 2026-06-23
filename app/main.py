from fastapi import FastAPI

from app.schemas import FinancialDatasetMetadata, AssessmentResponse
from app.service import assess_metadata

app = FastAPI(
    title="FAIR Financial Metadata Checker",
    version="0.1.0",
    description=(
        "A FastAPI service that evaluates FAIR-inspired metadata quality "
        "for controlled-access financial datasets."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/assess", response_model=AssessmentResponse)
def assess(metadata: FinancialDatasetMetadata) -> AssessmentResponse:
    return assess_metadata(metadata)