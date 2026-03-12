#!/usr/bin/env python3
"""
Rewrite expandable content sections to make pages unique.
Keeps template/appearance identical, only changes text in Show More sections.
"""

import os
import re
import random
import csv

# Town-specific facts for New Jersey towns (sample - will generate variations)
TOWN_DETAILS = {
    "clinton-township": "nestled in the scenic Hunterdon County highlands",
    "tewksbury-township": "known for its historic farmland and equestrian properties",
    "ship-bottom": "located on Long Beach Island's barrier island",
    "bernardsville": "in the heart of the Somerset Hills",
    "burlington-township": "along the Delaware River corridor",
    "holmdel": "home to the famous PNC Bank Arts Center",
    "howell": "one of Monmouth County's largest townships",
    "beachwood": "situated along the Toms River waterfront",
    "beverly": "a historic riverfront community on the Delaware",
    "riverdale": "in the Pequannock River valley of Morris County",
    "chesterfield-township": "surrounded by preserved farmland",
    "woodstown": "the county seat of Salem County",
    "green-brook": "in the Watchung Mountains foothills",
    "east-windsor": "near the NJ Turnpike corridor",
    "south-brunswick": "a growing suburban community",
    "cedar-grove": "at the base of the First Watchung Mountain",
    "east-orange": "a diverse urban community in Essex County",
    "elk-township": "in rural Gloucester County",
    "cape-may-point": "at the southern tip of New Jersey",
    "sayreville": "along the Raritan River",
    "princeton": "home to the world-renowned university",
    "haddonfield": "with its historic downtown and Victorian homes",
    "hopatcong": "on the shores of Lake Hopatcong",
    "robbinsville-township": "in central Mercer County",
    "trenton": "the state capital of New Jersey",
    "piscataway": "home to Rutgers University",
    "union-city": "one of the most densely populated cities in America",
    "north-wildwood": "a popular Jersey Shore destination",
    "bloomfield": "a thriving Essex County community",
    "shrewsbury-township": "in historic Monmouth County",
    "pemberton-township": "surrounded by the Pine Barrens",
    "woodlynne": "a close-knit Camden County community",
    "guttenberg": "the most densely populated municipality in the US",
    "mendham-township": "in the rolling hills of Morris County",
    "east-brunswick": "a major Middlesex County suburb",
    "stanhope": "gateway to the Sussex County highlands",
    "asbury-park": "the revitalized Jersey Shore cultural hub",
    "gloucester-city": "along the Delaware River waterfront",
    "millstone": "in the rural heart of Monmouth County",
    "glassboro": "home to Rowan University",
    "jersey-city": "New Jersey's second-largest city",
    "west-caldwell": "a suburban Essex County community",
    "buena": "in the agricultural heart of Atlantic County",
    "hillside": "bordering Newark and Elizabeth",
    "haledon": "with views of the Passaic County highlands",
    "avon-by-the-sea": "a charming beachfront community",
    "eatontown": "near the Monmouth Mall area",
}

