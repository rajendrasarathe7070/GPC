"""Notices tests."""

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.notices.models import Notice, NoticeCategory


@pytest.mark.django_db
class TestNoticeAPI:
    def setup_method(self):
        self.client = APIClient()
        self.category = NoticeCategory.objects.create(name="General", slug="general")
        self.notice = Notice.objects.create(
            title="Exam Schedule",
            slug="exam-schedule",
            content="Exams start next week.",
            category=self.category,
            priority="high",
        )

    def test_notice_list(self):
        url = reverse("notice-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True

    def test_notice_detail(self):
        url = reverse("notice-detail", kwargs={"slug": self.notice.slug})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["title"] == "Exam Schedule"
