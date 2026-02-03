#!/usr/bin/env python3
"""
Update county-level pages with unique, locally relevant expandable content
for each appliance type that specifically mentions the county name.
Preserves contextual links to other appliance pages.
"""

import os
import re
from pathlib import Path

# County data with local characteristics for unique content
COUNTIES = {
    "atlantic-county": {
        "name": "Atlantic County",
        "short": "Atlantic County",
        "characteristics": "coastal communities and beach towns",
        "notable": "Atlantic City and surrounding shore communities",
        "housing": "beachfront homes, condominiums, and seasonal properties",
        "lifestyle": "tourism-driven economy with year-round residents",
        "water": "hard water from coastal aquifers"
    },
    "burlington-county": {
        "name": "Burlington County",
        "short": "Burlington County",
        "characteristics": "mix of suburban and rural communities",
        "notable": "historic townships and farmland areas",
        "housing": "single-family homes, townhouses, and rural estates",
        "lifestyle": "family-oriented communities with agricultural heritage",
        "water": "varying water quality across municipal systems"
    },
    "camden-county": {
        "name": "Camden County",
        "short": "Camden County",
        "characteristics": "diverse urban and suburban neighborhoods",
        "notable": "Camden waterfront and Cherry Hill",
        "housing": "row homes, suburban developments, and apartments",
        "lifestyle": "commuter communities with Philadelphia access",
        "water": "treated municipal water systems"
    },
    "cape-may-county": {
        "name": "Cape May County",
        "short": "Cape May County",
        "characteristics": "premier shore destination communities",
        "notable": "Victorian Cape May and beach communities",
        "housing": "vacation homes, bed and breakfasts, and year-round residences",
        "lifestyle": "seasonal tourism with dedicated locals",
        "water": "coastal water with mineral content"
    },
    "cumberland-county": {
        "name": "Cumberland County",
        "short": "Cumberland County",
        "characteristics": "agricultural heartland communities",
        "notable": "Vineland, Millville, and Bridgeton",
        "housing": "farmhouses, suburban homes, and historic properties",
        "lifestyle": "agricultural community with glass-making heritage",
        "water": "well water common in rural areas"
    },
    "essex-county": {
        "name": "Essex County",
        "short": "Essex County",
        "characteristics": "diverse urban and affluent suburban areas",
        "notable": "Newark, Montclair, and the Oranges",
        "housing": "high-rises, historic homes, and luxury properties",
        "lifestyle": "urban professionals and established families",
        "water": "Newark watershed with quality municipal water"
    },
    "gloucester-county": {
        "name": "Gloucester County",
        "short": "Gloucester County",
        "characteristics": "growing suburban communities",
        "notable": "Washington Township and Deptford",
        "housing": "newer developments, established neighborhoods, townhomes",
        "lifestyle": "family communities with Philadelphia commuters",
        "water": "municipal systems with moderate hardness"
    },
    "hudson-county": {
        "name": "Hudson County",
        "short": "Hudson County",
        "characteristics": "densely populated urban area",
        "notable": "Jersey City, Hoboken, and waterfront communities",
        "housing": "high-rise apartments, brownstones, and luxury condos",
        "lifestyle": "NYC commuters and young professionals",
        "water": "urban water systems with treatment"
    },
    "hunterdon-county": {
        "name": "Hunterdon County",
        "short": "Hunterdon County",
        "characteristics": "affluent rural and suburban landscape",
        "notable": "Flemington, Clinton, and picturesque townships",
        "housing": "estates, historic homes, and upscale developments",
        "lifestyle": "equestrian communities and executive families",
        "water": "well water prevalent with varying mineral content"
    },
    "mercer-county": {
        "name": "Mercer County",
        "short": "Mercer County",
        "characteristics": "state capital region communities",
        "notable": "Trenton, Princeton, and surrounding townships",
        "housing": "historic properties, university housing, suburban homes",
        "lifestyle": "government workers, academics, and professionals",
        "water": "Delaware River watershed supply"
    },
    "middlesex-county": {
        "name": "Middlesex County",
        "short": "Middlesex County",
        "characteristics": "central New Jersey hub communities",
        "notable": "New Brunswick, Edison, and diverse townships",
        "housing": "varied housing from apartments to estates",
        "lifestyle": "diverse communities with major employers",
        "water": "multiple water authorities serving the area"
    },
    "monmouth-county": {
        "name": "Monmouth County",
        "short": "Monmouth County",
        "characteristics": "shore communities and affluent suburbs",
        "notable": "Red Bank, Long Branch, and Holmdel",
        "housing": "beachfront properties, horse farms, suburban homes",
        "lifestyle": "beach culture meets suburban sophistication",
        "water": "aquifer-supplied with varying hardness levels"
    },
    "morris-county": {
        "name": "Morris County",
        "short": "Morris County",
        "characteristics": "affluent suburban communities",
        "notable": "Morristown, Parsippany, and historic townships",
        "housing": "executive homes, historic estates, modern developments",
        "lifestyle": "corporate headquarters and established families",
        "water": "reservoir-supplied quality water"
    },
    "ocean-county": {
        "name": "Ocean County",
        "short": "Ocean County",
        "characteristics": "shore communities and retirement destinations",
        "notable": "Toms River, Lakewood, and barrier island towns",
        "housing": "beach homes, retirement communities, family neighborhoods",
        "lifestyle": "retirees, families, and seasonal residents",
        "water": "Kirkwood-Cohansey aquifer supply"
    },
    "passaic-county": {
        "name": "Passaic County",
        "short": "Passaic County",
        "characteristics": "urban centers and suburban highlands",
        "notable": "Paterson, Wayne, and mountain communities",
        "housing": "urban apartments, suburban homes, highland properties",
        "lifestyle": "diverse working communities and suburban families",
        "water": "Passaic Valley Water Commission service"
    },
    "salem-county": {
        "name": "Salem County",
        "short": "Salem County",
        "characteristics": "rural agricultural community",
        "notable": "Salem City and farming townships",
        "housing": "farmhouses, historic homes, rural properties",
        "lifestyle": "agricultural heritage with small-town values",
        "water": "well water common throughout"
    },
    "somerset-county": {
        "name": "Somerset County",
        "short": "Somerset County",
        "characteristics": "upscale suburban communities",
        "notable": "Bridgewater, Franklin, and Hillsborough",
        "housing": "executive homes, townhouse communities, estates",
        "lifestyle": "pharmaceutical corridor professionals and families",
        "water": "Raritan watershed and well systems"
    },
    "sussex-county": {
        "name": "Sussex County",
        "short": "Sussex County",
        "characteristics": "mountainous rural landscape",
        "notable": "Newton, Vernon, and lakeside communities",
        "housing": "lake houses, mountain homes, rural properties",
        "lifestyle": "outdoor enthusiasts and rural residents",
        "water": "well water with mineral content typical"
    },
    "union-county": {
        "name": "Union County",
        "short": "Union County",
        "characteristics": "established suburban communities",
        "notable": "Elizabeth, Westfield, and Summit",
        "housing": "historic homes, suburban developments, urban apartments",
        "lifestyle": "commuters and established neighborhood communities",
        "water": "Elizabethtown Water Company service"
    },
    "warren-county": {
        "name": "Warren County",
        "short": "Warren County",
        "characteristics": "scenic Skylands region communities",
        "notable": "Phillipsburg, Washington, and Delaware Water Gap area",
        "housing": "rural properties, small-town homes, historic buildings",
        "lifestyle": "rural living with outdoor recreation focus",
        "water": "well and spring water common"
    }
}

