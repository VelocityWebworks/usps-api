import json
import requests
import xmltodict

from lxml import etree

from .constants import LABEL_ZPL, SERVICE_PRIORITY


class USPSApiError(Exception):
    pass


class USPSApi(object):
    urls = {
        'tracking': 'https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2{test}&XML={xml}',
        'label': 'https://secure.shippingapis.com/ShippingAPI.dll?API=eVS{test}&XML={xml}',
        'validate': 'https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML={xml}'
    }

    def __init__(self,  api_user_id, test=False):
        self.api_user_id = api_user_id
        self.test = test

    def send_request(self, action, xml):
        xml = etree.tostring(xml, pretty_print=self.test).decode()
        url = self.urls[action].format(
            **{'test': 'Certify' if self.test else '', 'xml': xml}
        )
        xml_response = requests.get(url).content
        response = json.loads(json.dumps(xmltodict.parse(xml_response)))
        if 'Error' in response:
            raise USPSApiError(response['Error']['Description'])
        return response

    def validate_address(self, *args, **kwargs):
        return ValidateAddress(self, *args, **kwargs)

    def track(self, *args, **kwargs):
        return TrackingInfo(self, *args, **kwargs)

    def create_shipment(self, *args, **kwargs):
        return ShippingLabel(self, *args, **kwargs)


class AddressValidate(object):

    def __init__(self, usps, address):
        xml = etree.Element('AddressValidateRequest', {'USERID': usps.api_user_id})
        _address = etree.SubElement(xml, 'Address', {'ID': '0'})
        address.add_to_xml(_address, prefix='', validate=True)

        self.result = usps.send_request('validate', xml)


class TrackingInfo(object):

    def __init__(self, usps, tracking_number):
        xml = etree.Element('TrackFieldRequest', {'USERID': usps.api_user_id})
        child = etree.SubElement(xml, 'TrackID', {'ID': tracking_number})

        self.result = usps.send_request('tracking', xml)


class ShippingLabel(object):

    def __init__(self, usps, to_address, from_address, weight,
                 service=SERVICE_PRIORITY, label_type=LABEL_ZPL):
        root = 'eVSRequest' if not usps.test else 'eVSCertifyRequest'
        xml = etree.Element(root, {'USERID': usps.api_user_id})

        label_params = etree.SubElement(xml, 'ImageParameters')
        label = etree.SubElement(label_params, 'ImageParameter')
        label.text = label_type

        from_address.add_to_xml(xml, prefix='From')
        to_address.add_to_xml(xml, prefix='To')

        package_weight = etree.SubElement(xml, 'WeightInOunces')
        package_weight.text = str(weight)

        delivery_service = etree.SubElement(xml, 'ServiceType')
        delivery_service.text = service

        self.result = usps.send_request('label', xml)