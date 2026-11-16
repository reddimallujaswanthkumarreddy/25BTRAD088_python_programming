import sqlite3
import math
from datetime import datetime

# Database connection
conn = sqlite3.connect("parking.db")
cur = conn.cursor()

# Create parking table
cur.execute("""
CREATE TABLE IF NOT EXISTS slots (
    slot INTEGER PRIMARY KEY,
    vehicle TEXT UNIQUE,
    type TEXT,
    entry TEXT
)
""")

# Create history table
cur.execute("""
CREATE TABLE IF NOT EXISTS history (
    vehicle TEXT,
    type TEXT,
    slot INTEGER,
    hours INTEGER,
    fee INTEGER
)
""")

conn.commit()

# Parking settings
TOTAL_SLOTS = 20

RATE = {
    "bike": 10,
    "car": 20,
    "truck": 40
}


# 1. Park a vehicle
def park_vehicle():

    vehicle = input("Enter vehicle number: ").upper()
    vtype = input("Enter vehicle type: ").lower()

    if not vehicle:
        print("Vehicle number cannot be empty")
        return

    if vtype not in RATE:
        print("Invalid vehicle type")
        return

    cur.execute(
        "SELECT * FROM slots WHERE vehicle=?",
        (vehicle,)
    )

    if cur.fetchone():
        print("Vehicle is already parked")
        return

    cur.execute("SELECT slot FROM slots")
    occupied = [row[0] for row in cur.fetchall()]

    free_slot = None

    for i in range(1, TOTAL_SLOTS + 1):
        if i not in occupied:
            free_slot = i
            break

    if free_slot is None:
        print("Parking lot is full")
        return

    entry = datetime.now().isoformat()

    cur.execute(
        "INSERT INTO slots VALUES (?, ?, ?, ?)",
        (free_slot, vehicle, vtype, entry)
    )

    conn.commit()

    print("\nVehicle parked successfully!")
    print("Vehicle Number:", vehicle)
    print("Vehicle Type:", vtype)
    print("Assigned Slot:", free_slot)


# 2. Exit vehicle and calculate fee
def exit_vehicle():

    vehicle = input("Enter vehicle number: ").upper()

    cur.execute(
        "SELECT * FROM slots WHERE vehicle=?",
        (vehicle,)
    )

    data = cur.fetchone()

    if not data:
        print("Vehicle not found")
        return

    slot, vehicle, vtype, entry = data

    start_time = datetime.fromisoformat(entry)

    hours = max(
        1,
        math.ceil(
            (datetime.now() - start_time).total_seconds() / 3600
        )
    )

    fee = hours * RATE[vtype]

    cur.execute(
        "INSERT INTO history VALUES (?, ?, ?, ?, ?)",
        (vehicle, vtype, slot, hours, fee)
    )

    cur.execute(
        "DELETE FROM slots WHERE slot=?",
        (slot,)
    )

    conn.commit()

    print("\n----- PARKING BILL -----")
    print("Vehicle Number:", vehicle)
    print("Vehicle Type:", vtype)
    print("Parking Slot:", slot)
    print("Total Hours:", hours)
    print("Total Fee: Rs.", fee)
    print("------------------------")


# 3. Display parking status
def parking_status():

    cur.execute("SELECT * FROM slots ORDER BY slot")
    vehicles = cur.fetchall()

    print("\n----- PARKING STATUS -----")

    occupied = {row[0]: row for row in vehicles}

    for i in range(1, TOTAL_SLOTS + 1):

        if i in occupied:
            row = occupied[i]
            print(
                "Slot", i,
                "| Vehicle:", row[1],
                "| Type:", row[2],
                "| Occupied"
            )
        else:
            print("Slot", i, "| Free")

    print("Total Free Slots:", TOTAL_SLOTS - len(vehicles))
    print("Total Occupied Slots:", len(vehicles))


# 4. Search vehicle
def search_vehicle():

    vehicle = input("Enter vehicle number: ").upper()

    cur.execute(
        "SELECT * FROM slots WHERE vehicle=?",
        (vehicle,)
    )

    data = cur.fetchone()

    if data:
        print("\nVehicle Found!")
        print("Slot Number:", data[0])
        print("Vehicle Number:", data[1])
        print("Vehicle Type:", data[2])
        print("Entry Time:", data[3])
    else:
        print("Vehicle not found")


# 5. Display revenue report
def revenue_report():

    cur.execute(
        "SELECT SUM(fee) FROM history"
    )

    total = cur.fetchone()[0] or 0

    print("\n----- REVENUE REPORT -----")
    print("Total Revenue: Rs.", total)

    for vtype in RATE:

        cur.execute(
            "SELECT SUM(fee) FROM history WHERE type=?",
            (vtype,)
        )

        amount = cur.fetchone()[0] or 0

        print(vtype.capitalize(), "Revenue: Rs.", amount)


# 6. Display parking history
def parking_history():

    cur.execute("SELECT * FROM history")
    records = cur.fetchall()

    print("\n----- PARKING HISTORY -----")

    if not records:
        print("No parking history available")
        return

    for row in records:
        print(
            "Vehicle:", row[0],
            "| Type:", row[1],
            "| Slot:", row[2],
            "| Hours:", row[3],
            "| Fee: Rs.", row[4]
        )


# Main menu
while True:

    print("\n================================")
    print("       PARKEASE SYSTEM")
    print("================================")
    print("1. Park Vehicle")
    print("2. Exit Vehicle")
    print("3. Parking Status")
    print("4. Search Vehicle")
    print("5. Revenue Report")
    print("6. Parking History")
    print("7. Exit System")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        park_vehicle()

    elif choice == "2":
        exit_vehicle()

    elif choice == "3":
        parking_status()

    elif choice == "4":
        search_vehicle()

    elif choice == "5":
        revenue_report()

    elif choice == "6":
        parking_history()

    elif choice == "7":
        print("Thank you for using ParkEase!")
        break

    else:
        print("Invalid choice. Try again.")

conn.close()