# Appliance-specific content variations
APPLIANCE_INTROS = {
    "freezer": [
        "A malfunctioning freezer puts your food supply at immediate risk. When ice crystals form incorrectly, temperatures fluctuate, or your unit stops cooling entirely, every hour counts.",
        "Your LG freezer works around the clock to protect your frozen goods. When problems arise—whether it's frost buildup, temperature inconsistencies, or unusual noises—prompt professional repair prevents costly food spoilage.",
        "Freezer failures demand immediate attention. From defrost system malfunctions to compressor issues, our technicians diagnose and resolve LG freezer problems to minimize food loss and restore reliable operation.",
    ],
    "refrigerator": [
        "Your refrigerator is the hardest-working appliance in your kitchen, running 24/7 to keep food fresh and safe. When cooling problems, water leaks, or ice maker issues occur, expert repair restores your kitchen's essential hub.",
        "A failing refrigerator affects your entire household. Whether you're dealing with inconsistent temperatures, a broken ice maker, or water pooling beneath the unit, our LG specialists deliver precise diagnostics and lasting repairs.",
        "From French door models to side-by-side units, LG refrigerators require specialized knowledge for proper repair. Our factory-trained technicians understand the unique systems in every LG refrigerator configuration.",
    ],
    "dishwasher": [
        "When your LG dishwasher leaves dishes dirty, won't drain, or displays error codes, hand-washing becomes an unwelcome chore. Our repair service restores the convenience your household depends on.",
        "Dishwasher problems range from simple filter clogs to complex control board failures. Our technicians carry diagnostic equipment to pinpoint issues and genuine LG parts to complete repairs in a single visit.",
        "A malfunctioning dishwasher disrupts your daily routine. Whether water isn't draining, spray arms aren't spinning, or the unit won't start, we provide same-day diagnosis and repair for all LG dishwasher models.",
    ],
    "washer": [
        "Laundry piles up fast when your washer breaks down. From drum bearing failures to drainage problems, our LG washer specialists restore your laundry routine with precision repairs backed by genuine parts.",
        "LG washers feature advanced technology that requires specialized repair knowledge. Whether you have a front-load, top-load, or combination unit, our factory-trained technicians diagnose and fix problems efficiently.",
        "When your LG washer vibrates excessively, won't spin, or leaves clothes wet, prompt repair prevents water damage and restores normal operation. Our technicians service all LG washer models and configurations.",
    ],
    "dryer": [
        "A dryer that won't heat, takes too long, or makes unusual noises needs immediate attention. Our LG dryer repair service addresses heating element failures, drum issues, and ventilation problems.",
        "Whether you have a gas or electric LG dryer, our technicians understand the specific repair requirements for each type. From igniter replacements to thermal fuse repairs, we restore efficient drying performance.",
        "Dryer problems often indicate safety concerns—blocked vents, failing heating elements, or worn drum components. Our technicians inspect, diagnose, and repair LG dryers to ensure safe, efficient operation.",
    ],
    "oven": [
        "An oven that won't heat properly, has inconsistent temperatures, or displays error codes disrupts meal preparation. Our LG oven repair service addresses heating elements, igniters, thermostats, and control systems.",
        "From convection systems to self-cleaning features, LG ovens incorporate sophisticated technology. Our factory-trained technicians diagnose and repair all oven functions to restore your cooking capabilities.",
        "Oven repairs require precision—temperature accuracy matters for everything you cook. Our technicians calibrate, repair, and test LG ovens to ensure consistent heating and reliable performance.",
    ],
    "cooktop": [
        "Whether you have a gas, electric, or induction LG cooktop, precise burner operation is essential for cooking. Our repair service addresses ignition problems, heating inconsistencies, and control malfunctions.",
        "Cooktop problems range from burners that won't ignite to touch controls that malfunction. Our technicians service all LG cooktop types, carrying the parts needed for common repairs.",
        "A cooktop with non-working burners limits your cooking options. Our LG cooktop repair service restores full functionality, whether you need igniter replacement, element repair, or control board service.",
    ],
    "microwave": [
        "When your LG microwave stops heating, displays error codes, or makes unusual sounds, our technicians provide expert diagnosis and repair. We service all LG microwave models including over-the-range and countertop units.",
        "Microwave repairs involve high-voltage components that require professional handling. Our factory-trained technicians safely diagnose and repair magnetrons, capacitors, door switches, and control panels.",
        "A microwave that runs but doesn't heat often indicates a magnetron or diode failure. Our technicians carry diagnostic equipment and genuine LG parts to restore proper microwave function.",
    ],
    "wine-cooler": [
        "LG wine coolers maintain precise temperatures to preserve your collection. When cooling becomes inconsistent, compressors fail, or temperature displays malfunction, our specialists protect your wine investment.",
        "Wine storage requires exact temperature control—fluctuations can damage your collection. Our LG wine cooler repair service addresses thermostat issues, compressor problems, and cooling inconsistencies.",
        "From dual-zone cooling failures to door seal problems, wine cooler issues threaten your collection. Our technicians diagnose and repair LG wine coolers to maintain optimal storage conditions.",
    ],
    "vent-hood": [
        "A properly functioning vent hood removes smoke, grease, and odors from your kitchen. When your LG vent hood stops exhausting, makes noise, or has lighting problems, our technicians restore clean air circulation.",
        "Vent hood repairs often involve motor replacement, fan blade service, or control panel diagnosis. Our technicians service all LG vent hood models including ducted and ductless configurations.",
        "Kitchen ventilation affects air quality throughout your home. Our LG vent hood repair service addresses exhaust problems, lighting failures, and control malfunctions for healthier indoor air.",
    ],
}

