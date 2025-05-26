from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from src.database import Base
from src.models.associations import OrganizationActivity


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("activities.id"), nullable=True)

    parent = relationship("Activity", remote_side=[id], back_populates="children", lazy="selectin")
    children = relationship("Activity", back_populates="parent", cascade="all, delete-orphan", lazy="selectin")

    organization_activities = relationship("OrganizationActivity", back_populates="activity", cascade="all, delete-orphan", lazy="selectin")
