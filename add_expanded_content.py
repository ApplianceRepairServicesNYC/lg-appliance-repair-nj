#!/usr/bin/env python3
"""
LG NJ Site Expanded Content Generator
Adds ~250-300 words to each appliance card's Learn More section.
Content is unique to BOTH appliance type AND city/county location.
"""

import os
import re
from pathlib import Path

def generate_content(appliance_type, city, county):
    """Generate unique content specific to appliance AND location"""

    county_name = county.replace('-', ' ').title()

    content = {
        'washer': f'''Our factory-certified technicians provide comprehensive <strong>LG washer repair</strong> throughout {city}, NJ. Serving {county_name} residents, we diagnose direct drive motor assemblies, including rotor position sensors, stator coil resistance, and hall effect sensors that other technicians often miss. {city} homeowners trust us for LG TurboWash 360 repairs requiring specialized knowledge of spray jet nozzles, recirculation pumps, and AI DD fabric detection sensors.

Common repairs for {city} customers include tub bearing replacement with proper spider arm inspection, door boot seal installation to prevent water leaks damaging {county_name} home floors, and drain pump motor service when your washer won't empty. We stock genuine LG control boards for ThinQ connectivity issues affecting smart home setups throughout {city}. Our {county_name} technicians specialize in fixing washers that vibrate excessively, indicating worn shock absorbers or suspension rods.

{city} families rely on LG steam cleaning technology for sanitizing fabrics. When steam functions fail, we diagnose steam generators, water inlet valves, and heating elements. We repair lid lock mechanisms on top-load models popular in {county_name} homes, water level pressure switches, and inlet valve screens clogged with {city} hard water sediment.

Whether your LG washer displays UE, OE, or LE error codes, won't spin, makes grinding noises, or fails to drain, our {county_name} service team arrives equipped with authentic LG components for same-day resolution. {city} residents receive priority scheduling with fully-stocked service vehicles carrying pumps, motors, bearings, and electronic boards. We understand the laundry demands of {county_name} households and respond accordingly.''',

        'dryer': f'''Professional <strong>LG dryer repair</strong> service for {city} residents and all of {county_name}. Our technicians specialize in LG heat pump dryers using refrigerant-based technology requiring EPA certification. These energy-efficient models popular in {city} eco-conscious homes recycle heat rather than venting it, but their compressors and condensers require expert service.

For gas LG dryers common throughout {county_name}, we test igniter glow bar resistance, gas valve coil continuity, and flame sensor operation. {city} homeowners with electric models receive heating element continuity tests, high-limit thermostat verification, and thermal fuse diagnostics. Our {county_name} technicians understand local electrical systems and gas line configurations.

LG TurboSteam technology is popular among {city} families for wrinkle reduction. We service steam generators and water inlet valves. {county_name} customers frequently call us for Sensor Dry calibration when clothes emerge damp, drum roller bearing failures causing squeaking, and belt tensioner problems. Our {city} service area coverage ensures fast response.

Ventless dryers gaining popularity in {city} apartments receive specialized attention including condenser coil cleaning, water tank drainage repair, and heat exchanger maintenance. We address lint buildup reducing efficiency in {county_name} homes. Common error codes like d80 and Flow Sense alerts indicate airflow restrictions we quickly resolve for {city} customers with proper vent inspection and cleaning services.''',

        'refrigerator': f'''Our factory-certified technicians specialize in <strong>LG refrigerator repair</strong> across {city} and {county_name}. LG LinearCooling compressor technology maintains temperature within ±0.5°F—{city} homeowners depend on this precision for food safety. Our {county_name} service team completes annual LG certification to diagnose these advanced compressors.

We service InstaView Door-in-Door panels throughout {city}, including knock-to-illuminate LED systems and ThinQ camera modules letting {county_name} residents see inside their refrigerator remotely. Craft Ice maker repairs for {city} customers address slow freeze cycles, ice sphere ejector mechanisms, and water filtration issues affecting ice clarity.

{county_name} sealed system repairs include refrigerant recharge after leak detection, evaporator fan motor replacement when {city} homeowners hear clicking sounds, and condenser coil cleaning for optimal performance in New Jersey humidity. We service adaptive defrost systems that intelligently manage cycles based on {city} household usage patterns.

Door Cooling+ vents popular in {city} homes receive inspection for airflow obstructions and damper motor operation. We resolve temperature inconsistencies, frost buildup from defrost failures, and water leaks from clogged drain lines common in {county_name} homes. French door models throughout {city} with freezer drawer ice makers require special attention to water line routing. Our {county_name} technicians carry genuine LG thermistors, fans, and control boards for same-day repair.''',

        'oven': f'''Our technicians deliver expert <strong>LG oven repair</strong> throughout {city} and {county_name}. LG ProBake Convection technology places heating elements at the rear for even baking—{city} home cooks depend on this for perfect results. We diagnose rear elements, convection fan motors, and temperature sensors with precision equipment trusted throughout {county_name}.

For LG gas ranges popular in {city} homes, we service sealed burner ignition systems, spark modules, and gas valve functionality. {county_name} safety is our priority—we verify safety valve response times and calibrate flames for proper blue color indicating complete combustion safe for {city} families.

EasyClean oven technology helps busy {city} households maintain spotless interiors. We verify cleaning temperature accuracy and door lock mechanisms. InstaView window models throughout {county_name} receive heating element inspection for knock-to-see features. {city} customers appreciate our expertise with triple-pane glass panel service.

We repair bake element failures affecting {city} family meals, broil element burnouts, and temperature sensor drift causing overcooking or undercooking frustrating {county_name} cooks. Control board malfunctions and door switch issues are quickly resolved for {city} residents. Slide-in, freestanding, and double oven configurations throughout {county_name} receive comprehensive diagnosis with proper igniter amperage, element resistance, and sensor testing.''',

        'dishwasher': f'''Factory-certified <strong>LG dishwasher repair</strong> service throughout {city} and {county_name}. LG QuadWash technology features four spray arms with multi-motion cleaning—{city} households trust this thorough cleaning system. Our {county_name} technicians service rotation motors, nozzle assemblies, and water pressure systems unique to LG.

TrueSteam dishwashers popular among {city} families require specialized diagnosis of steam generators producing sanitizing temperatures. {county_name} customers with hygiene concerns rely on our expertise with these high-temperature systems exceeding 160°F.

We repair drain pump failures leaving standing water frustrating {city} homeowners, wash impeller damage reducing cleaning performance, and spray arm bearing issues. Dynamic Dry systems in {county_name} homes receive inspection of automatic door-opening mechanisms releasing steam for spot-free drying {city} families expect.

Common repairs for {city} customers include door latch assemblies, detergent dispenser motors, and float switch calibration preventing overfill or underfill conditions. {county_name} homes with hard water often experience inlet valve issues we quickly resolve. Turbidity sensors measuring water cleanliness, door gasket leaks, and filtration system maintenance keep {city} dishwashers running efficiently. Our {county_name} service vehicles carry genuine LG components for same-day repair.''',

        'microwave': f'''Our technicians provide safe, professional <strong>LG microwave repair</strong> in {city} and throughout {county_name}. Microwave repairs involve high-voltage components—{city} residents trust our strict safety protocols including proper capacitor discharge before any service. Our {county_name} team is trained in magnetron testing and high-voltage diode diagnostics.

LG Smart Inverter technology provides precise power control popular in {city} kitchens—we diagnose inverter circuit boards and control logic failures. {county_name} home cooks appreciate true power adjustment for delicate foods rather than simple on/off cycling.

Over-the-range LG microwaves throughout {city} receive exhaust fan service for proper stovetop ventilation, charcoal filter guidance, and cooktop lighting repair. {county_name} kitchen air quality depends on proper ventilation we ensure with professional service.

We repair magnetron failures causing no-heat conditions frustrating {city} families, turntable motor issues, and door switches preventing operation. {county_name} customers with unresponsive touchpads or SmoothTouch controls trust our diagnostic expertise. Sensor Cook features automatically adjusting time based on food moisture are restored for {city} convenience. We address sparking from damaged waveguide covers and door seal issues important for {county_name} family safety.''',

        'freezer': f'''Expert <strong>LG freezer repair</strong> service throughout {city} and {county_name}. Our EPA-certified technicians handle sealed system repairs requiring refrigerant recovery—{city} homeowners trust our specialized compressor diagnostics. Freezer systems operate at lower temperatures requiring precise refrigerant charges our {county_name} team expertly manages.

LG LinearCooling maintains consistent temperatures {city} families depend on for food preservation. We diagnose compressor start relay failures causing clicking sounds, overload protectors, and inverter boards. {county_name} customers receive expert service on these unique linear compressor systems.

Defrost system repairs for {city} freezers include heater testing, timer verification, and adaptive defrost boards learning {county_name} household usage patterns. Failed defrost causes frost buildup blocking airflow—we quickly resolve this for {city} residents.

We fix frost buildup, temperature fluctuations from damaged door gaskets allowing {county_name} humid air infiltration, and ice maker failures including fill tube freeze-ups. Evaporator fan replacements restore circulation when {city} freezer contents thaw unexpectedly. Condenser cleaning improves efficiency for {county_name} homes. ThinQ connectivity, temperature sensors, and door alarms are serviced with genuine LG components for {city} customers.''',

        'cooktop': f'''Professional <strong>LG cooktop repair</strong> throughout {city} and {county_name}. LG induction cooktops require specialized electromagnetic knowledge—{city} modern kitchens feature these efficient units heating cookware directly while surfaces stay cool. Our {county_name} technicians diagnose induction coils, power modules, and pan detection sensors.

Radiant electric cooktops throughout {city} receive element continuity testing, infinite switch diagnostics, and glass surface inspection. {county_name} electrical systems require technicians who understand proper resistance measurements and safety protocols we strictly follow.

LG gas cooktops popular in {city} homes feature sealed burners with individual igniters. We service spark modules, burner cap alignment for proper {county_name} flame distribution, and gas port cleaning. Safety valves protecting {city} families are thoroughly tested.

We repair burners that won't ignite frustrating {city} cooks, inconsistent heat from failing switches, and touch control malfunctions. Cracked glass surfaces require careful replacement maintaining seals protecting {county_name} home electrical components. Simmer burner adjustments for {city} gourmet cooking, power boost repairs for rapid boiling, and bridge element service for large cookware are completed with genuine LG parts.''',

        'vent-hood': f'''Our technicians deliver expert <strong>LG range hood repair</strong> in {city} and {county_name}. Kitchen ventilation removes odors, grease, smoke, and excess heat—{city} home cooks depend on proper airflow. We service fan motors, speed circuits, and blower assemblies restoring ventilation {county_name} kitchens need.

LED lighting illuminating {city} cooking surfaces receives board replacement when flickering occurs. {county_name} customers with older halogen models receive proper bulb matching. Touch controls are diagnosed for membrane failures affecting speed selection.

We repair fan motors running slowly or making grinding noises indicating bearing wear common in busy {city} kitchens, weak airflow from blower damage, and lighting issues. CFM airflow measurement ensures {county_name} hoods adequately ventilate based on range BTU output.

Mesh filter cleaning prevents grease buildup creating fire hazards in {city} homes. Charcoal filters for recirculating {county_name} installations ensure odor removal. Ducted systems receive airflow inspection and backdraft damper testing preventing outside air entry. Delay shut-off and heat-activated operation are restored for {city} convenience. Wall-mount, under-cabinet, and island configurations throughout {county_name} receive expert service.''',

        'wine-cooler': f'''Specialized <strong>LG wine cooler repair</strong> service throughout {city} and {county_name}. Wine storage requires precise 45-65°F temperature control—{city} wine collectors trust our thermoelectric and compressor system expertise. Proper storage preserves flavor profiles {county_name} enthusiasts value.

Dual-zone models popular in {city} homes receive individual thermistor calibration, damper adjustment between zones, and fan motor service. {county_name} collectors storing red wines at 55-65°F and whites at 45-55°F need independent climate control we expertly maintain.

We repair compressor failures endangering {city} wine collections, thermoelectric module replacements for silent operation preferred in {county_name} living spaces, and fan motor issues affecting temperature consistency throughout cabinets.

Door gasket inspection ensures proper sealing maintaining 50-80% humidity protecting corks in {city} collections from drying. UV-protected glass doors prevent light damage {county_name} wine enthusiasts avoid. We verify proper rack tilt keeping corks moist. Temperature fluctuations, lighting failures, and vibration issues affecting sediment are resolved for {city} collectors. Condenser cleaning and ventilation guidance ensure heat dissipation protecting {county_name} wine investments.'''
    }

    return content.get(appliance_type, '')

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

