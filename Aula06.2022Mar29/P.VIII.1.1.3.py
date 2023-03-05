import base64
import requests
import sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.x509 import ocsp
from urllib.parse import urljoin
from cryptography import x509


args = len(sys.argv)
if args > 1:
    cert_name = sys.argv[1]
    f = open(cert_name, 'rb')
    cer_data =  f.read()
    f.close()
    cert = x509.load_der_x509_certificate(cer_data)

    issuer_cer = sys.argv[2]
    f = open(issuer_cer, 'rb')
    issuer_data =  f.read()
    f.close()
    issuer_cert = x509.load_der_x509_certificate(issuer_data)
    
    ocsp_url = cert.extensions.get_extension_for_class(x509.AuthorityInformationAccess)._value._descriptions[0].access_location.value
    
    builder = ocsp.OCSPRequestBuilder()
    req = builder.add_certificate(cert,issuer_cert,hashes.SHA256()).build()
    req_path = base64.b64encode(req.public_bytes(serialization.Encoding.DER))
    ocsp_requestencoded = urljoin(ocsp_url + '/', req_path.decode('ascii'))
    
    ocsp_resp = requests.get(ocsp_requestencoded)
    ocsp_decoded = ocsp.load_der_ocsp_response(ocsp_resp.content)
    if ocsp_decoded.response_status:
        print('URL do OCSP:', ocsp_url)
        print('OCSP Server Response Date:', ocsp_decoded.produced_at)
        print('Cert Status:', ocsp_decoded.certificate_status.name)
        if ocsp_decoded.certificate_status.name == 'REVOKED':
            print('Revocation date:', ocsp_decoded.revocation_time)
    else:
        print(f"OCSP Response Status: {ocsp_decoded.response_status}")
else:
    print('Too few arguments! Please enter the certificate file name to check and the issuer certificate file name.')