def generate_washer_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Washer Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG washer repair technicians</strong> serve all of {county_data["name"]}, understanding the specific needs of {county_data["characteristics"]}. From {county_data["notable"]}, we provide prompt service for front-load, top-load, and specialty washers in {county_data["housing"]}. {county_data["name"]} residents rely on us for expert diagnosis and genuine LG parts.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Common Washer Issues in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">{county_data["name"]} homes often experience washer problems related to {county_data["water"]}. We frequently repair water inlet valve issues, drain pump failures, and bearing problems. Our technicians carry parts for common LG washer repairs, often completing service in a single visit to your {county_data["short"]} home.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Front Load Washer Expertise</h4>
                                <p style="margin-bottom: 12px;"><strong>LG front load washer repair</strong> in {county_data["name"]} addresses door boot seal leaks, bearing failures, and spider arm corrosion. We service the {county_data["lifestyle"]} with flexible scheduling. Front loaders in {county_data["short"]} benefit from our expertise with high-efficiency models and proper maintenance guidance.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Top Load Washer Service</h4>
                                <p style="margin-bottom: 12px;"><strong>LG top load washer repair</strong> throughout {county_data["name"]} covers agitator and impeller models. We fix lid switch failures, transmission issues, and water inlet problems. {county_data["short"]} families trust us for reliable service on all LG top-loading washers, from basic models to smart ThinQ-enabled units.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Residential Washer Repair</h4>
                                <p style="margin-bottom: 12px;"><strong>LG residential washer repair</strong> covers all home laundry machines in {county_data["name"]} from basic models to premium smart washers. We understand that a broken washer disrupts daily family routines. For dryer issues in the same visit, see our <a href="https://lgappliancerepairnj.com/appliances/dryer-repair/" style="color: var(--blue); font-weight: 500;">LG dryer repair services</a>. Our technicians service washers in laundry rooms, basements, and garages throughout {county_data["short"]} homes.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Why Choose Us in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">We've served {county_data["name"]} families for years, building a reputation for honest, reliable LG washer repair. Our technicians know the {county_data["characteristics"]} and provide service tailored to local needs. Same-day appointments available throughout {county_data["short"]} when you need urgent washer repair.</p>