# Varied advantage points (rotate different subsets for different pages)
ADVANTAGE_POINTS = [
    ("<strong>Certified LG Specialists:</strong>", "Our technicians hold factory certifications specifically for LG appliances, ensuring repairs meet manufacturer standards."),
    ("<strong>Same-Day Appointments:</strong>", "We understand appliance emergencies. Same-day service is available throughout the area when you call before noon."),
    ("<strong>Genuine LG Parts:</strong>", "Every repair uses authentic LG components, maintaining warranty coverage and ensuring long-lasting results."),
    ("<strong>Transparent Pricing:</strong>", "You'll receive a complete quote before any work begins. No hidden fees or surprise charges."),
    ("<strong>Repair Warranty:</strong>", "All repairs include our service guarantee. If issues recur, we return at no additional cost."),
    ("<strong>Experienced Technicians:</strong>", "Our team averages over 10 years of appliance repair experience, with specialized LG training."),
    ("<strong>Stocked Service Vehicles:</strong>", "Technicians arrive with commonly needed parts, completing most repairs during the first visit."),
    ("<strong>Flexible Scheduling:</strong>", "We offer appointments seven days a week, including evenings, to fit your schedule."),
    ("<strong>Licensed and Insured:</strong>", "Full liability coverage protects your home. Insurance certificates available upon request."),
    ("<strong>Diagnostic Fee Applied:</strong>", "The service call fee applies toward your repair cost, reducing your total expense."),
    ("<strong>Local Service Team:</strong>", "Technicians dispatched from nearby locations ensure fast arrival and familiarity with the area."),
    ("<strong>24/7 Support Available:</strong>", "Emergency repairs available outside regular hours for urgent situations."),
    ("<strong>Free Follow-Up:</strong>", "If any problems arise after repair, we return to resolve them at no extra charge."),
    ("<strong>Price Match Promise:</strong>", "Found a lower quote for the same repair? We'll match legitimate competitor pricing."),
    ("<strong>Clean Work Guarantee:</strong>", "Technicians protect your floors and clean up completely after every repair."),
    ("<strong>Senior Discounts:</strong>", "Special pricing available for senior residents in the community."),
    ("<strong>Multi-Appliance Savings:</strong>", "Repair multiple appliances in one visit and save on the service call fee."),
    ("<strong>Energy Efficiency Check:</strong>", "We verify your repaired appliance operates at peak efficiency, potentially lowering utility bills."),
]

def get_town_detail(town_slug):
    """Get or generate a town-specific detail."""
    if town_slug in TOWN_DETAILS:
        return TOWN_DETAILS[town_slug]
    # Generate a generic but varied description
    variations = [
        "a welcoming New Jersey community",
        "a growing residential area",
        "a family-oriented neighborhood",
        "a well-established township",
        "a thriving local community",
    ]
    return random.choice(variations)

def get_appliance_intro(appliance, town_name, county_name):
    """Get a unique intro paragraph for this appliance/town combo."""
    intros = APPLIANCE_INTROS.get(appliance, APPLIANCE_INTROS["refrigerator"])
    base_intro = random.choice(intros)
    return base_intro

def get_advantage_subset(seed_value):
    """Get a varied subset of advantage points based on page seed."""
    random.seed(seed_value)
    # Pick 8-10 random advantages instead of all 15
    num_points = random.randint(8, 10)
    selected = random.sample(ADVANTAGE_POINTS, num_points)
    random.shuffle(selected)
    return selected

def format_town_name(slug):
    """Convert slug to proper town name."""
    return slug.replace("-", " ").title().replace(" Township", " Township").replace(" County", " County")

def generate_unique_intro(town_slug, county_slug, appliance):
    """Generate unique intro paragraph content."""
    town_name = format_town_name(town_slug)
    county_name = format_town_name(county_slug)
    town_detail = get_town_detail(town_slug)
    appliance_name = appliance.replace("-", " ")
    appliance_display = appliance_name

    # Create unique opening
    intro = get_appliance_intro(appliance, town_name, county_name)

    # Add town-specific context
    local_context = f"Serving {town_name}, {town_detail}, our factory-certified technicians bring specialized LG {appliance_display} expertise directly to your home."

    return f'<p style="margin-bottom: 15px;">{intro}</p>\n                        <p style="margin-bottom: 15px;">{local_context}</p>'

