#!/usr/bin/env python3
"""
Fix missing expanded content for fridge, hood, wine cards
"""

import os
import re
from pathlib import Path

def generate_content(card_id, city, county):
    county_name = county.replace('-', ' ').title()

    content = {
        'fridge': f'''Our factory-certified technicians specialize in <strong>LG refrigerator repair</strong> across {city} and {county_name}. LG refrigeration systems feature LinearCooling compressor technology that maintains temperature within ±0.5°F—{city} homeowners depend on this precision for food safety. Our {county_name} service team completes annual LG certification to diagnose these advanced compressors.

We service InstaView Door-in-Door panels throughout {city}, including knock-to-illuminate LED systems and ThinQ camera modules letting {county_name} residents see inside their refrigerator remotely. Craft Ice maker repairs for {city} customers address slow freeze cycles, ice sphere ejector mechanisms, and water filtration issues affecting ice clarity.

{county_name} sealed system repairs include refrigerant recharge after leak detection, evaporator fan motor replacement when {city} homeowners hear clicking sounds, and condenser coil cleaning for optimal performance in New Jersey humidity. We service adaptive defrost systems that intelligently manage cycles based on {city} household usage patterns.

Door Cooling+ vents popular in {city} homes receive inspection for airflow obstructions and damper motor operation. We resolve temperature inconsistencies, frost buildup from defrost failures, and water leaks from clogged drain lines common in {county_name} homes. French door models throughout {city} with freezer drawer ice makers require special attention to water line routing. Our {county_name} technicians carry genuine LG thermistors, fans, and control boards for same-day repair.

<strong>LG Refrigerator Food Safety for {city} Families:</strong> Temperature fluctuations risk food spoilage and illness. Our {county_name} technicians verify your LG refrigerator maintains safe temperatures: below 40°F for fresh food, 0°F for freezer. We calibrate sensors, test defrost cycles, and ensure proper airflow throughout compartments. {city} families trust our thorough inspections protecting household health.

<strong>{county_name} Refrigerator Energy Assessment:</strong> LG refrigerators should run 8-10 hours daily. Continuous operation indicates problems wasting electricity and wearing components. Our {city} technicians measure run cycles, check door seal integrity with dollar-bill tests, and verify condenser cleanliness. {county_name} customers typically see 15-25% energy reduction after our efficiency tune-ups.''',

        'hood': f'''Our technicians deliver expert <strong>LG range hood repair</strong> in {city} and {county_name}. Kitchen ventilation removes odors, grease, smoke, and excess heat—{city} home cooks depend on proper airflow. We service fan motors, speed circuits, and blower assemblies restoring ventilation {county_name} kitchens need.

LED lighting illuminating {city} cooking surfaces receives board replacement when flickering occurs. {county_name} customers with older halogen models receive proper bulb matching. Touch controls are diagnosed for membrane failures affecting speed selection.

We repair fan motors running slowly or making grinding noises indicating bearing wear common in busy {city} kitchens, weak airflow from blower damage, and lighting issues. CFM airflow measurement ensures {county_name} hoods adequately ventilate based on range BTU output.

Mesh filter cleaning prevents grease buildup creating fire hazards in {city} homes. Charcoal filters for recirculating {county_name} installations ensure odor removal. Ducted systems receive airflow inspection and backdraft damper testing preventing outside air entry. Delay shut-off and heat-activated operation are restored for {city} convenience. Wall-mount, under-cabinet, and island configurations throughout {county_name} receive expert service.

<strong>Kitchen Ventilation Assessment for {city} Homes:</strong> Proper ventilation protects {county_name} indoor air quality and prevents grease accumulation. Our {city} technicians measure actual CFM airflow, compare against range BTU requirements, and identify restrictions. Many {county_name} kitchens have undersized or poorly installed ventilation—we recommend solutions improving {city} cooking environments.

<strong>{county_name} Range Hood Noise Diagnosis:</strong> Excessive noise indicates bearing wear, blade imbalance, or motor problems. Our {city} technicians identify noise sources, measure decibel levels, and restore quiet operation {county_name} homeowners expect.''',

        'wine': f'''Specialized <strong>LG wine cooler repair</strong> service throughout {city} and {county_name}. Wine storage requires precise 45-65°F temperature control—{city} wine collectors trust our thermoelectric and compressor system expertise. Proper storage preserves flavor profiles {county_name} enthusiasts value.

Dual-zone models popular in {city} homes receive individual thermistor calibration, damper adjustment between zones, and fan motor service. {county_name} collectors storing red wines at 55-65°F and whites at 45-55°F need independent climate control we expertly maintain.

We repair compressor failures endangering {city} wine collections, thermoelectric module replacements for silent operation preferred in {county_name} living spaces, and fan motor issues affecting temperature consistency throughout cabinets.

Door gasket inspection ensures proper sealing maintaining 50-80% humidity protecting corks in {city} collections from drying. UV-protected glass doors prevent light damage {county_name} wine enthusiasts avoid. We verify proper rack tilt keeping corks moist. Temperature fluctuations, lighting failures, and vibration issues affecting sediment are resolved for {city} collectors. Condenser cleaning and ventilation guidance ensure heat dissipation protecting {county_name} wine investments.

<strong>Wine Collection Protection for {city} Enthusiasts:</strong> Temperature stability is critical—even brief fluctuations damage wine. Our {county_name} technicians install temperature monitoring during service, minimizing door-open time protecting {city} collections. We understand {county_name} wine investments and treat every bottle with appropriate care.

<strong>{county_name} Wine Storage Consultation:</strong> Optimal wine storage extends beyond temperature. Our {city} technicians advise on humidity control, vibration reduction, and light protection. {county_name} collectors receiving our guidance report improved wine aging and better preservation of valuable bottles.'''
    }

    return content.get(card_id, '')

