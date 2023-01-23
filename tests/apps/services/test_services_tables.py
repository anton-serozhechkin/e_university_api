from apps.services.models import Service, UserDocument, UserRequest, UserRequestReview, ServiceDocument, Status, Requisites
from tests.apps.services.factories import (
    ServiceFactory,
    UserRequestFactory,
    StatusFactory,
    RequisitesFactory,
    UserRequestReviewFactory,
    UserDocumentFactory,
    ServiceDocumentFactory,
)
from tests.bases import BaseModelFactory


class TestService:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=ServiceFactory, model=Service)

    def test__repr__(self) -> None:
        obj: Service = ServiceFactory()
        expected_result = (
            f'{obj.__class__.__name__}(service_id="{obj.service_id}",'
            f' service_name="{obj.service_name}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestUserRequest:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=UserRequestFactory, model=UserRequest)

    def test__repr__(self) -> None:
        obj: UserRequest = UserRequestFactory()
        expected_result = (
            f'{obj.__class__.__name__}(user_request_id="{obj.user_request_id}",'
            f' created_at="{obj.created_at}", comment="{obj.comment}",'
            f' user_id="{obj.user_id}", service_id="{obj.service_id}",'
            f' faculty_id="{obj.faculty_id}", university_id="{obj.university_id}",'
            f' status_id="{obj.status_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestStatus:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=StatusFactory, model=Status)

    def test__repr__(self) -> None:
        obj: Status = StatusFactory()
        expected_result = (
            f'{obj.__class__.__name__}(status_id="{obj.status_id}",'
            f' status_name="{obj.status_name}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestRequisites:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=RequisitesFactory, model=Requisites)

    def test__repr__(self) -> None:
        obj: Requisites = RequisitesFactory()
        expected_result = (
            f'{obj.__class__.__name__}(requisites_id="{obj.requisites_id}",'
            f' iban="{obj.iban}", organisation_code="{obj.organisation_code}",'
            f' payment_recognition="{obj.payment_recognition}",'
            f' university_id="{obj.university_id}", service_id="{obj.service_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestUserRequestReview:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=UserRequestReviewFactory, model=UserRequestReview)

    def test__repr__(self) -> None:
        obj: UserRequestReview = UserRequestReviewFactory()
        expected_result = (
            f'{obj.__class__.__name__}(user_request_review_id='
            f'"{obj.user_request_review_id}",'
            f' created_at="{obj.created_at}", room_number="{obj.room_number}",'
            f' start_accommodation_date="{obj.start_accommodation_date}",'
            f' end_accommodation_date="{obj.end_accommodation_date}",'
            f' total_sum="{obj.total_sum}",'
            f' payment_deadline_date="{obj.payment_deadline_date}",'
            f' remark="{obj.remark}", bed_place_id="{obj.bed_place_id}",'
            f' reviewer="{obj.reviewer}", hostel_id="{obj.hostel_id}",'
            f' university_id="{obj.university_id}",'
            f' user_request_id="{obj.user_request_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestUserDocument:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=UserDocumentFactory, model=UserDocument)

    def test__repr__(self) -> None:
        obj: UserDocument = UserDocumentFactory()
        expected_result = (
            f'{obj.__class__.__name__}(user_document_id="{obj.user_document_id}", '
            f'created_at="{obj.created_at}", name="{obj.name}", '
            f'content="{obj.content}", user_request_id="{obj.user_request_id}")'
        )
        result = obj.__repr__()
        assert expected_result == result


class TestServiceDocument:
    def test_factory(self) -> None:
        BaseModelFactory.check_factory(factory_class=ServiceDocumentFactory, model=ServiceDocument)

    def test__repr__(self) -> None:
        obj: ServiceDocument = ServiceDocumentFactory()
        expected_result = (
            f'{obj.__class__.__name__}(service_document_id='
            f'"{obj.service_document_id}", service_id="{obj.service_id}",'
            f'university_id="{obj.university_id}", documents="{obj.documents}"'
        )
        result = obj.__repr__()
        assert expected_result == result
