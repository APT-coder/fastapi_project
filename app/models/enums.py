from enum import Enum

class UserStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"


class DocumentType(str, Enum):
    INVOICE = "invoice"
    ORDER_SUMMARY = "order_summary"


class DocumentStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
