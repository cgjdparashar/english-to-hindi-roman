#!/usr/bin/env python3
"""
Setup script for Playwright testing environment
Run this after installing dependencies with: uv add playwright pytest pytest-playwright
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and print results"""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        print("✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🎭 PLAYWRIGHT SETUP FOR HINGLISH TRANSLATION TESTS")
    print("=" * 60)
    
    # Check if we're in the right directory
    project_root = Path.cwd()
    if not (project_root / "pyproject.toml").exists():
        print("❌ Error: Run this script from the project root directory")
        sys.exit(1)
    
    print(f"📁 Project root: {project_root}")
    
    # Install Playwright browsers
    install_cmd = [sys.executable, "-m", "playwright", "install"]
    if not run_command(install_cmd, "Installing Playwright browsers"):
        print("⚠️  Browser installation failed, but continuing...")
    
    # Install system dependencies (Linux/WSL only)
    deps_cmd = [sys.executable, "-m", "playwright", "install-deps"]
    if not run_command(deps_cmd, "Installing system dependencies"):
        print("⚠️  System deps installation failed (normal on Windows)")
    
    # Verify installation
    print("\n🔍 VERIFICATION")
    print("-" * 30)
    
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Playwright sync_api import successful")
        
        with sync_playwright() as p:
            browsers = []
            try:
                chromium = p.chromium.launch(headless=True)
                browsers.append("Chromium")
                chromium.close()
            except Exception as e:
                print(f"⚠️  Chromium: {e}")
            
            try:
                firefox = p.firefox.launch(headless=True)
                browsers.append("Firefox")
                firefox.close()
            except Exception as e:
                print(f"⚠️  Firefox: {e}")
            
            try:
                webkit = p.webkit.launch(headless=True)
                browsers.append("WebKit")
                webkit.close()
            except Exception as e:
                print(f"⚠️  WebKit: {e}")
        
        print(f"✅ Available browsers: {', '.join(browsers)}")
        
    except ImportError as e:
        print(f"❌ Playwright import failed: {e}")
        print("Try: uv add playwright pytest pytest-playwright")
        return False
    
    # Check story files exist
    story_dir = project_root / "story" / "output" / "story_31_10"
    if story_dir.exists():
        txt_files = list(story_dir.glob("*.txt"))
        print(f"✅ Found {len(txt_files)} story files for testing")
    else:
        print("⚠️  Story files not found - run file splitter first")
    
    print("\n🚀 READY TO RUN TESTS!")
    print("=" * 40)
    print("Run tests with:")
    print("  pytest tests/test_hinglish_playwright.py -v")
    print("  pytest tests/test_hinglish_playwright.py::test_single_story_translation -v")
    print("  pytest tests/test_hinglish_playwright.py -v --headed  # See browser")
    print("\nTo run specific test:")
    print("  pytest tests/test_hinglish_playwright.py::test_translation_quality_samples -v")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)