def generate_advantage_html(town_slug, county_slug, appliance):
    """Generate varied advantage points HTML."""
    seed = hash(f"{town_slug}-{county_slug}-{appliance}")
    advantages = get_advantage_subset(seed)
    county_name = format_town_name(county_slug)

    html_parts = [f'<h3 style="font-size: 20px; color: var(--blue); margin: 25px 0 15px;">Why Choose Us in {county_name}</h3>']
    html_parts.append('<ul style="list-style: none; padding: 0; margin: 0 0 20px 0;">')

    for i, (title, desc) in enumerate(advantages):
        border = 'border-bottom: 1px solid #eee; ' if i < len(advantages) - 1 else ''
        html_parts.append(f'''                            <li style="padding: 12px 0; {border}display: flex; align-items: flex-start;">
                                <span style="color: var(--red); font-weight: bold; margin-right: 10px; font-size: 18px;">✓</span>
                                <span>{title} {desc}</span>
                            </li>''')

    html_parts.append('                        </ul>')
    return '\n'.join(html_parts)

def rewrite_page(filepath, town_slug, county_slug, appliance):
    """Rewrite the expandable content sections of a page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    town_name = format_town_name(town_slug)
    county_name = format_town_name(county_slug)
    appliance_name = appliance.replace("-", " ")

    # Generate new intro content
    new_intro = generate_unique_intro(town_slug, county_slug, appliance)

    # Generate new advantage section
    new_advantages = generate_advantage_html(town_slug, county_slug, appliance)

    # Find and replace the expandable-text-1 content
    # Pattern: from opening p tag after expandable-text-1 div to the closing </ul> before the fade div

    # Build the replacement content
    replacement_content = f'''{new_intro}
                        {new_advantages}'''

    # Use regex to find and replace the content between expandable-text-1 div and expandable-fade-1
    pattern = r'(<div id="expandable-text-1"[^>]*>)\s*<p style="margin-bottom: 15px;">.*?</ul>\s*(</div>\s*<div id="expandable-fade-1")'

    replacement = f'\\1\n                        {replacement_content}\n                    \\2'

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def url_to_filepath(url, base_dir):
    """Convert URL to local filepath."""
    # Remove domain
    path = url.replace("https://lgappliancerepairnj.com/", "")
    # Remove trailing slash
    path = path.rstrip("/")
    # Add index.html
    filepath = os.path.join(base_dir, path, "index.html")
    return filepath

def parse_url(url):
    """Extract county, town, appliance from URL."""
    path = url.replace("https://lgappliancerepairnj.com/", "").rstrip("/")
    parts = path.split("/")

    if len(parts) == 3:
        county, town, appliance = parts
        appliance = appliance.replace("-repair", "")
        return county, town, appliance
    elif len(parts) == 2:
        # Town-only page
        county, town = parts
        return county, town, None
    return None, None, None

def main():
    base_dir = "/tmp/lg-appliance-repair-nj"
    csv_path = "/tmp/lgappliancerepair_crawl/Table.csv"

    # Read affected URLs
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        urls = [row[0] for row in reader]

    success_count = 0
    skip_count = 0
    fail_count = 0

    for url in urls:
        county, town, appliance = parse_url(url)

        if not appliance:
            # Town-only page - skip for now
            skip_count += 1
            print(f"SKIP (town-only): {url}")
            continue

        filepath = url_to_filepath(url, base_dir)

        if not os.path.exists(filepath):
            fail_count += 1
            print(f"FAIL (not found): {filepath}")
            continue

        if rewrite_page(filepath, town, county, appliance):
            success_count += 1
            print(f"OK: {town}/{appliance}")
        else:
            fail_count += 1
            print(f"FAIL (no match): {filepath}")

    print(f"\nDone: {success_count} updated, {skip_count} skipped, {fail_count} failed")

if __name__ == "__main__":
    main()
