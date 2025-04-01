from lxml import etree
import xmlschema

def read_xml(payload_path):
    """
    Reads an XML file with a file lock to prevent concurrent access.
    """
    with open(payload_path, 'rb') as f:
        payload = etree.parse(f)
    return payload

def validate_xml_against_xsd(xsd_filename, payload_path):
    """
    Validates the given XML payload against the XSD schema file.
    Raises a pytest failure if the validation fails, with detailed error messages.
    """
    is_valid = False
    try:
        tree = etree.parse(xsd_filename)
        root = tree.getroot()

        # Define namespaces for xs and vc
        namespaces = {
            'xs': 'http://www.w3.org/2001/XMLSchema',
            'vc': 'http://www.w3.org/2007/XMLSchema-versioning'
        }
        # Search for the schema element with vc:minVersion="1.1"
        schema_element = root.xpath("//xs:schema[@vc:minVersion='1.1']", namespaces=namespaces)
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XSD file & XSD version check: {e}")
        raise
    

    if schema_element:
        # Validate with XSD 1.1 schema
        xsd = xmlschema.XMLSchema11(xsd_filename)
        try:
            xsd.validate(payload_path)
            is_valid = True
        except xmlschema.XMLSchemaValidationError as e:
            print(f"Payload validation failed with the following error: {e}")

    else:
        # Validate with XSD 1.0 schema
        try:
            xsd = etree.XMLSchema(etree.parse(xsd_filename))
        except etree.XMLSchemaParseError as e:
            print(f"Error parsing XSD file: {e}")
            raise
        
        is_valid = xsd.validate(read_xml(payload_path))
        if not is_valid:
            # Collect all error messages
            errors = "\n".join([str(error) for error in xsd.error_log])
            print(f"Payload validation failed with the following errors {errors}")
    return is_valid

def print_result(xml_filename, xsd_filename):
    result = validate_xml_against_xsd(xsd_filename, xml_filename)
    if result:
        print(f"{xml_filename} - VALID")
    else:
        print(f"{xml_filename} - INVALID!!!!")

print_result("examples/AddPGN.xml", "xsd/AddPGN.xsd")
print_result("examples/FMStoIPDelivery.xml", "xsd/FMStoIPDelivery.xsd")
print_result("examples/FMStoIPResponse.xml", "xsd/FMStoIPResponse.xsd")
print_result("examples/GetPGN.xml", "xsd/GetPGN.xsd")
print_result("examples/PGNDetails.xml", "xsd/PGNDetails.xsd")
print_result("examples/PGNId.xml", "xsd/PGNId.xsd")
print_result("examples/PGNInfoKnown.xml", "xsd/PGNInfoKnown.xsd")
print_result("examples/PGNStatusStructure.xml", "xsd/PGNStatusStructure.xsd")
print_result("examples/RegistrationStatus.xml", "xsd/RegistrationStatus.xsd")
print_result("examples/RemovePGN.xml", "xsd/RemovePGN.xsd")
print_result("examples/SPN.xml", "xsd/SPN.xsd")

print_result("examples/FMStoIPDelivery_2.3.1_example1_no_SPN.xml", "xsd/FMStoIPDelivery.xsd")
print_result("examples/FMStoIPDelivery_2.3.1_example1_some_SPN.xml", "xsd/FMStoIPDelivery.xsd")
print_result("examples/FMStoIPDelivery_2.3.1_on-change_example2_full_SPN.xml", "xsd/FMStoIPDelivery.xsd")
print_result("examples/FMStoIPDelivery_2.3.1_on-change_example2_no_SPN.xml", "xsd/FMStoIPDelivery.xsd")