'''

def generate_dryer_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Dryer Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG dryer repair specialists</strong> provide comprehensive service throughout {county_data["name"]}. We understand the needs of {county_data["housing"]} and offer expert repair for gas, electric, and ventless dryers. From {county_data["notable"]}, {county_data["short"]} residents trust our certified technicians.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Gas Dryer Repair in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG gas dryer repair</strong> in {county_data["name"]} requires certified technicians trained in gas safety protocols. We repair igniter systems, gas valve solenoids, and flame sensors. {county_data["short"]} homes with gas dryers receive priority service to minimize inconvenience and ensure safe operation.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Electric Dryer Service</h4>
                                <p style="margin-bottom: 12px;"><strong>LG electric dryer repair</strong> across {county_data["name"]} addresses heating elements, thermal fuses, and thermostats. We diagnose 240-volt power issues common in older {county_data["housing"]}. {county_data["short"]} customers appreciate our thorough diagnostics and upfront pricing.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Smart Dryer Technology</h4>
                                <p style="margin-bottom: 12px;"><strong>LG ThinQ smart dryer repair</strong> in {county_data["name"]} includes WiFi connectivity troubleshooting and smart diagnosis features. We repair control boards enabling smart features and diagnose connectivity problems. Pair with our <a href="https://lgappliancerepairnj.com/appliances/washer-repair/" style="color: var(--blue); font-weight: 500;">LG washer repair</a> for complete laundry system service in {county_data["short"]}.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Ventless Dryer Expertise</h4>
                                <p style="margin-bottom: 12px;">Ventless and heat pump dryers are increasingly popular in {county_data["name"]}, especially in {county_data["characteristics"]}. We service condenser systems, heat exchangers, and condensate pumps. {county_data["short"]} apartments and condos benefit from our ventless dryer expertise.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Serving {county_data["short"]} Communities</h4>
                                <p style="margin-bottom: 12px;">From {county_data["notable"]}, we provide same-day LG dryer repair throughout {county_data["name"]}. Our technicians serve the {county_data["lifestyle"]} with flexible scheduling and professional service. Trust {county_data["short"]}'s preferred LG dryer repair specialists.</p>
'''

