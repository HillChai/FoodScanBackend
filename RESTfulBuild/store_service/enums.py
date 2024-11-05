from enum import Enum

class PERMISSION(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    NO_PERMISSION = "NO_PERMISSION"