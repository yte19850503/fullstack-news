"""
广告模块测试

覆盖：
- 公开广告：按 position 获取、无广告时返回空
- 广告事件上报：impression / click
- 后台管理：ADMIN CRUD、非 ADMIN 被拒绝
"""

import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from conftest import auth_header


class TestPublicAds:
    def test_get_ads_empty(self, client):
        resp = client.get("/api/ads/public?position=header")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_ads_with_data(self, client, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Header Banner",
            position="header",
            ad_type="banner",
            platform="self",
            code="<div>Ad</div>",
            status=AdStatus.ACTIVE,
            weight=10,
        )
        db_session.add(slot)
        db_session.commit()

        resp = client.get("/api/ads/public?position=header")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["name"] == "Header Banner"
        assert "code" in data[0]

    def test_get_ads_wrong_position(self, client, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Sidebar Ad",
            position="sidebar",
            ad_type="banner",
            platform="self",
            code="<div>Sidebar</div>",
            status=AdStatus.ACTIVE,
            weight=10,
        )
        db_session.add(slot)
        db_session.commit()

        resp = client.get("/api/ads/public?position=header")
        assert resp.status_code == 200
        assert resp.json() == []


class TestAdEvent:
    def test_record_impression(self, client, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Test Ad",
            position="header",
            ad_type="banner",
            platform="self",
            code="<div>Ad</div>",
            status=AdStatus.ACTIVE,
            weight=1,
        )
        db_session.add(slot)
        db_session.commit()
        db_session.refresh(slot)

        resp = client.post(f"/api/ads/public/{slot.id}/event?event=impression")
        assert resp.status_code == 200
        assert resp.json()["message"] == "Recorded"

    def test_record_click(self, client, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Click Ad",
            position="sidebar",
            ad_type="banner",
            platform="self",
            code="<div>Click</div>",
            status=AdStatus.ACTIVE,
            weight=1,
        )
        db_session.add(slot)
        db_session.commit()
        db_session.refresh(slot)

        resp = client.post(f"/api/ads/public/{slot.id}/event?event=click")
        assert resp.status_code == 200

    def test_record_invalid_event(self, client, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Bad Event",
            position="header",
            ad_type="banner",
            platform="self",
            code="<div>Bad</div>",
            status=AdStatus.ACTIVE,
            weight=1,
        )
        db_session.add(slot)
        db_session.commit()
        db_session.refresh(slot)

        resp = client.post(f"/api/ads/public/{slot.id}/event?event=invalid")
        assert resp.status_code == 422


class TestAdminAds:
    def test_admin_create_slot(self, client, admin):
        resp = client.post(
            "/api/ads/",
            json={
                "name": "New Ad",
                "position": "footer",
                "ad_type": "banner",
                "platform": "self",
                "code": "<div>Footer Ad</div>",
                "weight": 5,
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "New Ad"
        assert data["position"] == "footer"

    def test_admin_list_slots(self, client, admin, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="List Test",
            position="header",
            ad_type="banner",
            platform="self",
            code="<div>Test</div>",
            status=AdStatus.ACTIVE,
            weight=1,
        )
        db_session.add(slot)
        db_session.commit()

        resp = client.get("/api/ads/", headers=auth_header(admin))
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    def test_admin_update_slot(self, client, admin, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Update Me",
            position="header",
            ad_type="banner",
            platform="self",
            code="<div>Old</div>",
            status=AdStatus.ACTIVE,
            weight=1,
        )
        db_session.add(slot)
        db_session.commit()
        db_session.refresh(slot)

        resp = client.put(
            f"/api/ads/{slot.id}",
            json={
                "name": "Updated Name",
            },
            headers=auth_header(admin),
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"

    def test_admin_delete_slot(self, client, admin, db_session):
        from app.models.ad import AdSlot, AdStatus

        slot = AdSlot(
            name="Delete Me",
            position="sidebar",
            ad_type="banner",
            platform="self",
            code="<div>Gone</div>",
            status=AdStatus.ACTIVE,
            weight=1,
        )
        db_session.add(slot)
        db_session.commit()
        db_session.refresh(slot)

        resp = client.delete(f"/api/ads/{slot.id}", headers=auth_header(admin))
        assert resp.status_code == 200

    def test_editor_cannot_manage_ads(self, client, editor):
        resp = client.post(
            "/api/ads/",
            json={
                "name": "Nope",
                "position": "header",
                "ad_type": "banner",
                "platform": "self",
                "code": "<div>No</div>",
            },
            headers=auth_header(editor),
        )
        assert resp.status_code == 403

    def test_admin_get_stats(self, client, admin):
        resp = client.get("/api/ads/stats?days=7", headers=auth_header(admin))
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
