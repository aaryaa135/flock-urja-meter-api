"""Pydantic response models for verified portal fields only.

Only fields that were directly observed in the Chrome DevTools Network panel
are included. Unknown response metadata is preserved as ``dict`` rather than
invented.
"""

from typing import Any

from pydantic import BaseModel


class MeterRecord(BaseModel):
    """A single meter record as observed in the portal.

    Verified fields: meterId, serialNo, make, phaseType, installStatus, dtCode.
    """

    meterId: str
    serialNo: str
    make: str
    phaseType: str
    installStatus: str
    dtCode: str


class MeterSearchResponse(BaseModel):
    """Response from the portal meter search endpoint.

    Verified top-level fields: data, page, pageSize, total.
    Additional unknown keys are preserved in ``extra``.
    """

    data: list[MeterRecord]
    page: int
    pageSize: int
    total: int

    model_config = {"extra": "allow"}


class TransformerRecord(BaseModel):
    """A single transformer record as observed in the portal.

    Verified fields from the expanded first record: code, name, feederCode,
    capacityKva. Not claimed to be all fields in every record.
    """

    code: str
    name: str
    feederCode: str
    capacityKva: int


class TransformerListResponse(BaseModel):
    """Response from the portal transformers endpoint.

    Verified top-level field: data. Additional unknown keys are preserved.
    """

    data: list[TransformerRecord]

    model_config = {"extra": "allow"}


class PortalErrorResponse(BaseModel):
    """Standardized error response returned by our API when the portal fails."""

    detail: str
    status_code: int
    source: str = "portal"
