from apps.common.services import AsyncCRUDBase
from apps.hostel.models import BedPlace, hostel_list_view

hostel_service = AsyncCRUDBase(model=hostel_list_view)
bed_place_service = AsyncCRUDBase(model=BedPlace)
