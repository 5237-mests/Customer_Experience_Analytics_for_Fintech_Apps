import pandas as pd
import oracledb

# --- Configuration ---
DB_CONFIG = {
    "user": "bank_reviews",
    "password": "mypassword",
    "host": "localhost",
    "port": 1521,
    "service_name": "XEPDB1"
}

# List of your CSV files to process
# Ensure these paths are correct relative to where you run the script
CSV_FILES = [
    # "../data/processed_boa_bank_reviews.csv"
    # "../data/processed_cbe_bank_reviews.csv",
    # "../data/processed_dashen_bank_reviews.csv"
]

# --- Database Operations ---

def get_db_connection():
    """Establishes and returns an Oracle database connection."""
    try:
        conn = oracledb.connect(**DB_CONFIG)
        print("Connected to the database successfully!")
        return conn
    except oracledb.Error as e:
        error_obj, = e.args
        print(f"Error connecting to Oracle Database:")
        print(f"  Code: {error_obj.code}")
        print(f"  Message: {error_obj.message}")
        print(f"  Help: {error_obj.help_url}")
        return None

def get_existing_bank_ids(cursor):
    """
    Retrieves existing bank names and their IDs from the 'banks' table.
    Returns a dictionary mapping bank names to their IDs.
    """
    bank_ids = {}
    try:
        cursor.execute("SELECT id, name FROM banks")
        for row in cursor:
            bank_id, bank_name = row
            bank_ids[bank_name] = int(bank_id)
        print(f"Retrieved {len(bank_ids)} existing banks from the database.")
    except oracledb.Error as e:
        error_obj, = e.args
        print(f"Error retrieving existing banks: {error_obj.message}")
        # Re-raise to ensure transaction rollback in main
        raise
    return bank_ids

def insert_reviews(cursor, df_reviews, bank_id_map):
    """
    Inserts review data into the 'reviews' table.
    Uses executemany for efficiency.
    """
    if df_reviews.empty:
        print("No reviews to insert.")
        return

    data_to_insert = []
    for _, row in df_reviews.iterrows():
        try:
            # Get the correct bank_id from the map based on the bank name in the row
            bank_id = bank_id_map.get(row["bank"])
            if bank_id is None:
                # This means a bank from the CSV wasn't found in the bank_id_map.
                # Check for exact name match between CSV 'bank' column and 'banks' table 'name' column.
                print(f"Warning: Bank '{row['bank']}' not found in the database's bank ID map, skipping review. Review text: '{row['review'][:50]}...'")
                continue

            data_to_insert.append({
                "review": row["review"],
                "rating": int(row["rating"]),
                "review_date": row["date"], # TO_DATE in SQL handles string date
                "bank_id": bank_id, # Use the dynamically looked-up bank_id
                "source": row["source"],
                "processed_review": row["processed_review"],
                "sentiment": row["sentiment"],
                "vader_sentiment": row["vader_sentiment"],
                "label": row["label"],
            })
        except KeyError as ke:
            print(f"Skipping row due to missing column: {ke} in review: {row.to_dict()}")
        except ValueError as ve:
            print(f"Skipping row due to data type conversion error: {ve} in review: {row.to_dict()}")

    if not data_to_insert:
        print("No valid review data to insert after processing.")
        return

    cursor.executemany("""
        INSERT INTO reviews (review, rating, review_date, bank_id, source, processed_review, sentiment, vader_sentiment, label)
        VALUES (:review, :rating, TO_DATE(:review_date, 'YYYY-MM-DD'), :bank_id, :source, :processed_review, :sentiment, :vader_sentiment, :label)
    """, data_to_insert, batcherrors=True)

    print(f"Inserted {len(data_to_insert)} reviews.")


## Main Execution Flow (Modified)

def main():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()

        # --- Get existing bank IDs from the database ---
        # This replaces the need for insert_banks
        bank_ids_map = get_existing_bank_ids(cursor)

        # --- Process reviews for each bank sequentially by loading specific CSVs ---
        for current_csv_path in CSV_FILES: # Use the global CSV_FILES list
            try:
                print(f"\n--- Processing reviews from: {current_csv_path} ---")
                df = pd.read_csv(current_csv_path)
                print(f"Loaded {len(df)} reviews from '{current_csv_path}'.")

                # --- Data Type Cleaning (CRITICAL) ---
                string_columns = ["review", "source", "processed_review", "sentiment", "vader_sentiment", "label", "bank"]
                for col in string_columns:
                    if col in df.columns:
                        df[col] = df[col].fillna('').astype(str)
                    else:
                        print(f"Warning: Column '{col}' not found in '{current_csv_path}'. This might cause issues.")

                if 'rating' in df.columns:
                    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0).astype(int)
                else:
                    print("Warning: 'rating' column not found in '{current_csv_path}'.")
                # --- End Data Type Cleaning ---

                # Assuming each CSV contains reviews predominantly for one bank,
                # or you want to derive the bank name from the file name, or the 'bank' column.
                # The 'bank' column in the CSV is the most reliable.
                unique_banks_in_current_csv = df["bank"].unique().tolist()
                
                for bank_name_from_csv in unique_banks_in_current_csv:
                    if bank_name_from_csv: # Ensure not an empty string
                        print(f"--- Inserting reviews for: {bank_name_from_csv} from {current_csv_path.split('/')[-1]} ---")
                        df_bank_reviews = df[df["bank"] == bank_name_from_csv].copy()
                        if not df_bank_reviews.empty:
                            # Pass the entire bank_ids_map to insert_reviews
                            insert_reviews(cursor, df_bank_reviews, bank_ids_map)
                        else:
                            print(f"No reviews found for {bank_name_from_csv} in {current_csv_path.split('/')[-1]}.")
            except FileNotFoundError:
                print(f"Error: CSV file not found at '{current_csv_path}'. Skipping this file.")
            except Exception as e:
                print(f"Error processing CSV '{current_csv_path}': {e}")
        
        conn.commit()
        print("\nAll data insertion operations completed and committed!")

    except oracledb.Error as e:
        error_obj, = e.args
        print(f"Oracle Database Error during main process:")
        print(f"  Code: {error_obj.code}")
        print(f"  Message: {error_obj.message}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred during main process: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
# This script is designed to insert bank reviews into an Oracle database.
