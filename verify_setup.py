#!/usr/bin/env python3
"""
Setup verification script for baswana-sen-spanner-experiments.
Verifies that all required packages are installed and can be imported.
"""

import sys

def verify_imports():
    """Verify that all required packages can be imported."""
    packages = {
        'numpy': 'numpy',
        'scipy': 'scipy',
        'networkx': 'networkx',
        'matplotlib': 'matplotlib',
        'pandas': 'pandas',
        'tqdm': 'tqdm',
        'jupyter': 'jupyter',
        'jupyterlab': 'jupyterlab',
    }
    
    failed = []
    success = []
    
    for name, module in packages.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', 'unknown')
            success.append(f"✅ {name}: {version}")
        except ImportError as e:
            failed.append(f"❌ {name}: {e}")
    
    print("=" * 60)
    print("Package Import Verification")
    print("=" * 60)
    
    if success:
        print("\nSuccessfully imported packages:")
        for msg in success:
            print(f"  {msg}")
    
    if failed:
        print("\nFailed to import packages:")
        for msg in failed:
            print(f"  {msg}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All packages verified successfully!")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = verify_imports()
    sys.exit(0 if success else 1)

