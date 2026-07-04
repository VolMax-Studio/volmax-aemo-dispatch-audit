import os
import shutil
import sys

import argparse
import glob

def reproduce():
    parser = argparse.ArgumentParser(description="Reproduce AEMO BESS fleet dispatch audit.")
    parser.add_argument("--clean", action="store_true", help="Force clean download and processing.")
    args = parser.parse_args()

    print("======================================================================")
    proc_dir = './data/processed'
    
    # Check if processed feather files are already present (12 months * 3 tables = 36 files)
    existing_feathers = glob.glob(os.path.join(proc_dir, "*.feather"))
    should_download = args.clean or (len(existing_feathers) < 36)
    
    if args.clean:
        print(f"Cleaning existing processed files in {proc_dir}...")
        if os.path.exists(proc_dir):
            for f in os.listdir(proc_dir):
                if f.endswith('.feather') or f.endswith('.json'):
                    os.remove(os.path.join(proc_dir, f))
    
    if should_download:
        print("\nStarting data download and SHA-256 manifest verification...")
        try:
            from download_aemo_data import run_pipeline
            run_pipeline()
        except Exception as e:
            print(f"\nCRITICAL: Reproduction failed during data download/verification phase: {e}")
            sys.exit(1)
    else:
        print(f"\nFound {len(existing_feathers)} processed files in {proc_dir}. Skipping download phase.")
        
    # 3. Compile the L1 Integrity Report
    print("\nCompiling Level 1 Integrity Report...")
    try:
        from compile_l1_integrity import compile_report
        compile_report()
    except Exception as e:
        print(f"\nCRITICAL: Reproduction failed during report compilation phase: {e}")
        sys.exit(1)
        
    # 4. Run Level 2 Claims Verification
    print("\nRunning Level 2 Claims Verification...")
    try:
        from verify_aemo_claims import main as run_l2
        run_l2()
    except Exception as e:
        print(f"\nCRITICAL: Reproduction failed during Level 2 claims verification phase: {e}")
        sys.exit(1)
        
    # 4b. Compile FCAS Frequency Telemetry
    print("\nCompiling FCAS Grid Frequency Telemetry...")
    try:
        from compile_fcas_frequency import main as run_fcas_freq
        run_fcas_freq()
    except Exception as e:
        print(f"\nCRITICAL: Reproduction failed during FCAS frequency compilation phase: {e}")
        sys.exit(1)
        
    # 5. Run Level 3 FCAS Performance Audit
    print("\nRunning Level 3 FCAS Performance Audit...")
    try:
        from verify_aemo_fcas import main as run_l3
        run_l3()
    except Exception as e:
        print(f"\nCRITICAL: Reproduction failed during Level 3 FCAS performance audit phase: {e}")
        sys.exit(1)
        
    print("\n======================================================================")
    print("SUCCESS: Audit reproduction completed successfully.")
    print("All downloaded AEMO raw tables matched their pinned SHA-256 hashes.")
    print("Processed datasets, Level 2/3 reports, and plots have been regenerated.")
    print("======================================================================")

if __name__ == '__main__':
    reproduce()
