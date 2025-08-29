import sqlite3, random, datetime, pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
DB_PATH = BASE / "app" / "data.db"

def ensure_db(seed: int = 42):
    random.seed(seed)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE merchants (merchant_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
    CREATE TABLE transactions (
        txn_id INTEGER PRIMARY KEY,
        merchant_id INTEGER NOT NULL,
        amount_cents INTEGER NOT NULL,
        txn_ts TEXT NOT NULL,
        card_last4 TEXT NOT NULL,
        FOREIGN KEY (merchant_id) REFERENCES merchants(merchant_id)
    );
    """)

    merchants = ["Acme","Globex","Soylent","Initech","Umbrella","Stark","Wayne","Wonka","Gekko","Tyrell"]
    cur.executemany("INSERT INTO merchants(name) VALUES (?)", [(m,) for m in merchants])

    now = datetime.datetime.utcnow()
    rows = []
    for _ in range(500):
        mid = random.randint(1, len(merchants))
        amount = random.randint(100, 200000)
        days_ago = random.randint(0, 150)
        dt = now - datetime.timedelta(days=days_ago, hours=random.randint(0,23), minutes=random.randint(0,59))
        last4 = f"{random.randint(0,9999):04d}"
        rows.append((mid, amount, dt.strftime("%Y-%m-%d %H:%M:%S"), last4))
    cur.executemany("INSERT INTO transactions(merchant_id, amount_cents, txn_ts, card_last4) VALUES (?,?,?,?)", rows)

    conn.commit()
    conn.close()
    print(f"Initialized DB at {DB_PATH}")

if __name__ == "__main__":
    ensure_db()
