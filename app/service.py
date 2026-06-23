from app.schemas import FinancialDatasetMetadata, CheckResult, AssessmentResponse


def assess_metadata(metadata: FinancialDatasetMetadata) -> AssessmentResponse:
    results = []
    recommendations = []

    def add_check(principle: str, check_name: str, passed: bool, message: str, recommendation: str | None = None):
        results.append(
            CheckResult(
                principle=principle,
                check_name=check_name,
                passed=passed,
                message=message,
            )
        )
        if not passed and recommendation:
            recommendations.append(recommendation)

    # Findable
    add_check(
        principle="F",
        check_name="identifier_present",
        passed=bool(metadata.identifier.strip()),
        message="Dataset has a stable identifier." if metadata.identifier.strip() else "Dataset is missing a stable identifier.",
        recommendation="Add a stable identifier for the dataset.",
    )

    add_check(
        principle="F",
        check_name="dataset_name_present",
        passed=bool(metadata.dataset_name.strip()),
        message="Dataset has a title." if metadata.dataset_name.strip() else "Dataset is missing a title.",
        recommendation="Add a human-readable dataset name.",
    )

    add_check(
        principle="F",
        check_name="description_present",
        passed=bool(metadata.description.strip()),
        message="Dataset has a description." if metadata.description.strip() else "Dataset is missing a description.",
        recommendation="Add a clear description of dataset contents and purpose.",
    )

    # Accessible
    access_rights_present = bool(metadata.access_rights.strip())
    add_check(
        principle="A",
        check_name="access_rights_present",
        passed=access_rights_present,
        message="Access rights are defined." if access_rights_present else "Access rights are missing.",
        recommendation="Specify whether access is public, internal, restricted, or approval-based.",
    )

    access_contact_needed = metadata.access_rights.strip().lower() in {"restricted", "approval_required", "internal"}
    access_contact_present = metadata.access_request_contact is not None

    add_check(
        principle="A",
        check_name="access_request_contact_present",
        passed=(not access_contact_needed) or access_contact_present,
        message="Access request contact is available when needed."
        if (not access_contact_needed) or access_contact_present
        else "Restricted/internal datasets should provide an access request contact.",
        recommendation="Add an access request contact for non-public datasets.",
    )

    # Interoperable
    add_check(
        principle="I",
        check_name="schema_version_present",
        passed=bool(metadata.schema_version.strip()),
        message="Schema version is defined." if metadata.schema_version.strip() else "Schema version is missing.",
        recommendation="Add a schema version for the dataset structure.",
    )

    domain_standard_present = metadata.domain_standard is not None and bool(metadata.domain_standard.strip())
    add_check(
        principle="I",
        check_name="domain_standard_present",
        passed=domain_standard_present,
        message="Domain standard is referenced." if domain_standard_present else "No domain standard is referenced.",
        recommendation="Reference an internal or external domain standard if available.",
    )

    # Reusable
    add_check(
        principle="R",
        check_name="license_or_usage_terms_present",
        passed=bool(metadata.license_or_usage_terms.strip()),
        message="Usage terms are defined." if metadata.license_or_usage_terms.strip() else "Usage terms are missing.",
        recommendation="Add license information or internal usage terms.",
    )

    add_check(
        principle="R",
        check_name="provenance_present",
        passed=bool(metadata.provenance.strip()),
        message="Provenance is documented." if metadata.provenance.strip() else "Provenance is missing.",
        recommendation="Add dataset provenance or lineage information.",
    )

    add_check(
        principle="R",
        check_name="retention_policy_present",
        passed=bool(metadata.retention_policy.strip()),
        message="Retention policy is defined." if metadata.retention_policy.strip() else "Retention policy is missing.",
        recommendation="Add a retention or deletion policy.",
    )

    total_checks = len(results)
    passed_checks = sum(1 for result in results if result.passed)
    score = round(passed_checks / total_checks, 2) if total_checks else 0.0

    return AssessmentResponse(
        total_checks=total_checks,
        passed_checks=passed_checks,
        score=score,
        results=results,
        recommendations=recommendations,
    )