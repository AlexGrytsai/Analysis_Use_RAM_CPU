from datetime import datetime
from typing import Optional, List, Dict, Any

import pytz
from dateutil import parser
from pydantic import (
    BaseModel,
    field_validator,
    HttpUrl,
    Field,
    model_validator,
)


def ensure_utc(date_str: str) -> str | None:
    """
    Ensures that the provided date string is in UTC format.

    Args:
        date_str (Optional[str]): The date string to be converted.

    Returns:
        Optional[str]: The date string in UTC format,
        or None if the input is None.
    """
    if not date_str:
        return None

    date_obj = parser.isoparse(date_str)

    if date_obj.tzinfo is None:
        date_obj = date_obj.replace(tzinfo=pytz.UTC)
    else:
        date_obj = date_obj.astimezone(pytz.UTC)

    return date_obj.isoformat()


class SupplierValidator(BaseModel):
    legalName: str
    legal_id: int

    @model_validator(mode="before")
    def extract_value(cls, values: Dict) -> Dict:
        values["legalName"] = values.get("name", "")
        values["legal_id"] = values.get("identifier", {}).get("id")
        return values

    @field_validator("legal_id", mode="before")
    def validate_legal_id(cls, value: int | str) -> int | str:
        try:
            return int(value)
        except ValueError:
            return 0


class ProcuringEntityValidator(SupplierValidator):
    kind: str


class AwardValidator(BaseModel):
    date: datetime
    value: float
    supplier: SupplierValidator

    @field_validator("date", mode="before")
    def validate_date_utc(cls, value: str) -> str | None:
        return ensure_utc(value)

    @model_validator(mode="before")
    def extract_value(cls, values: Dict) -> Dict:
        values["value"] = values.get("value", {}).get("amount", 0.0)
        return values

    @model_validator(mode="before")
    def extract_suppliers(cls, values: List[Dict]) -> Dict:
        values[0]["supplier"] = values[0].get("suppliers")[0]
        return values[0]


class ContractValidator(BaseModel):
    awardID: str
    date: datetime
    contractID: str
    value: float


class DocumentValidator(BaseModel):
    title: str
    url: Optional[HttpUrl | str] = None
    datePublished: datetime
    dateModified: datetime

    @field_validator("datePublished", "dateModified", mode="before")
    def validate_date_utc(cls, value: Optional[str]) -> Optional[str]:
        return ensure_utc(value)


class TenderPeriodValidator(BaseModel):
    startDate: datetime
    endDate: datetime

    @field_validator("startDate", "endDate", mode="before")
    def validate_date_utc(cls, value: Optional[str]) -> Optional[str]:
        return ensure_utc(value)


class LotValidator(BaseModel):
    title: str
    date: datetime
    value: float

    @field_validator("date", mode="before")
    def validate_date_utc(cls, value: Optional[str]) -> Optional[str]:
        return ensure_utc(value)

    @model_validator(mode="before")
    def extract_value(cls, values: Dict) -> Dict:
        values["value"] = values.get("value", {}).get("amount", 0.0)
        return values


class ItemBidValidator(BaseModel):
    description: str
    unit: str
    quantity: int

    @model_validator(mode="before")
    def extract_unit(cls, values: Dict) -> Dict:
        values["unit"] = values.get("unit", {}).get("name", "")
        return values


class ItemValidator(ItemBidValidator):
    deliveryDate: Optional[datetime] = None

    @model_validator(mode="before")
    def extract_delivery_date(cls, values: Dict) -> Dict:
        values["deliveryDate"] = values.get("deliveryDate", {}).get("endDate")
        return values

    @field_validator("deliveryDate", mode="before")
    def validate_date_utc(cls, value: str) -> Optional[str]:
        return ensure_utc(value)


