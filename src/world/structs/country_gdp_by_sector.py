from dataclasses import dataclass

@dataclass(frozen=True)
class CountryGDPBySector:
    country: str
    agriculture_percent: float
    agriculture_year: int
    industry_percent: float
    industry_year: int
    services_percent: float
    services_year: int
