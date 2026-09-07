import threading
from sqlalchemy import text

from app.database import engine
from app.services.cache import redis_client

VIEW_KEY_PREFIX = "views:pending"


class ViewCounterService:
    def __init__(self):
        self._redis_ok = None

    def _check_redis(self) -> bool:
        if self._redis_ok is None:
            try:
                redis_client.ping()
                self._redis_ok = True
            except Exception:
                self._redis_ok = False
                print("[ViewCounter] Redis unavailable, falling back to direct DB writes")
        return self._redis_ok

    def increment(self, article_id: int) -> None:
        if self._check_redis():
            try:
                redis_client.hincrby(VIEW_KEY_PREFIX, str(article_id), 1)
                return
            except Exception:
                self._redis_ok = False
        try:
            with engine.connect() as conn:
                conn.execute(
                    text("UPDATE articles SET view_count = view_count + 1 WHERE id = :id"),
                    {"id": article_id},
                )
                conn.commit()
        except Exception as e:
            print(f"[ViewCounter] Direct DB increment failed for article {article_id}: {e}")

    def sync_to_database(self) -> None:
        try:
            pending = redis_client.hgetall(VIEW_KEY_PREFIX)
            if not pending:
                return

            with engine.connect() as conn:
                for article_id_str, count_str in pending.items():
                    count = int(count_str)
                    conn.execute(
                        text("UPDATE articles SET view_count = view_count + :c WHERE id = :id"),
                        {"c": count, "id": int(article_id_str)},
                    )
                conn.commit()

            redis_client.delete(VIEW_KEY_PREFIX)
            print(f"[ViewCounter] Synced {len(pending)} article(s) to DB")
        except Exception as e:
            print(f"[ViewCounter] Sync error: {e}")

    def start_auto_sync(self, interval_ms: int = 60000) -> None:
        def _loop():
            while True:
                import time

                time.sleep(interval_ms / 1000)
                self.sync_to_database()

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


view_counter = ViewCounterService()