def generate_oven_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Oven Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG oven repair technicians</strong> serve kitchens throughout {county_data["name"]}, from {county_data["notable"]} to every corner of the county. We repair gas and electric ovens in {county_data["housing"]}, understanding the cooking needs of {county_data["lifestyle"]}.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Gas Oven Repair in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG gas oven repair</strong> in {county_data["name"]} requires expertise with igniters, gas valves, and safety systems. We service gas ranges and wall ovens throughout {county_data["short"]}, ensuring safe operation and precise temperature control. We also service <a href="https://lgappliancerepairnj.com/appliances/cooktop-repair/" style="color: var(--blue); font-weight: 500;">LG cooktops</a> and range surfaces.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Electric Oven Service</h4>
                                <p style="margin-bottom: 12px;"><strong>LG electric oven repair</strong> across {county_data["name"]} addresses bake and broil elements, control boards, and convection fans. {county_data["short"]} homes with electric ranges trust our thorough diagnostics and quality repairs using genuine LG components.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Convection Oven Expertise</h4>
                                <p style="margin-bottom: 12px;">LG convection ovens in {county_data["name"]} provide even cooking through fan-circulated heat. We repair convection motors, fan assemblies, and related controls. {county_data["short"]} home chefs rely on our expertise to maintain their convection cooking performance.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Smart Oven Technology</h4>
                                <p style="margin-bottom: 12px;">LG ThinQ smart ovens in {county_data["name"]} offer remote monitoring and recipe integration. We service WiFi connectivity, app features, and the advanced controls that make smart cooking possible. {county_data["short"]} residents with connected kitchens trust our technical expertise.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Trusted in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Families throughout {county_data["name"]} depend on working ovens for daily meals and special occasions. We provide prompt, professional LG oven repair with same-day service available in {county_data["short"]}. Your kitchen is too important for delays.</p>
'''

def generate_fridge_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Refrigerator Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG refrigerator repair specialists</strong> protect food and families throughout {county_data["name"]}. From {county_data["notable"]}, we provide urgent service for all LG fridge models in {county_data["housing"]}. {county_data["short"]} residents trust our expertise with French door, side-by-side, and specialty refrigerators.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Cooling System Repair in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG refrigerator cooling issues</strong> in {county_data["name"]} often stem from compressor problems, sealed system leaks, or fan failures. We diagnose warm fridges, frost buildup, and temperature inconsistencies. {county_data["short"]} families receive priority service to prevent food spoilage.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Ice Maker and Dispenser Service</h4>
                                <p style="margin-bottom: 12px;">LG ice makers and water dispensers in {county_data["name"]} can be affected by {county_data["water"]}. We repair ice production problems, dispenser malfunctions, and water line issues. {county_data["short"]} homes enjoy restored ice and water functionality with our expert service.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Top-Freezer Refrigerator Service</h4>
                                <p style="margin-bottom: 12px;"><strong>LG top-freezer refrigerator repair</strong> in {county_data["name"]} services the classic configuration with freezer compartment above the fresh food section. We repair compressor failures, defrost system problems, and evaporator fan issues. For compressor failures, see our specialized <a href="https://lgappliancerepairnj.com/repairs/lg-refrigerator-compressor-replacement/" style="color: var(--blue); font-weight: 500;">LG compressor replacement service</a>.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">French Door Refrigerator Expertise</h4>
                                <p style="margin-bottom: 12px;"><strong>LG French door refrigerator repair</strong> throughout {county_data["name"]} addresses the unique features of these popular models. We service InstaView panels, door-in-door compartments, and dual ice makers. {county_data["short"]} kitchens with premium LG refrigerators receive specialized attention.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Emergency Service in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Refrigerator failures require immediate attention. We offer same-day LG refrigerator repair throughout {county_data["name"]} to protect your food investment. {county_data["short"]} families know they can count on us when their fridge stops cooling.</p>
'''

