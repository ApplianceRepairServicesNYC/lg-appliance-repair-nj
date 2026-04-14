#!/usr/bin/env python3
"""
LG NJ Site Unique Content Generator
Adds unique, non-plagiarized content ONLY to the Learn More/Show More
expandable sections of each appliance card.
Does NOT modify the main intro paragraph or template structure.
"""

import os
import re
from pathlib import Path

# Unique Learn More content for each appliance type - 100% original
APPLIANCE_LEARN_MORE = {
    'washer': '''Our factory-certified technicians provide comprehensive <strong>LG washer repair</strong> throughout {city}, NJ. We diagnose direct drive motor assemblies, including rotor position sensors, stator coil resistance, and hall effect sensors that other technicians often miss. LG TurboWash 360 systems require specialized knowledge of the spray jet nozzles, recirculation pumps, and AI DD fabric detection sensors. Common repairs include tub bearing replacement with proper spider arm inspection, door boot seal installation to prevent leaks, and drain pump motor service when your washer won't empty properly. We stock genuine LG control boards for ThinQ connectivity issues and motor control unit failures. Whether your LG washer displays error codes, won't spin, makes grinding noises during the wash cycle, or fails to drain completely, we arrive equipped with authentic LG components for same-day resolution.''',

    'dryer': '''Professional <strong>LG dryer repair</strong> service in {city} for gas and electric models. Our technicians specialize in LG heat pump dryers, which use refrigerant-based drying technology requiring EPA certification and specialized diagnostic equipment. For gas LG dryers, we test igniter glow bar resistance, gas valve coil continuity, and flame sensor operation using precise measurement tools. Electric models receive heating element continuity tests, high-limit thermostat verification, and thermal fuse diagnostics. LG TurboSteam technology requires proper steam generator and water inlet valve service. We diagnose Sensor Dry calibration issues when clothes emerge damp, drum roller bearing failures causing squeaking or thumping, and belt tensioner problems affecting rotation. Ventless and condenser dryer models receive specialized attention including condenser coil cleaning, water collection tank drainage system repair, and heat exchanger maintenance.''',

    'refrigerator': '''Our factory-certified technicians specialize in <strong>LG refrigerator repair</strong> across {city}, NJ. LG refrigeration systems feature LinearCooling compressor technology that maintains temperature within ±0.5°F—diagnosing these precision compressors requires specialized training we complete annually. We service InstaView Door-in-Door panels including the knock-to-illuminate LED system and interior camera modules for ThinQ app connectivity. Craft Ice maker repairs address the slow freeze cycle, ice sphere ejector mechanisms, and water filtration issues affecting ice clarity. Common sealed system repairs include refrigerant recharge after leak detection, evaporator fan motor replacement, and condenser coil cleaning for optimal heat dissipation. Door Cooling+ vents receive inspection for air flow obstructions and damper motor operation. We resolve temperature inconsistencies, frost buildup from defrost heater failures, water leaks from clogged drain lines, and ice maker malfunctions using genuine LG diagnostic procedures and factory components.''',

    'oven': '''Our technicians deliver expert <strong>LG oven repair</strong> throughout {city}, NJ. LG ProBake Convection technology places the heating element at the rear of the oven cavity for even heat distribution—we diagnose these rear elements, convection fan motors, and temperature sensor assemblies with precision testing equipment. For LG gas ranges, we service sealed burner ignition systems, spark module operation, gas valve functionality, and safety valve response times. EasyClean oven interiors require specific cleaning temperature verification and door lock mechanism service. InstaView window models receive heating element inspection for the knock-to-see feature and glass panel integrity checks. We repair bake element failures causing uneven cooking, broil element burnouts, oven temperature sensor drift requiring recalibration, control board malfunctions displaying error codes, and door switch issues preventing proper operation. Slide-in and freestanding range models all receive comprehensive diagnosis with genuine LG replacement parts.''',

    'dishwasher': '''Factory-certified <strong>LG dishwasher repair</strong> service throughout {city}, NJ. LG QuadWash technology features four spray arms with multi-motion cleaning patterns—our technicians service the rotation motors, nozzle assemblies, and water pressure regulation systems unique to this design. TrueSteam dishwashers require specialized diagnosis of the steam generator, water inlet valve operation, and condensation management systems. We repair drain pump motor failures preventing proper water removal, wash impeller damage reducing cleaning performance, and upper spray arm bearing issues causing rotation problems. Dynamic Dry systems receive inspection of the automatic door opening mechanism and ventilation fan operation. Common repairs include door latch assembly replacement, detergent dispenser motor service, float switch calibration for fill level issues, and control board diagnostics for error codes. Water inlet valve failures causing no-fill conditions and leak detection from worn door gaskets are resolved with genuine LG components.''',

    'microwave': '''Our technicians provide safe, professional <strong>LG microwave repair</strong> in {city}, NJ. Microwave repairs involve high-voltage components requiring strict safety protocols—our technicians are trained in proper capacitor discharge procedures, magnetron testing, and high-voltage diode diagnostics. LG Smart Inverter technology provides precise power control through variable wattage rather than on/off cycling—we diagnose inverter circuit boards, power transistors, and control logic failures. Over-the-range LG microwaves receive exhaust fan motor service, charcoal filter replacement guidance, and ventilation system diagnostics for proper kitchen air circulation. We repair magnetron failures causing no-heat conditions, turntable motor replacements for rotation issues, door switch assembly problems preventing operation, and touchpad membrane failures affecting control input. SmoothTouch glass panel controls and Sensor Cook features are diagnosed using LG technical procedures with genuine manufacturer components.''',

    'freezer': '''Expert <strong>LG freezer repair</strong> service throughout {city}, NJ. Our EPA-certified technicians handle sealed system repairs requiring refrigerant recovery equipment and specialized compressor diagnostics. LG LinearCooling technology maintains consistent freezing temperatures with minimal variation—we diagnose compressor start relay failures, overload protector issues, and inverter board malfunctions affecting this precision cooling. Defrost system repairs include defrost heater continuity testing, defrost timer advancement verification, adaptive defrost control board service, and bi-metal thermostat replacement. We resolve frost buildup from failed defrost cycles, temperature fluctuations from damaged door gaskets, and ice maker failures in freezer compartments. Evaporator fan motor replacements restore proper air circulation when contents thaw unexpectedly. Condenser coil cleaning improves efficiency when the compressor runs continuously. Smart ThinQ connectivity issues and temperature sensor calibration are completed with genuine LG diagnostic procedures.''',

    'cooktop': '''Professional <strong>LG cooktop repair</strong> throughout {city}, NJ. LG induction cooktops require specialized knowledge of electromagnetic heating—our technicians diagnose induction coils, power inverter modules, and magnetic pan detection sensors that must recognize cookware before heating activates. Radiant electric cooktops receive element continuity testing, infinite switch diagnostics for temperature control, and glass surface inspection for cracks or damage. LG gas cooktops feature sealed burner systems with individual igniters—we service spark modules, burner cap alignment, gas port cleaning, and safety valve operation. We repair burners that won't ignite, elements providing inconsistent heat, control knob failures, and touch control panel malfunctions. Cracked glass cooktop surfaces require careful replacement to maintain proper sealing. Simmer burner adjustments, power boost element repairs, and bridge element service for oversized cookware are completed with genuine LG components.''',

    'vent-hood': '''Our technicians deliver expert <strong>LG range hood repair</strong> in {city}, NJ. Kitchen ventilation is essential for removing cooking odors, grease particles, and excess heat—we service LG range hood fan motors, speed control circuits, and blower wheel assemblies to restore proper airflow. LED lighting systems receive board replacement when illumination fails, and halogen bulb service for older models. Touch control panels are diagnosed for membrane switch failures and control board malfunctions. We repair fan motors running slowly or making noise, ventilation reducing to weak airflow, and lighting that flickers or won't turn on. Mesh grease filter cleaning guidance and charcoal filter replacement for recirculating models ensure optimal air quality. Ducted installations receive inspection for proper airflow and backdraft damper operation. Delay shut-off features and automatic heat-activated operation are restored with genuine LG diagnostic procedures.''',

    'wine-cooler': '''Specialized <strong>LG wine cooler repair</strong> service throughout {city}, NJ. Wine storage requires precise temperature control—our technicians service both thermoelectric Peltier-based cooling and compressor refrigeration systems used in LG wine coolers. Dual-zone models with separate temperature controls for red and white wine receive individual thermistor calibration, damper door adjustment, and zone-specific fan motor service. We repair compressor failures causing temperature rise, thermoelectric module replacements for silent-operation coolers, and evaporator fan motor issues affecting air circulation. Door gasket inspection ensures proper sealing to maintain humidity levels that protect wine corks. UV-protected glass door components receive service for proper operation. We resolve temperature fluctuations, interior lighting failures, vibration issues affecting wine sediment, and digital display malfunctions. Condenser coil cleaning and proper ventilation clearance guidance are provided with all service calls.'''
}

