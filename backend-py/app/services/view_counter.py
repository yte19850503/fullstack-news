import threading
from sqlalchemy import text

from app.database import engine
from app.services.cache import redis_client

VIEW_KEY_PREFIX = "views:pending"


class ViewCounterService:
    def increment(self, article_id: int) -> None:
        try:
            redis_client.hincrby(VIEW_KEY_PREFIX, str(article_id), 1)
        except Exception:
            pass

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
        except Exception as e:
            print(f"View sync error: {e}")

    def start_auto_sync(self, interval_ms: int = 60000) -> None:
        def _loop():
            while True:
                import time

                time.sleep(interval_ms / 1000)
                self.sync_to_database()

        t = threading.Thread(target=_loop, daemon=True)
        t.start()


view_counter = ViewCounterService()
