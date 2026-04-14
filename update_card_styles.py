#!/usr/bin/env python3
"""
Update LG NJ site card styles to match Texas site:
- Add border/frame to cards
- Blue gradient button style for h3 titles
"""

import os
import re
from pathlib import Path

def update_styles(filepath):
    """Update CSS styles in HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    updated = False

    # 1. Update .service { } to add border
    old_service = '''.service {
            height: 100%;
            background: white;
            padding: 40px 35px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: all .4s ease;
            position: relative;
            cursor: pointer;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            min-height: 280px;
        }'''

    new_service = '''.service {
            height: 100%;
            background: white;
            padding: 25px 20px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: all .4s ease;
            position: relative;
            cursor: pointer;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            min-height: 280px;
        }'''

    if old_service in html:
        html = html.replace(old_service, new_service)
        updated = True

    # 2. Update .service h3 { } to blue gradient button style
    old_h3 = '''.service h3 {
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }'''

    new_h3 = '''.service h3 {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--blue) 0%, #2d2d4a 100%);
            color: white;
            padding: 14px 18px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 16px;
            margin-top: 15px;
            min-height: 50px;
            text-align: center;
            line-height: 1.3;
            transition: all .3s;
        }
        .service h3:hover {
            background: linear-gradient(135deg, var(--red) 0%, #a01830 100%);
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(196, 30, 58, 0.4);
        }'''

    if old_h3 in html:
        html = html.replace(old_h3, new_h3)
        updated = True

    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True

    return False

def main():
    base_path = Path('/Users/globalaffiliate/lg-appliance-repair-nj')

    total_updated = 0

    # Process all county directories
    for county_dir in sorted(base_path.iterdir()):
        if not county_dir.is_dir() or not county_dir.name.endswith('-county'):
            continue

        print(f"Processing {county_dir.name}...")

        for city_dir in county_dir.iterdir():
            if not city_dir.is_dir():
                continue

            # City landing page
            city_index = city_dir / 'index.html'
            if city_index.exists():
                try:
                    if update_styles(city_index):
                        total_updated += 1
                except Exception as e:
                    print(f"  Error: {city_index}: {e}")

            # Service pages
            for service_dir in city_dir.iterdir():
                if not service_dir.is_dir():
                    continue

                index_file = service_dir / 'index.html'
                if index_file.exists():
                    try:
                        if update_styles(index_file):
                            total_updated += 1
                            if total_updated % 500 == 0:
                                print(f"  Updated {total_updated} pages...")
                    except Exception as e:
                        print(f"  Error: {index_file}: {e}")

    print(f"\n{'='*50}")
    print(f"COMPLETE: Updated card styles on {total_updated} pages")
    print(f"- Added border frame to cards")
    print(f"- Blue gradient button style for h3 titles")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