def generate_dishwasher_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Dishwasher Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG dishwasher repair technicians</strong> restore convenience to {county_data["name"]} kitchens. We service all LG dishwasher models in {county_data["housing"]} throughout {county_data["short"]}. From {county_data["notable"]}, families trust our expertise with QuadWash, TrueSteam, and standard models.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Cleaning Performance Issues in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG dishwasher cleaning problems</strong> in {county_data["name"]} often relate to {county_data["water"]}. We repair spray arm issues, wash motor failures, and water circulation problems. {county_data["short"]} homes receive thorough diagnostics to restore sparkling clean results.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Built-In Dishwasher Repair</h4>
                                <p style="margin-bottom: 12px;"><strong>LG built-in dishwasher repair</strong> services standard under-counter units in {county_data["name"]} kitchens. We repair drain pump failures, wash motor problems, and door latch mechanisms. Need help with other kitchen appliances? See our <a href="https://lgappliancerepairnj.com/appliances/microwave-repair/" style="color: var(--blue); font-weight: 500;">LG microwave repair</a> services.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Drainage and Leak Repair</h4>
                                <p style="margin-bottom: 12px;">LG dishwashers in {county_data["name"]} can experience drain pump failures and door seal leaks. We repair drainage issues, replace worn gaskets, and address water pooling problems. {county_data["short"]} kitchens stay dry with our professional leak repairs.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">QuadWash and TrueSteam Service</h4>
                                <p style="margin-bottom: 12px;">LG's QuadWash technology uses multi-motion spray arms for superior cleaning. TrueSteam provides sanitization and better results. Our {county_data["name"]} technicians service these advanced systems, ensuring {county_data["short"]} residents enjoy premium dishwasher performance.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Reliable Service in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">A broken dishwasher disrupts {county_data["name"]} household routines. We provide prompt LG dishwasher repair with same-day availability throughout {county_data["short"]}. The {county_data["lifestyle"]} deserve working appliances without long waits.</p>
'''

def generate_cooktop_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Cooktop Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG cooktop repair specialists</strong> service gas, electric, and induction cooktops throughout {county_data["name"]}. From {county_data["notable"]}, we repair cooktops in {county_data["housing"]}. {county_data["short"]} home cooks trust our expertise with all LG cooking surfaces.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Gas Cooktop Repair in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG gas cooktop repair</strong> in {county_data["name"]} addresses igniter failures, burner issues, and gas valve problems. We ensure safe, efficient operation for {county_data["short"]} kitchens. For oven and range service, visit our <a href="https://lgappliancerepairnj.com/appliances/oven-repair/" style="color: var(--blue); font-weight: 500;">LG oven repair</a> page.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Electric Cooktop Service</h4>
                                <p style="margin-bottom: 12px;"><strong>LG electric cooktop repair</strong> across {county_data["name"]} covers radiant elements, smoothtop surfaces, and control systems. {county_data["short"]} homes with electric cooktops receive expert diagnosis and repair for heating issues, cracked glass, and control malfunctions.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Induction Cooktop Expertise</h4>
                                <p style="margin-bottom: 12px;">LG induction cooktops in {county_data["name"]} use magnetic technology for precise, efficient cooking. We repair induction coils, power boards, and control systems. {county_data["short"]} residents with induction cooking enjoy our specialized technical knowledge.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Burner and Element Issues</h4>
                                <p style="margin-bottom: 12px;">Whether gas burners won't light or electric elements won't heat, {county_data["name"]} residents can count on our expertise. We diagnose and repair individual burners, ensuring even heating across your LG cooktop. {county_data["short"]} kitchens deserve full cooking capability.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Professional Service in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Cooking is central to {county_data["name"]} family life. We provide reliable LG cooktop repair throughout {county_data["short"]} with same-day service available. The {county_data["lifestyle"]} trust our professional approach and quality workmanship.</p>
'''

