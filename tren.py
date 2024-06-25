from datetime import datetime, timezone

a = datetime.now(timezone.utc).replace(tzinfo=None)
print(a)