def title_case(slug):
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())

def update_page(filepath):
    parts = str(filepath).split('/')

    county_slug = None
    city_slug = None

    for i, part in enumerate(parts):
        if part.endswith('-county'):
            county_slug = part
            if i + 1 < len(parts):
                city_slug = parts[i + 1]
            break

    if not county_slug or not city_slug:
        return False

    city_name = title_case(city_slug)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    updated = False

    for card_id in ['fridge', 'hood', 'wine']:
        new_content = generate_content(card_id, city_name, county_slug)
        if not new_content:
            continue

        # Convert to HTML paragraphs
        paragraphs = new_content.strip().split('\n\n')
        html_content = '\n                                '.join([
            f'<p style="margin-bottom: 12px;">{p.strip()}</p>' for p in paragraphs
        ])

        # Replace existing content
        pattern = rf'(<div id="expandable-text-{card_id}"[^>]*>)\s*<p[^>]*>.*?</p>(\s*</div>\s*<div id="expandable-fade-{card_id}")'

        if re.search(pattern, html, re.DOTALL):
            replacement = f'\\1\n                                {html_content}\n                            \\2'
            html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)
            updated = True

    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True

    return False

def main():
    base_path = Path('/Users/globalaffiliate/lg-appliance-repair-nj')

    service_types = ['refrigerator-repair', 'washer-repair', 'dryer-repair', 'oven-repair',
                     'dishwasher-repair', 'microwave-repair', 'freezer-repair', 'cooktop-repair',
                     'vent-hood-repair', 'wine-cooler-repair']

    total_updated = 0

    for county_dir in sorted(base_path.iterdir()):
        if not county_dir.is_dir() or not county_dir.name.endswith('-county'):
            continue

        print(f"Processing {county_dir.name}...")

        for city_dir in county_dir.iterdir():
            if not city_dir.is_dir():
                continue

            # Update city landing page
            city_index = city_dir / 'index.html'
            if city_index.exists():
                try:
                    if update_page(city_index):
                        total_updated += 1
                except Exception as e:
                    print(f"  Error: {city_index}: {e}")

            # Update service pages
            for service_dir in city_dir.iterdir():
                if not service_dir.is_dir() or service_dir.name not in service_types:
                    continue

                index_file = service_dir / 'index.html'
                if index_file.exists():
                    try:
                        if update_page(index_file):
                            total_updated += 1
                            if total_updated % 500 == 0:
                                print(f"  Updated {total_updated} pages...")
                    except Exception as e:
                        print(f"  Error: {index_file}: {e}")

    print(f"\n{'='*50}")
    print(f"COMPLETE: Updated fridge/hood/wine content on {total_updated} pages")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
