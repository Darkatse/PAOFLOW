#!/usr/bin/env python3
"""
Cleanup tool for example directories
"""

import os
import shutil

# Configuration
TARGET_DIRS = [d for d in os.listdir('.') if d.startswith('example') and os.path.isdir(d)]
WHITELIST = {'Reference', '.in', '.UPF', '.py', 'README', 'inputfile.xml', \
             'SnTe.save'}

def should_keep(path):
    """Check if path should be preserved"""
    basename = os.path.basename(path)
    # Keep whitelisted items and Reference directory
    return (basename in WHITELIST or
            os.path.splitext(path)[1] in WHITELIST or
            os.path.isdir(path) and basename == 'Reference' or
            os.path.isdir(path) and basename.startswith('example') or
            "Reference" in path or "SnTe.save" in path)

def collect_removals(root_dir):
    """Generate deletion list with relative paths"""
    for foldername, _, filenames in os.walk(root_dir, topdown=False):
        # Process files first
        for f in filenames:
            full_path = os.path.join(foldername, f)
            if not should_keep(full_path):
                yield full_path
        
        # Process directories after files
        if not should_keep(foldername):
            yield foldername

def safe_delete(path_list):
    """Delete files/folders with verification"""
    print("\nItems to be removed:")
    for item in path_list:
        print(f" - {item}")
    
    if input("\nConfirm deletion? (y/N): ").lower() == 'y':
        for item in path_list:
            try:
                if os.path.isfile(item) or os.path.islink(item):
                    os.unlink(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Error deleting {item}: {str(e)}")

def main():
    """Main cleanup workflow"""
    for target_dir in TARGET_DIRS:
        print(f"\nProcessing directory: {target_dir}")
        deletion_list = list(collect_removals(target_dir))
        
        if not deletion_list:
            print("No items to delete")
            continue
            
        safe_delete(deletion_list)

if __name__ == "__main__":
    main()
