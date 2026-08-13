from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DimYear(Base):
    __tablename__ = "dim_year"
    year_id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False, unique=True)


class DimCountry(Base):
    __tablename__ = "dim_country"
    country_id = Column(Integer, primary_key=True)
    code = Column(String(3), nullable=False, unique=True)
    name = Column(String(100), nullable=False)


class DimIndicator(Base):
    __tablename__ = "dim_indicator"
    indicator_id = Column(Integer, primary_key=True)
    wb_code = Column(String(30), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    unit = Column(String(50), nullable=False)


class FactEconomic(Base):
    __tablename__ = "fact_economic"
    fact_id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey("dim_year.year_id"), nullable=False)
    country_id = Column(Integer, ForeignKey("dim_country.country_id"), nullable=False)
    indicator_id = Column(Integer, ForeignKey("dim_indicator.indicator_id"), nullable=False)
    value = Column(Float, nullable=False)
    source_url = Column(String)
    ingested_at = Column(DateTime, server_default=func.now())