class BidValidator(BaseModel):
    date: datetime
    legalName: str
    legal_id: int
    value: Optional[float]
    items: Optional[List[ItemBidValidator]]

    @field_validator("date", mode="before")
    def validate_date_utc(cls, value: str) -> str | None:
        return ensure_utc(value)

    @model_validator(mode="before")
    def extract_legal_name(cls, values: Dict[str, Dict]) -> Dict[str, dict]:
        tenderer = values.get("tenderers")
        if tenderer:
            values["legalName"] = (
                tenderer[0].get("identifier", {}).get("legalName")
            )
        return values

    @model_validator(mode="before")
    def extract_legal_id(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get("tenderers"):
            try:
                values["legal_id"] = int(
                    values.get("tenderers")[0].get("identifier", {}).get("id")
                )
            except ValueError:
                values["legal_id"] = 0

        return values

    @model_validator(mode="before")
    def extract_value(cls, values: Dict[str, Dict]) -> Dict[str, dict]:
        if values.get("lotValues"):
            # If the tender specifies several lots for purchase,
            # then lotValues is applied.
            try:
                value = values["lotValues"][0].get("value").get("amount")
            except AttributeError:
                value = None
        else:
            value = values.get("value").get("amount")
        values["value"] = value
        return values

    @model_validator(mode="before")
    def extract_items(cls, values: Dict[str, Dict]) -> Dict[str, dict]:
        values["items"] = values.get("items")
        return values


class TenderConfigValidator(BaseModel):
    hasAuction: bool
    hasAwardingOrder: bool
    hasValueRestriction: bool
    valueCurrencyEquality: bool
    hasPrequalification: bool
    minBidsNumber: int
    hasPreSelectionAgreement: bool
    hasTenderComplaints: bool
    hasAwardComplaints: bool
    hasCancellationComplaints: bool
    hasValueEstimation: bool
    hasQualificationComplaints: bool
    tenderComplainRegulation: int
    qualificationComplainDuration: int
    awardComplainDuration: int
    cancellationComplainDuration: int
    clarificationUntilDuration: int
    qualificationDuration: int
    restricted: bool


class TenderDataValidator(BaseModel):
    tenderID: str
    api_id: str = Field(..., alias="id")
    dateModified: datetime
    dateCreated: datetime
    documents: List[DocumentValidator]
    procurementMethod: str
    procurementMethodType: str
    status: str
    title: str
    value: float
    tenderPeriod: Optional[TenderPeriodValidator] = None
    lots: Optional[List[LotValidator]] = None
    procuringEntity: ProcuringEntityValidator
    items: Optional[List[ItemValidator]] = None
    bids: Optional[List[BidValidator]] = None
    date_of_disclosure: Optional[datetime] = None
    award: Optional[AwardValidator] = Field(default=None, alias="awards")
    contract: Optional[ContractValidator] = Field(
        default=None, alias="contracts"
    )

    config: TenderConfigValidator
    keywords: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    def extract_value(cls, values: Dict) -> Dict:
        values["value"] = values.get("value", {}).get("amount", 0.0)
        return values

    @model_validator(mode="before")
    def validate_bids(cls, values: Dict) -> Dict:
        if values.get("bids"):
            values["bids"] = [
                bid
                for bid in values["bids"]
                if bid["status"] not in ("deleted", "invalid")
            ]
        return values

    @model_validator(mode="before")
    def validate_date_of_disclosure(cls, values: Dict) -> Dict:
        if values.get("awardPeriod", {}).get("startDate"):
            values["date_of_disclosure"] = values.get("awardPeriod", {}).get(
                "startDate"
            )
        return values

    @model_validator(mode="before")
    def extract_procuring_entity(cls, values: Dict) -> Dict:
        kind = values.get("procuringEntity", {}).get("kind")
        values["procuringEntity"] = values.get("procuringEntity", {})
        if values["procuringEntity"]:
            values["procuringEntity"]["identifier"]["kind"] = kind
        return values

    @model_validator(mode="before")
    def extract_contract(cls, values: Dict) -> Dict:
        if values.get("contracts"):
            values["contracts"][0]["value"] = (
                values["contracts"][0].get("value", {}).get("amount", 0.0)
            )
            values["contracts"] = values["contracts"][0]
        return values

    @field_validator(
        "dateModified", "dateCreated", "date_of_disclosure", mode="before"
    )
    def validate_date_utc(cls, value: str) -> str | None:
        return ensure_utc(value)

    def __init__(self, **data):
        tender_data = data.pop("data", {})
        super().__init__(**data, **tender_data)
