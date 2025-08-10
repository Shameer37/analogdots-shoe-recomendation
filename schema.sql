

-- 1. Shoe Catalog (sample_shoe_catalog.csv)
CREATE TABLE shoes (
    shoe_id INT PRIMARY KEY,
    brand VARCHAR(100),
    model VARCHAR(100),
    type VARCHAR(32),
    material VARCHAR(32),
    color VARCHAR(32),
    size SMALLINT,
    water_resistant BOOLEAN,
    season VARCHAR(16),
    comfort_score REAL,
    care_required VARCHAR(32)
);

-- 2. User Interactions (sample_user_interactions.csv)
CREATE TABLE user_interactions (
    interaction_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    shoe_id INT NOT NULL REFERENCES shoes(shoe_id) ON DELETE CASCADE,
    event_type VARCHAR(32) NOT NULL,
    rating REAL,
    timestamp TIMESTAMP
);

CREATE INDEX idx_ui_user ON user_interactions(user_id);
CREATE INDEX idx_ui_shoe ON user_interactions(shoe_id);

-- 3. Device Care History (sample_device_care_history.csv)
CREATE TABLE device_care_history (
    care_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    shoe_id INT NOT NULL REFERENCES shoes(shoe_id) ON DELETE CASCADE,
    device_mode VARCHAR(32),
    duration_minutes INT,
    timestamp TIMESTAMP
);

CREATE INDEX idx_dch_user ON device_care_history(user_id);
CREATE INDEX idx_dch_shoe ON device_care_history(shoe_id);
