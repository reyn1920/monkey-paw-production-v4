import sqlite3


def check_affiliate_programs_table():
    conn = sqlite3.connect("right_perspective.db")
    cursor = conn.cursor()

    # Check current table structure
    cursor.execute("PRAGMA table_info(affiliate_programs)")
    columns = cursor.fetchall()

    print("Current affiliate_programs table structure=")
    for col in columns:
        print(f"  {col[1]} {col[2]} (nullable: {not col[3]})")

    # Check if signup_url column exists
    column_names = [col[1] for col in columns]

    if "signup_url" not in column_names:
        print("\\nAdding signup_url column...")
        cursor.execute("ALTER TABLE affiliate_programs ADD COLUMN signup_url TEXT")
        conn.commit()
        print("signup_url column added successfully")
    else:
        print("\\nsignup_url column already exists")

    conn.close()
    print("\\nDatabase schema check completed")


if __name__ == "__main__":
    check_affiliate_programs_table()
