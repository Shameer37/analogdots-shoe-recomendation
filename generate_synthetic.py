# data/generate_synthetic.py (concept)
import random, csv, json, uuid
from datetime import datetime, timedelta

NUM_USERS = 1000
NUM_SHOES = 500
NUM_INTERACTIONS = 30000

types = ["casual","running","formal","boots","sandals"]
materials = ["leather","synthetic","knit","canvas"]
seasons = ["all","summer","winter"]
care = ["handwash","machine_wash","dry_clean","none"]

# generate shoes
shoes = []
for sid in range(1, NUM_SHOES+1):
    shoe = {
        "shoe_id": sid,
        "brand": f"Brand{random.randint(1,50)}",
        "model": f"Model{random.randint(1,1000)}",
        "type": random.choice(types),
        "material": random.choice(materials),
        "color": random.choice(["black","white","blue","brown","grey"]),
        "size": random.choice([6,7,8,9,10,11]),
        "water_resistant": random.random() < 0.2,
        "season": random.choice(seasons),
        "comfort_score": round(random.random(), 2),
        "care_required": random.choice(care)
    }
    shoes.append(shoe)

# write catalog
with open('sample_shoe_catalog.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=shoes[0].keys())
    writer.writeheader()
    writer.writerows(shoes)

# generate interactions
events = []
for i in range(NUM_INTERACTIONS):
    user = random.randint(1, NUM_USERS)
    shoe = random.randint(1, NUM_SHOES)
    ev = random.choices(["view","wishlist","add_to_cart","purchase","rating"], weights=[0.6,0.15,0.1,0.1,0.05])[0]
    rating = round(random.uniform(1,5),1) if ev=="rating" else (round(random.uniform(3,5),1) if ev=="purchase" and random.random()<0.3 else "")
    ts = (datetime.now() - timedelta(days=random.randint(0,365))).isoformat()
    events.append({"interaction_id": i+1, "user_id": user, "shoe_id": shoe, "event_type": ev, "rating": rating, "timestamp": ts})

with open('sample_user_interactions.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=events[0].keys())
    writer.writeheader()
    writer.writerows(events)

# generate device care logs (small)
care_logs=[]
for i in range(int(NUM_USERS*0.2)):
    user = random.randint(1, NUM_USERS)
    shoe = random.randint(1, NUM_SHOES)
    mode = random.choice(["quick_clean","deep_clean","polish"])
    dur = random.randint(5,60)
    ts = (datetime.now() - timedelta(days=random.randint(0,365))).isoformat()
    care_logs.append({"care_id": i+1, "user_id": user, "shoe_id": shoe, "device_mode": mode, "duration_minutes": dur, "timestamp": ts})

with open('sample_device_care_history.csv','w',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=care_logs[0].keys())
    writer.writeheader()
    writer.writerows(care_logs)
