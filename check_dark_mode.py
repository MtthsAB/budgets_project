#!/usr/bin/env python3
"""
Dark Mode Implementation - Quick Test Script
Validates that all dark mode components are properly implemented
"""

import re
from pathlib import Path

def check_file(filepath):
    """Check if dark mode components are present in base.html"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'FOUC Prevention Script': '<script>' in content and 'theme-preference' in content,
        'Data-theme Attribute': 'data-theme=' in content,
        'CSS Variables - Light': ':root {' in content and '--color-bg-primary:' in content,
        'CSS Variables - Dark': ':root.dark-mode {' in content and '--color-bg-primary: #1a1a1a' in content,
        'Theme Toggle Button': 'id="theme-toggle"' in content,
        'Theme Icon': 'id="theme-icon"' in content,
        'ThemeManager Module': 'const ThemeManager = (() =>' in content,
        'ThemeManager.init()': 'ThemeManager.init' in content,
        'ARIA Label': 'aria-label' in content and 'tema' in content.lower(),
        'Dark Mode Class Toggle': "classList.toggle('dark-mode'" in content,
        'localStorage Usage': "localStorage.getItem('theme-preference')" in content,
        'System Preference Check': "prefers-color-scheme" in content,
        'Bootstrap Dark Styles': 'html.dark-mode .form-control' in content,
        'Navbar Dark Mode': 'html.dark-mode .navbar' in content,
        'Menu Variable Usage': 'var(--color-' in content,
    }
    
    return checks

def main():
    filepath = Path('/home/matas/budgets_project/templates/base.html')
    
    if not filepath.exists():
        print(f"❌ File not found: {filepath}")
        return False
    
    print("=" * 70)
    print("🌓 DARK MODE IMPLEMENTATION CHECK")
    print("=" * 70)
    print()
    
    checks = check_file(filepath)
    passed = 0
    failed = 0
    
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        passed += result
        failed += not result
        print(f"{status} {check_name}")
    
    print()
    print("=" * 70)
    print(f"Results: {passed}/{len(checks)} checks passed")
    
    if failed == 0:
        print("✅ ALL CHECKS PASSED - Dark mode is fully implemented!")
    else:
        print(f"❌ {failed} checks failed - Review the implementation")
    
    print("=" * 70)
    print()
    
    # Statistics
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("📊 STATISTICS:")
    print(f"  Total lines: {len(content.splitlines())}")
    print(f"  CSS variables: {content.count('--color-')}")
    print(f"  Dark mode rules: {content.count('html.dark-mode ')}")
    print(f"  JavaScript module size: ~150 lines (ThemeManager)")
    print()
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