def generate_microwave_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Microwave Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG microwave repair technicians</strong> service countertop and over-the-range models throughout {county_data["name"]}. From {county_data["notable"]}, we repair microwaves in {county_data["housing"]}. {county_data["short"]} residents trust our expertise with all LG microwave systems.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Over-the-Range Microwave Repair in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG over-the-range microwave repair</strong> in {county_data["name"]} addresses heating issues, ventilation problems, and light failures. We service these combination units that save counter space in {county_data["short"]} kitchens while providing exhaust ventilation.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Convection Microwave Repair</h4>
                                <p style="margin-bottom: 12px;"><strong>LG convection microwave repair</strong> services combination units in {county_data["name"]} offering both microwave and convection cooking for baking and roasting. We repair convection fans, heating elements, and combination cooking controls. We also handle <a href="https://lgappliancerepairnj.com/appliances/oven-repair/" style="color: var(--blue); font-weight: 500;">LG oven and range repairs</a> for complete kitchen coverage.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Countertop Microwave Service</h4>
                                <p style="margin-bottom: 12px;"><strong>LG countertop microwave repair</strong> across {county_data["name"]} covers magnetron failures, turntable issues, and control panel problems. {county_data["short"]} homes with countertop models receive the same professional service as built-in units.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Heating and Power Issues</h4>
                                <p style="margin-bottom: 12px;">Microwaves that don't heat properly frustrate {county_data["name"]} families. We diagnose magnetron failures, diode problems, and capacitor issues. {county_data["short"]} residents enjoy restored microwave function with our expert repairs.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Fast Service in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Microwaves are essential for busy {county_data["name"]} households. We provide prompt LG microwave repair throughout {county_data["short"]}. The {county_data["lifestyle"]} depend on quick, reliable appliance service.</p>
'''

def generate_wine_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Wine Cooler Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG wine cooler repair specialists</strong> protect wine collections throughout {county_data["name"]}. From {county_data["notable"]}, we service wine refrigerators in {county_data["housing"]}. {county_data["short"]} wine enthusiasts trust our expertise with temperature-sensitive storage.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Temperature Control Issues in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG wine cooler temperature problems</strong> in {county_data["name"]} can damage valuable wine collections. We repair cooling systems, thermostats, and compressors to maintain proper storage conditions. {county_data["short"]} collectors receive priority service for temperature emergencies.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Dual Zone Wine Refrigerators</h4>
                                <p style="margin-bottom: 12px;">LG dual zone wine coolers in {county_data["name"]} store reds and whites at different temperatures. We repair zone control systems, independent cooling circuits, and temperature sensors. {county_data["short"]} wine connoisseurs enjoy restored dual zone functionality.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Compressor and Cooling Repair</h4>
                                <p style="margin-bottom: 12px;">Wine cooler compressors in {county_data["name"]} require quiet, consistent operation. We diagnose and repair cooling failures, fan issues, and refrigerant problems. {county_data["short"]} wine storage stays at perfect temperature with our expert service.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Built-In Wine Cooler Service</h4>
                                <p style="margin-bottom: 12px;">Built-in LG wine coolers in {county_data["name"]} kitchens require service technicians who understand installation constraints. We repair units in cabinetry with proper care. {county_data["short"]} custom kitchens receive meticulous service.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Protecting Your Investment in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Wine collections represent significant investment for {county_data["name"]} residents. We provide urgent LG wine cooler repair throughout {county_data["short"]} to protect your wines. Don't risk your collection with cooling failures.</p>
'''

def generate_hood_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Vent Hood Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG range hood repair technicians</strong> maintain kitchen air quality throughout {county_data["name"]}. From {county_data["notable"]}, we service vent hoods in {county_data["housing"]}. {county_data["short"]} kitchens stay fresh with our expert ventilation repairs.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Ventilation Fan Repair in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG vent hood fan problems</strong> in {county_data["name"]} reduce cooking comfort and air quality. We repair fan motors, blade assemblies, and speed controls. {county_data["short"]} homes enjoy restored ventilation power with our professional service.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Light and Control Issues</h4>
                                <p style="margin-bottom: 12px;">LG range hood lights and controls in {county_data["name"]} ensure safe, convenient cooking. We repair LED lighting, touch controls, and switch assemblies. {county_data["short"]} kitchens stay well-lit and properly ventilated.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Ducted vs. Ductless Systems</h4>
                                <p style="margin-bottom: 12px;">{county_data["name"]} homes have both ducted and recirculating vent hoods. We service external venting systems and charcoal filter units. {county_data["short"]} kitchens receive appropriate service for their ventilation configuration.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Filter Maintenance and Repair</h4>
                                <p style="margin-bottom: 12px;">Grease filters and charcoal filters in {county_data["name"]} range hoods require regular attention. We clean, repair, and replace filtration components. {county_data["short"]} cooking produces less odor and grease buildup with proper filter service.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Kitchen Comfort in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Proper ventilation matters for {county_data["name"]} home cooks. We provide reliable LG vent hood repair throughout {county_data["short"]}. The {county_data["lifestyle"]} deserve comfortable, well-ventilated kitchens.</p>
