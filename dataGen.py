import json
import random
from datetime import datetime, timedelta


def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


segments = [
    "Vielfahrer",
    "Gelegenheitsbesucher",
    "Merchandise Käufer",
    "Social Media Fan",
    "Newsletter Abonnent",
]


def generate_fan(id):
    last_contact = random_date(datetime(2024, 1, 1), datetime(2025, 9, 1)).strftime(
        "%Y-%m-%d"
    )
    frequency = random.randint(1, 50)
    monetary = round(random.uniform(0, 1500), 2)
    clv = round(monetary * random.uniform(1.1, 2.5), 2)
    fan_segments = random.sample(segments, random.randint(1, 3))
    return {
        "id": id,
        "name": f"Fan{id:03d}",
        "last_contact": last_contact,
        "frequency": frequency,
        "monetary": monetary,
        "clv": clv,
        "segments": fan_segments,
        "social_media_interactions": random.randint(0, 100),
        "newsletter": random.choice([True, False]),
        "satisfaction": random.randint(1, 10),
    }


data = [generate_fan(i) for i in range(1, 101)]

with open("fans_data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Generated fans_data.json with 100 sample fans.")