def title_case(slug):
    """Convert slug to title case"""
    return ' '.join(word.capitalize() for word in slug.replace('-', ' ').split())

def update_service_page(filepath):
    """Update Learn More sections with expanded location-specific content"""
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
            break

    if not all([county_slug, city_slug, service_slug]):
        return False

    city_name = title_case(city_slug)

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update each appliance card's Learn More section
    updated = False
    for appliance_type in APPLIANCE_SLUG_MAP.values():
        # Generate unique content for this appliance + location
        unique_content = generate_content(appliance_type, city_name, county_slug)

        if not unique_content:
            continue

        # Convert double newlines to separate paragraphs
        paragraphs = unique_content.strip().split('\n\n')
        html_paragraphs = '\n                                '.join([
            f'<p style="margin-bottom: 12px;">{p.strip()}</p>' for p in paragraphs
        ])

        # Pattern to find and replace the expandable text content
        pattern = rf'(<div id="expandable-text-{appliance_type}"[^>]*>)\s*(?:<p[^>]*>.*?</p>\s*)+'

        if re.search(pattern, html, re.DOTALL):
            replacement = f'\\1\n                                {html_paragraphs}\n                            '
            html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)
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
    print(f"COMPLETE: Updated {total_updated} service pages")
    print(f"Each page has ~250-300 words per appliance card")
    print(f"Content unique to appliance + city + county")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
