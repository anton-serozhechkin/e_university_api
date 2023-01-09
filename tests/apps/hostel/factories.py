from apps.hostel.models import BedPlace, Commandant, Hostel
from apps.hostel.schemas import BedPlaceOut, HostelListOut
from tests.bases import AsyncPersistenceHandler, BaseFactory


class BedPlaceFactory(BaseFactory):
    """BedPlaceFactory based on Faker and Pydantic"""

    __async_persistence__ = AsyncPersistenceHandler(model=BedPlace)