'''

def generate_freezer_content(county_data):
    return f'''
                                <h4 style="color: var(--blue); margin: 15px 0 10px;">LG Freezer Service in {county_data["name"]}</h4>
                                <p style="margin-bottom: 12px;">Our <strong>LG freezer repair specialists</strong> protect frozen foods throughout {county_data["name"]}. From {county_data["notable"]}, we service standalone freezers and refrigerator freezer compartments in {county_data["housing"]}. {county_data["short"]} residents trust our urgent response to freezer failures.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Cooling Failures in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;"><strong>LG freezer not freezing</strong> in {county_data["name"]} requires immediate attention to prevent food loss. We diagnose compressor issues, sealed system problems, and thermostat failures. {county_data["short"]} families receive priority service for freezer emergencies.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Frost and Ice Buildup</h4>
                                <p style="margin-bottom: 12px;">Excess frost in {county_data["name"]} LG freezers indicates defrost system problems. We repair defrost heaters, timers, and thermostats. {county_data["short"]} freezers stay frost-free with our expert defrost system repairs.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Standalone Freezer Repair</h4>
                                <p style="margin-bottom: 12px;">Chest and upright LG freezers in {county_data["name"]} provide valuable food storage. We repair these standalone units throughout {county_data["short"]}, addressing compressor failures, seal issues, and temperature control problems.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Refrigerator Freezer Compartments</h4>
                                <p style="margin-bottom: 12px;">Freezer sections in LG refrigerators throughout {county_data["name"]} sometimes fail independently. We diagnose air flow issues, damper failures, and individual compartment problems. {county_data["short"]} families get complete freezer compartment repairs.</p>

                                <h4 style="color: var(--blue); margin: 15px 0 10px;">Emergency Freezer Service in {county_data["short"]}</h4>
                                <p style="margin-bottom: 12px;">Freezer failures threaten food investments for {county_data["name"]} households. We provide same-day LG freezer repair throughout {county_data["short"]} when available. Protect your frozen foods with our rapid response service.</p>
