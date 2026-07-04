import os
import sys
from nemosis import dynamic_data_compiler

def test_schema_dump():
    start_time = '2025/06/01 00:00:00'
    end_time = '2025/06/01 01:00:00'
    raw_dir = './data/raw_cache'
    os.makedirs(raw_dir, exist_ok=True)

    print("--- Downloading DISPATCH_UNIT_SCADA ---")
    try:
        scada_df = dynamic_data_compiler(
            start_time=start_time,
            end_time=end_time,
            table_name='DISPATCH_UNIT_SCADA',
            raw_data_location=raw_dir,
            select_columns=['SETTLEMENTDATE', 'DUID', 'SCADAVALUE']
        )
        print("SCADA Columns:", scada_df.columns.tolist())
        print("SCADA Sample:\n", scada_df.head(5))
    except Exception as e:
        print("Failed to download SCADA:", str(e))

    print("\n--- Downloading DISPATCHLOAD ---")
    try:
        dispatch_df = dynamic_data_compiler(
            start_time=start_time,
            end_time=end_time,
            table_name='DISPATCHLOAD',
            raw_data_location=raw_dir
        )
        print("DISPATCHLOAD Columns:", dispatch_df.columns.tolist())
        print("DISPATCHLOAD Sample:\n", dispatch_df.head(5))
    except Exception as e:
        print("Failed to download DISPATCHLOAD:", str(e))

if __name__ == '__main__':
    test_schema_dump()
