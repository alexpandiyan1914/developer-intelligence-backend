from enum import Enum


class SourceType(str, Enum):
    RSS = "RSS"
    PUBLIC_API = "PUBLIC_API"
    GITHUB_RELEASE = "GITHUB_RELEASE"
    MANUAL = "MANUAL"


class SourceCategory(str, Enum):
    OFFICIAL = "OFFICIAL"
    NEWS = "NEWS"
    COMMUNITY = "COMMUNITY"
    RESEARCH = "RESEARCH"
    GOVERNMENT = "GOVERNMENT"
    RELEASE = "RELEASE"


class RegionCode(str, Enum):
    GLOBAL = "GLOBAL"
    INDIA = "INDIA"
    TAMIL_NADU = "TAMIL_NADU"