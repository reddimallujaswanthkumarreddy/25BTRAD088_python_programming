import unittest
import sqlite3
import math
from datetime import datetime

# Parking system settings
TOTAL_SLOTS = 20

RATE = {
    "bike": 10,
    "car": 20,
    "truck": 40
}


class TestParkEase(unittest.TestCase):

    def setUp(self):
        # Create temporary test database
        self.conn = sqlite3.connect(":memory:")
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE slots(
            slot INTEGER PRIMARY KEY,
            vehicle TEXT UNIQUE,
            type TEXT,
            entry TEXT
        )
        """)

        self.cur.execute("""
        CREATE TABLE history(
            vehicle TEXT,
            type TEXT,
            slot INTEGER,
            hours INTEGER,
            fee INTEGER
        )
        """)

        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    # Test 1: Vehicle parking
    def test_vehicle_parking(self):
        self.cur.execute(
            "INSERT INTO slots VALUES(?,?,?,?)",
            (1, "KA01AB1234", "car",
             datetime.now().isoformat())
        )

        self.cur.execute(
            "SELECT * FROM slots WHERE vehicle=?",
            ("KA01AB1234",)
        )

        self.assertIsNotNone(self.cur.fetchone())

    # Test 2: Duplicate vehicle
    def test_duplicate_vehicle(self):
        entry = datetime.now().isoformat()

        self.cur.execute(
            "INSERT INTO slots VALUES(?,?,?,?)",
            (1, "KA01AB1234", "car", entry)
        )

        with self.assertRaises(sqlite3.IntegrityError):
            self.cur.execute(
                "INSERT INTO slots VALUES(?,?,?,?)",
                (2, "KA01AB1234", "bike", entry)
            )

    # Test 3: Parking fee calculation
    def test_fee_calculation(self):
        hours = 3
        fee = hours * RATE["car"]

        self.assertEqual(fee, 60)

    # Test 4: Bike fee
    def test_bike_fee(self):
        fee = 2 * RATE["bike"]
        self.assertEqual(fee, 20)

    # Test 5: Truck fee
    def test_truck_fee(self):
        fee = 2 * RATE["truck"]
        self.assertEqual(fee, 80)

    # Test 6: Parking lot capacity
    def test_parking_capacity(self):
        self.assertEqual(TOTAL_SLOTS, 20)

    # Test 7: Parking hours
    def test_parking_hours(self):
        start = 2 * 3600
        hours = max(1, math.ceil(start / 3600))

        self.assertEqual(hours, 2)

    # Test 8: Vehicle search
    def test_vehicle_search(self):
        self.cur.execute(
            "INSERT INTO slots VALUES(?,?,?,?)",
            (1, "KA05CD5678", "bike",
             datetime.now().isoformat())
        )

        self.cur.execute(
            "SELECT * FROM slots WHERE vehicle=?",
            ("KA05CD5678",)
        )

        self.assertIsNotNone(self.cur.fetchone())

    # Test 9: Vehicle exit
    def test_vehicle_exit(self):
        self.cur.execute(
            "INSERT INTO slots VALUES(?,?,?,?)",
            (1, "KA01AB1234", "car",
             datetime.now().isoformat())
        )

        self.cur.execute(
            "DELETE FROM slots WHERE vehicle=?",
            ("KA01AB1234",)
        )

        self.cur.execute(
            "SELECT * FROM slots WHERE vehicle=?",
            ("KA01AB1234",)
        )

        self.assertIsNone(self.cur.fetchone())


# Run all test cases
if __name__ == "__main__":
    unittest.main(verbosity=2)
