#!/usr/bin/env python3
"""
LG NJ Site - APPEND Additional Content
Adds MORE content to existing Learn More sections without replacing.
"""

import os
import re
from pathlib import Path

def generate_additional_content(appliance_type, city, county):
    """Generate ADDITIONAL content to append to existing Learn More"""

    county_name = county.replace('-', ' ').title()

    # Additional paragraphs to APPEND (not replace)
    additional = {
        'washer': f'''<p style="margin-bottom: 12px;"><strong>Advanced LG Washer Diagnostics in {city}:</strong> Our {county_name} technicians use LG's proprietary Smart Diagnosis technology, transmitting error data directly from your washer to our diagnostic systems. This allows us to identify problems before arriving at your {city} home, ensuring we bring the correct parts. We test motor windings for shorts, check capacitor values, and verify control board outputs with oscilloscopes when standard diagnostics aren't sufficient.</p>

<p style="margin-bottom: 12px;"><strong>{city} LG Washer Maintenance Tips:</strong> {county_name} water conditions affect washer performance. We recommend monthly tub clean cycles using LG's recommended cleaners to prevent odor-causing residue buildup common in {city} front-loaders. Check inlet hose screens quarterly—{county_name} water sediment clogs these filters. Leave doors ajar after cycles to dry gaskets and prevent mold growth. Our {city} technicians provide personalized maintenance schedules based on your household usage patterns and local water quality.</p>

<p style="margin-bottom: 12px;"><strong>Emergency Washer Service for {county_name}:</strong> Water leaks don't wait for business hours. Our {city} emergency response team is available for urgent LG washer repairs including burst hoses, pump failures causing flooding, and door seal ruptures. We've served {county_name} families during laundry emergencies for years, understanding that water damage compounds quickly. {city} homeowners receive priority response with our 24/7 emergency line.</p>''',

        'dryer': f'''<p style="margin-bottom: 12px;"><strong>LG Dryer Safety Inspections in {city}:</strong> Lint accumulation causes thousands of house fires annually. Our {county_name} technicians perform comprehensive safety inspections including internal lint pathway cleaning, exhaust duct inspection, and thermal limit testing. {city} homes with long duct runs require special attention—we measure actual airflow CFM to ensure safe operation. We've protected countless {county_name} families with thorough dryer safety assessments.</p>

<p style="margin-bottom: 12px;"><strong>{city} Dryer Efficiency Optimization:</strong> High energy bills often indicate dryer problems. Our {county_name} service includes efficiency testing—measuring actual drying times versus optimal performance. {city} customers with extended drying cycles typically have restricted airflow, failing heating elements, or sensor calibration issues. We restore factory efficiency levels, reducing utility costs for {county_name} households while extending appliance lifespan.</p>

<p style="margin-bottom: 12px;"><strong>LG Dryer Installation Verification for {county_name}:</strong> Improper installation causes many dryer problems. We verify {city} gas dryer connections meet code requirements, check electrical circuits for proper voltage, and ensure exhaust routing follows LG specifications. Many {county_name} service calls reveal installation deficiencies from previous contractors—we correct these issues preventing future breakdowns and ensuring {city} family safety.</p>''',

        'refrigerator': f'''<p style="margin-bottom: 12px;"><strong>LG Refrigerator Food Safety for {city} Families:</strong> Temperature fluctuations risk food spoilage and illness. Our {county_name} technicians verify your LG refrigerator maintains safe temperatures: below 40°F for fresh food, 0°F for freezer. We calibrate sensors, test defrost cycles, and ensure proper airflow throughout compartments. {city} families trust our thorough inspections protecting household health.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Refrigerator Energy Assessment:</strong> LG refrigerators should run 8-10 hours daily. Continuous operation indicates problems wasting electricity and wearing components. Our {city} technicians measure run cycles, check door seal integrity with dollar-bill tests, and verify condenser cleanliness. {county_name} customers typically see 15-25% energy reduction after our efficiency tune-ups.</p>

<p style="margin-bottom: 12px;"><strong>Smart Refrigerator Connectivity in {city}:</strong> LG ThinQ features let {county_name} homeowners monitor temperatures remotely, receive filter replacement alerts, and diagnose problems via smartphone. When connectivity fails, our {city} technicians troubleshoot WiFi modules, update firmware, and verify router compatibility. We've connected hundreds of {county_name} smart refrigerators, bringing modern convenience to {city} kitchens.</p>''',

        'oven': f'''<p style="margin-bottom: 12px;"><strong>LG Oven Calibration for {city} Home Cooks:</strong> Recipes fail when ovens run hot or cold. Our {county_name} technicians use laboratory-grade thermometers to verify actual versus displayed temperatures at multiple points. We calibrate LG oven sensors ensuring {city} bakers achieve consistent results. Many {county_name} customers discover 25-50°F discrepancies affecting their cooking—we restore factory accuracy.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Gas Range Safety Inspection:</strong> Gas appliances require annual safety checks. Our {city} technicians test for gas leaks using electronic detectors, verify burner combustion produces proper blue flames, and check safety valve response times. {county_name} families trust our comprehensive inspections meeting insurance and code requirements. We've identified dangerous conditions in {city} homes before problems occurred.</p>

<p style="margin-bottom: 12px;"><strong>LG Oven Self-Clean System Service in {city}:</strong> Self-clean cycles reach 900°F, stressing components. Our {county_name} technicians verify door lock mechanisms engage properly, temperature limits function correctly, and oven cavities have no grease accumulation risking fires. {city} homeowners using self-clean features benefit from our pre-cycle inspections ensuring safe operation throughout {county_name}.</p>''',

        'dishwasher': f'''<p style="margin-bottom: 12px;"><strong>LG Dishwasher Water Efficiency in {city}:</strong> Modern LG dishwashers use 3-4 gallons per cycle—less than hand washing. When water consumption increases, our {county_name} technicians diagnose fill valve issues, float switch problems, and cycle logic errors. {city} customers concerned about utility bills trust our efficiency assessments restoring optimal water usage for {county_name} households.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Hard Water Solutions:</strong> {city} water conditions affect dishwasher performance and lifespan. We remove mineral deposits from spray arms, clean heating elements, and treat door gaskets. Our {county_name} technicians recommend appropriate water softening for {city} homes experiencing spotty dishes, reduced cleaning power, and premature component wear from hard water damage.</p>

<p style="margin-bottom: 12px;"><strong>LG Dishwasher Installation Verification for {city}:</strong> Improper installation causes drainage issues, leaks, and poor cleaning. Our {county_name} technicians verify air gap or high loop configurations, check supply line connections, and ensure proper leveling. Many {city} service calls reveal installation deficiencies—we correct these issues preventing future problems for {county_name} homeowners.</p>''',

        'microwave': f'''<p style="margin-bottom: 12px;"><strong>Microwave Radiation Safety Testing in {city}:</strong> Damaged door seals can leak radiation. Our {county_name} technicians test every LG microwave repair with certified radiation detection equipment, verifying emissions stay well below FDA limits. {city} families trust our safety-first approach—we never return a microwave to service without confirmed safe operation protecting {county_name} households.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Microwave Ventilation Assessment:</strong> Over-the-range microwaves must properly ventilate cooking fumes. Our {city} technicians measure exhaust CFM, verify damper operation, and check filter conditions. Many {county_name} homes have inadequate kitchen ventilation—we optimize LG microwave settings and recommend solutions improving {city} indoor air quality.</p>

<p style="margin-bottom: 12px;"><strong>LG Microwave Power Output Testing for {city}:</strong> Weak heating often precedes complete failure. Our {county_name} technicians measure actual wattage output using water temperature tests, diagnosing magnetron degradation before total breakdown. {city} customers receive advance warning of impending failures, allowing planned replacement rather than emergency service disrupting {county_name} meal preparation.</p>''',

        'freezer': f'''<p style="margin-bottom: 12px;"><strong>LG Freezer Food Protection for {city} Families:</strong> Freezer failures risk hundreds of dollars in food loss. Our {county_name} technicians perform preventive inspections identifying early warning signs: unusual sounds, frost patterns, and temperature variations. {city} homeowners protecting bulk food purchases and meal preps trust our thorough assessments preventing costly losses throughout {county_name}.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Freezer Organization Consultation:</strong> Proper loading improves freezer efficiency and food quality. Our {city} technicians advise on airflow optimization, recommend storage containers, and identify overloading affecting performance. {county_name} families receiving our organization guidance report better food preservation and lower energy consumption in their {city} homes.</p>

<p style="margin-bottom: 12px;"><strong>Emergency Freezer Service for {city}:</strong> When freezers fail, food spoils quickly. Our {county_name} emergency response prioritizes freezer calls—we understand {city} families' concerns about food safety and financial loss. We've saved countless {county_name} food supplies with rapid response, often completing repairs before significant thawing occurs.</p>''',

        'cooktop': f'''<p style="margin-bottom: 12px;"><strong>LG Induction Cooktop Diagnostics in {city}:</strong> Induction technology requires compatible cookware—we help {county_name} customers identify suitable pots and pans. Our {city} technicians test magnetic field generation, verify pan detection sensitivity, and calibrate power delivery. Many {county_name} induction issues stem from cookware incompatibility rather than appliance failure.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Gas Cooktop Carbon Monoxide Testing:</strong> Improperly adjusted gas burners produce dangerous carbon monoxide. Our {city} technicians test combustion products, adjust air-fuel mixtures, and verify proper flame characteristics. {county_name} family safety depends on correct gas appliance operation—we ensure {city} cooktops burn cleanly and efficiently.</p>

<p style="margin-bottom: 12px;"><strong>Glass Cooktop Care for {city} Homeowners:</strong> Scratches and stains affect cooktop appearance and function. Our {county_name} technicians recommend proper cleaning products, identify scratch-causing cookware, and treat stubborn stains. {city} customers maintaining glass cooktops properly enjoy longer service life and better resale value for {county_name} homes.</p>''',

        'vent-hood': f'''<p style="margin-bottom: 12px;"><strong>Kitchen Ventilation Assessment for {city} Homes:</strong> Proper ventilation protects {county_name} indoor air quality and prevents grease accumulation. Our {city} technicians measure actual CFM airflow, compare against range BTU requirements, and identify restrictions. Many {county_name} kitchens have undersized or poorly installed ventilation—we recommend solutions improving {city} cooking environments.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Range Hood Noise Diagnosis:</strong> Excessive noise indicates bearing wear, blade imbalance, or motor problems. Our {city} technicians identify noise sources, measure decibel levels, and restore quiet operation {county_name} homeowners expect. We've quieted countless {city} kitchens, making cooking more enjoyable throughout {county_name}.</p>

<p style="margin-bottom: 12px;"><strong>Fire Prevention Service for {city} Kitchens:</strong> Grease-laden range hoods create fire hazards. Our {county_name} technicians provide deep cleaning services, replacing saturated filters and degreasing internal components. {city} homeowners cooking frequently should schedule annual professional cleaning protecting {county_name} families and homes from kitchen fires.</p>''',

        'wine-cooler': f'''<p style="margin-bottom: 12px;"><strong>Wine Collection Protection for {city} Enthusiasts:</strong> Temperature stability is critical—even brief fluctuations damage wine. Our {county_name} technicians install temperature monitoring during service, minimizing door-open time protecting {city} collections. We understand {county_name} wine investments and treat every bottle with appropriate care.</p>

<p style="margin-bottom: 12px;"><strong>{county_name} Wine Storage Consultation:</strong> Optimal wine storage extends beyond temperature. Our {city} technicians advise on humidity control, vibration reduction, and light protection. {county_name} collectors receiving our guidance report improved wine aging and better preservation of valuable bottles in {city} homes.</p>

<p style="margin-bottom: 12px;"><strong>Wine Cooler Placement Optimization for {city}:</strong> Location affects performance and efficiency. Our {county_name} technicians evaluate installation sites, recommend proper clearances, and identify environmental factors affecting operation. Many {city} wine cooler problems stem from poor placement—we optimize installations throughout {county_name} for reliable long-term performance.</p>'''
    }

    return additional.get(appliance_type, '')

