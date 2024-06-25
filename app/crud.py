from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from settings import db_settings
from .models import Service, ServiceStatus
from .schemas import ServiceSchema, ServiceStatusUpdate, ServiceStatusSchema

router = APIRouter()


@router.get("/")
def get_index():
    return {"message": "все работает"}


@router.post("/services", response_model=ServiceSchema)
async def create_service(service: ServiceSchema, session: AsyncSession = Depends(db_settings.get_session)):
    """
    Создает новый сервис в postgresql через classmethod в модели
    """
    result = await Service.create_service(service, session)
    return ServiceSchema.from_orm(result)


@router.get("/services", response_model=list[ServiceSchema])
async def get_services(session: AsyncSession = Depends(db_settings.get_session)):
    """
    Получает список всех сервисов
    """
    query = select(Service).order_by(Service.id)
    result = await session.execute(query)
    result = result.scalars().all()
    return [ServiceSchema.from_orm(service) for service in result]


@router.post("/service/{name}", response_model=ServiceStatusSchema)
async def update_history_service(name: str, service_status: ServiceStatusUpdate,
                                 session: AsyncSession = Depends(db_settings.get_session)):
    """
    Принимает статус сервиса, с указанием его имени
    """
    # проверяем, что такой сервис есть в базе
    id_service = select(Service).where(Service.name == name)
    query = await session.execute(id_service)
    id_service_query_result = query.scalars().first()
    if not id_service_query_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"сервис '{name}' на зарегистрирован в системе")
    new_status = await ServiceStatus.update_history_status(session, id_service_query_result, service_status)
    return ServiceStatusSchema.from_orm(new_status)


@router.get("/services/history")
async def get_all_history(session: AsyncSession = Depends(db_settings.get_session)):
    """
    Показывает все сервисы с историей
    """
    pass


@router.get("/services/history/{name}")
async def get_history_by_name(name: str, session: AsyncSession = Depends(db_settings.get_session)):
    """
    Показывает историю сервиса, указанного по имени
    """
    pass
