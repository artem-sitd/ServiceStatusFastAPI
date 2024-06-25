from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(200), nullable=True)

    @classmethod
    async def create_service(cls, new_name_description, session):
        """
        Создает новый сервис в postgresql через classmethod в модели
        """
        new_service = cls(name=new_name_description.name, description=new_name_description.description)
        session.add(new_service)
        await session.commit()
        return new_service


class ServiceStatus(Base):
    __tablename__ = "service_statuses"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    status = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc).replace(tzinfo=None))

    service = relationship("Service", back_populates="statuses")

    @classmethod
    async def update_history_status(cls, session, service, status):
        new_status = cls(service_id=service.id, status=status.status)
        session.add(new_status)
        await session.commit()
        return new_status


Service.statuses = relationship("ServiceStatus", order_by=ServiceStatus.timestamp,
                                back_populates="service")