APPLIANCE_SLUG_MAP = {
    'refrigerator-repair': 'refrigerator',
    'washer-repair': 'washer',
    'dryer-repair': 'dryer',
    'oven-repair': 'oven',
    'dishwasher-repair': 'dishwasher',
    'microwave-repair': 'microwave',
    'freezer-repair': 'freezer',
    'cooktop-repair': 'cooktop',
    'vent-hood-repair': 'vent-hood',
    'wine-cooler-repair': 'wine-cooler'
}

def title_case(slug):
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())

def update_service_page(filepath):
    """APPEND additional content to existing Learn More sections"""
    parts = str(filepath).split('/')

    county_slug = None
    city_slug = None

    for i, part in enumerate(parts):
        if part.endswith('-county'):
            county_slug = part
            if i + 1 < len(parts) and parts[i + 1] not in APPLIANCE_SLUG_MAP:
                city_slug = parts[i + 1]
            break

    if not county_slug or not city_slug:
        return False

    city_name = title_case(city_slug)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    updated = False
    for appliance_type in APPLIANCE_SLUG_MAP.values():
        additional_content = generate_additional_content(appliance_type, city_name, county_slug)

        if not additional_content:
            continue

        # Find the LAST </p> before </div> in the expandable-text section and append after it
        # Pattern: find the expandable text div content and append before closing
        pattern = rf'(<div id="expandable-text-{appliance_type}"[^>]*>)(.*?)(</div>\s*<div id="expandable-fade-{appliance_type}")'

        match = re.search(pattern, html, re.DOTALL)
        if match:
            existing_content = match.group(2)
            # Append new content after existing
            new_content = existing_content.rstrip() + '\n                                ' + additional_content + '\n                            '
            html = html[:match.start(2)] + new_content + html[match.end(2):]
            updated = True

    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True

    return False

def main():
    base_path = Path('/Users/globalaffiliate/lg-appliance-repair-nj')
    counties = [d for d in base_path.iterdir() if d.is_dir() and d.name.endswith('-county')]

    total_updated = 0

    for county_dir in sorted(counties):
        print(f"\nProcessing {county_dir.name}...")

        for city_dir in county_dir.iterdir():
            if not city_dir.is_dir():
                continue

            for service_dir in city_dir.iterdir():
                if not service_dir.is_dir() or service_dir.name not in APPLIANCE_SLUG_MAP:
                    continue

                index_file = service_dir / 'index.html'
                if index_file.exists():
                    try:
                        if update_service_page(index_file):
                            total_updated += 1
                            if total_updated % 100 == 0:
                                print(f"  Updated {total_updated} pages...")
                    except Exception as e:
                        print(f"  Error: {index_file}: {e}")

    print(f"\n{'='*50}")
    print(f"COMPLETE: Appended content to {total_updated} pages")
    print(f"Added ~150 more words per appliance card")
    print(f"Total now ~400-450 words per card")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
