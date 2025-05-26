from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table

from src.database import Base
#from src.models import Building, OrganizationActivity



class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False) # o2m

    phones = relationship("Phone", back_populates="organization", cascade="all, delete-orphan") # o2m
    organization_activities = relationship("OrganizationActivity", back_populates="organization", cascade="all, delete-orphan")
    building = relationship("Building", back_populates="organizations")