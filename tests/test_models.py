"""Tests for Pydantic response models (verified fields only)."""

from app.portal.models import MeterRecord, MeterSearchResponse, TransformerRecord


def test_meter_record_verified_fields():
    """MeterRecord should accept only verified fields."""
    record = MeterRecord(
        meterId="J100000",
        serialNo="SE33962",
        make="HPL",
        phaseType="single",
        installStatus="Decommissioned",
        dtCode="DT-001",
    )
    assert record.meterId == "J100000"
    assert record.serialNo == "SE33962"
    assert record.make == "HPL"
    assert record.phaseType == "single"
    assert record.installStatus == "Decommissioned"
    assert record.dtCode == "DT-001"


def test_meter_search_response_verified_fields():
    """MeterSearchResponse should have verified top-level fields."""
    response = MeterSearchResponse(
        data=[
            MeterRecord(
                meterId="J100000",
                serialNo="SE33962",
                make="HPL",
                phaseType="single",
                installStatus="Decommissioned",
                dtCode="DT-001",
            )
        ],
        page=1,
        pageSize=20,
        total=403,
    )
    assert response.page == 1
    assert response.pageSize == 20
    assert response.total == 403
    assert len(response.data) == 1


def test_meter_search_response_preserves_extra():
    """MeterSearchResponse should preserve unknown keys (extra=allow)."""
    response = MeterSearchResponse(
        data=[],
        page=1,
        pageSize=20,
        total=0,
        extraField="unknown",
    )
    assert response.extraField == "unknown"


def test_transformer_record_verified_fields():
    """TransformerRecord should accept verified fields from expanded first record."""
    record = TransformerRecord(
        code="DT-001",
        name="Malviya Nagar DT 1",
        feederCode="F-001",
        capacityKva=100,
    )
    assert record.code == "DT-001"
    assert record.name == "Malviya Nagar DT 1"
    assert record.feederCode == "F-001"
    assert record.capacityKva == 100