'''

def generate_main_content(county_data):
    return f'''
                        <h4 style="color: var(--blue); margin: 15px 0 10px;">Expert LG Appliance Repair in {county_data["name"]}</h4>
                        <p style="margin-bottom: 12px;">Welcome to {county_data["name"]}'s trusted source for <strong>professional LG appliance repair</strong>. Our certified technicians serve {county_data["characteristics"]}, providing expert service for all LG home appliances. From {county_data["notable"]}, we deliver prompt, reliable repairs that restore your appliances to peak performance.</p>

                        <h4 style="color: var(--blue); margin: 15px 0 10px;">Why {county_data["short"]} Chooses Us</h4>
                        <p style="margin-bottom: 12px;">{county_data["name"]} residents deserve appliance repair technicians who understand local needs. We've built our reputation serving {county_data["housing"]} throughout the county. Our technicians know the {county_data["lifestyle"]} and provide service tailored to {county_data["short"]} homes and schedules.</p>

                        <h4 style="color: var(--blue); margin: 15px 0 10px;">Comprehensive LG Service</h4>
                        <p style="margin-bottom: 15px;">As the leading <strong>LG appliance repair</strong> provider in <strong>{county_data["name"]}</strong>, we deliver exceptional service throughout the county. Our <strong>factory-certified technicians</strong> diagnose and repair your <a href="https://lgappliancerepairnj.com/appliances/washer-repair/" style="color: var(--blue); font-weight: 500;">washer</a>, dryer, refrigerator, or dishwasher with precision and care.</p>

                        <h4 style="color: var(--blue); margin: 15px 0 10px;">Local Water Considerations</h4>
                        <p style="margin-bottom: 12px;">{county_data["name"]} homes often deal with {county_data["water"]}. This affects appliances like dishwashers, washing machines, and ice makers. Our technicians understand these local conditions and provide appropriate maintenance recommendations for {county_data["short"]} households.</p>

                        <h4 style="color: var(--blue); margin: 15px 0 10px;">Same-Day Service Available</h4>
                        <p style="margin-bottom: 12px;">When appliances fail, {county_data["name"]} families need fast response. We offer same-day LG appliance repair throughout {county_data["short"]} based on availability. Emergency refrigerator and freezer repairs receive priority scheduling to protect your food.</p>

                        <h4 style="color: var(--blue); margin: 15px 0 10px;">Serving All {county_data["short"]} Communities</h4>
                        <p style="margin-bottom: 12px;">From {county_data["notable"]} to every township in the county, our technicians provide consistent, professional LG appliance repair. {county_data["name"]} residents throughout the area trust our honest assessments, fair pricing, and quality workmanship. Contact us today for expert LG service.</p>
'''

def update_county_file(filepath, county_key):
    """Update a single county file with unique content."""
    county_data = COUNTIES.get(county_key)
    if not county_data:
        print(f"No data for county: {county_key}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate new content for each appliance section
    new_washer = generate_washer_content(county_data)
    new_dryer = generate_dryer_content(county_data)
    new_oven = generate_oven_content(county_data)
    new_fridge = generate_fridge_content(county_data)
    new_dishwasher = generate_dishwasher_content(county_data)
    new_cooktop = generate_cooktop_content(county_data)
    new_microwave = generate_microwave_content(county_data)
    new_wine = generate_wine_content(county_data)
    new_hood = generate_hood_content(county_data)
    new_main = generate_main_content(county_data)

    # Replace each expandable section
    # Pattern to match expandable text content
    def replace_expandable(content, section_id, new_text):
        pattern = rf'(<div id="expandable-text-{section_id}"[^>]*>)\s*(.*?)\s*(</div>\s*<div id="expandable-fade-{section_id}")'
        replacement = rf'\1{new_text}\3'
        return re.sub(pattern, replacement, content, flags=re.DOTALL)

    content = replace_expandable(content, 'washer', new_washer)
    content = replace_expandable(content, 'dryer', new_dryer)
    content = replace_expandable(content, 'oven', new_oven)
    content = replace_expandable(content, 'fridge', new_fridge)
    content = replace_expandable(content, 'dishwasher', new_dishwasher)
    content = replace_expandable(content, 'cooktop', new_cooktop)
    content = replace_expandable(content, 'microwave', new_microwave)
    content = replace_expandable(content, 'wine', new_wine)
    content = replace_expandable(content, 'hood', new_hood)

    # Replace main section (expandable-text-1)
    pattern = r'(<div id="expandable-text-1"[^>]*>)\s*(.*?)\s*(</div>\s*<div id="expandable-fade-1")'
    replacement = rf'\1{new_main}\3'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    base_path = Path('/tmp/lg-appliance-repair-nj')

    # Find all county index.html files
    county_files = list(base_path.glob('*-county/index.html'))

    print(f"Found {len(county_files)} county pages to update")

    updated = 0
    for filepath in county_files:
        county_key = filepath.parent.name
        print(f"Updating {county_key}...")
        if update_county_file(str(filepath), county_key):
            updated += 1
            print(f"  Updated successfully")
        else:
            print(f"  Skipped - no data")

    print(f"\nCompleted: {updated} files updated")

if __name__ == '__main__':
    main()
