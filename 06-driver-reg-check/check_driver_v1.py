#coding=utf-8
import xml.etree.ElementTree as ET

def driver_initsettings_check(xml_file):
    print(f"Checking init settings in {xml_file}...")

    tree = ET.parse(xml_file)
    root = tree.getroot()

    init_settings = []
    for reg_setting in root.iter('regSetting'):
        addr = reg_setting.find('registerAddr').text
        data = reg_setting.find('registerData').text
        init_settings.append((addr, data))

    return init_settings

def driver_factory_initdata(txt_file):
    print(f"Reading factory init data from {txt_file}...")

    factory_data = []
    with open(txt_file, 'r') as file:
        for line in file:
            addr, data = line.strip().split(',')
            factory_data.append((addr.strip(), data.strip()))

    return factory_data

def main():
    xml_file = 'hi1336_sensor.xml'
    txt_file = 'init.txt'

    init_settings = driver_initsettings_check(xml_file)
    factory_data = driver_factory_initdata(txt_file)

    # Compare init settings and factory data
    for (addr_xml, data_xml), (addr_txt, data_txt) in zip(init_settings, factory_data):
        if addr_xml != addr_txt or data_xml != data_txt:
            print(f"Data mismatch! XML: ({addr_xml}, {data_xml}), Text: ({addr_txt}, {data_txt})")

if __name__ == "__main__":
    main()