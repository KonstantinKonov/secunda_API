from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey

from src.database import Base


class OrganizationActivity(Base):
    __tablename__ = "organization_activity_table"

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True)

    organization = relationship("Organization", back_populates="organization_activities")
    activity = relationship("Activity", back_populates="organization_activities")