# Map URL slugs to appliance card IDs
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

# Card ID mapping (how they appear in expandable-text-{id})
CARD_ID_MAP = {
    'refrigerator': 'refrigerator',
    'washer': 'washer',
    'dryer': 'dryer',
    'oven': 'oven',
    'dishwasher': 'dishwasher',
    'microwave': 'microwave',
    'freezer': 'freezer',
    'cooktop': 'cooktop',
    'vent-hood': 'vent-hood',
    'wine-cooler': 'wine-cooler'
}

def title_case(slug):
    """Convert slug to title case"""
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())

def update_service_page(filepath):
    """Update Learn More sections in a service page with unique content"""
    parts = str(filepath).split('/')

    # Find county, city, and service from path
    county_slug = None
    city_slug = None
    service_slug = None

    for i, part in enumerate(parts):
        if part.endswith('-county'):
            county_slug = part
            if i + 1 < len(parts) and parts[i + 1] not in APPLIANCE_SLUG_MAP:
                city_slug = parts[i + 1]
            if i + 2 < len(parts) and parts[i + 2] in APPLIANCE_SLUG_MAP:
                service_slug = parts[i + 2]
            elif i + 1 < len(parts) and parts[i + 1] in APPLIANCE_SLUG_MAP:
                service_slug = parts[i + 1]
            break

    if not all([county_slug, city_slug, service_slug]):
        return False

    if service_slug not in APPLIANCE_SLUG_MAP:
        return False

    city_name = title_case(city_slug)

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update each appliance card's Learn More section
    updated = False
    for appliance_type, content_template in APPLIANCE_LEARN_MORE.items():
        card_id = CARD_ID_MAP.get(appliance_type, appliance_type)

        # Format unique content with city name
        unique_content = content_template.format(city=city_name)

        # Pattern to find the expandable text div for this appliance card
        # Matches: <div id="expandable-text-washer" ...>...<p>...</p>...</div>
        pattern = rf'(<div id="expandable-text-{card_id}"[^>]*>)\s*<p[^>]*>.*?</p>'

        if re.search(pattern, html, re.DOTALL):
            replacement = f'\\1\n                                <p style="margin-bottom: 12px;">{unique_content}</p>'
            html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)
            updated = True

    if updated:
        # Write the updated file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True

    return False

def main():
    base_path = Path('/Users/globalaffiliate/lg-appliance-repair-nj')

    # Find all service pages (in city/service-repair/ directories)
    counties = [d for d in base_path.iterdir() if d.is_dir() and d.name.endswith('-county')]

    total_updated = 0
    total_skipped = 0

    for county_dir in sorted(counties):
        print(f"\nProcessing {county_dir.name}...")

        for city_dir in county_dir.iterdir():
            if not city_dir.is_dir():
                continue

            for service_dir in city_dir.iterdir():
                if not service_dir.is_dir():
                    continue

                if service_dir.name not in APPLIANCE_SLUG_MAP:
                    continue

                index_file = service_dir / 'index.html'
                if not index_file.exists():
                    continue

                try:
                    if update_service_page(index_file):
                        total_updated += 1
                        if total_updated % 100 == 0:
                            print(f"  Updated {total_updated} pages...")
                    else:
                        total_skipped += 1
                except Exception as e:
                    print(f"  Error updating {index_file}: {e}")
                    total_skipped += 1

    print(f"\n{'='*50}")
    print(f"COMPLETE: Updated {total_updated} service pages")
    print(f"Skipped: {total_skipped} pages")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
