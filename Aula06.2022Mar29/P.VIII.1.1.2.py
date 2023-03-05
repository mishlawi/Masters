import requests
import sys
from cryptography import x509


args = len(sys.argv)
if args > 1:
    cert_name = sys.argv[1]
    f = open(cert_name, 'rb')
    cer_data =  f.read()
    f.close()


    crl_url = x509.load_der_x509_certificate(cer_data).extensions.get_extension_for_class(x509.CRLDistributionPoints).value._distribution_points[0].full_name[0].value

    URL = crl_url
    response = requests.get(URL)

    crl = x509.load_der_x509_crl(response.content)

    print(crl.last_update)
    print(crl.next_update)

    revoked = crl.get_revoked_certificate_by_serial_number(x509.load_der_x509_certificate(cer_data).serial_number)

    print('URL da CRL:', crl_url)
    print('CRL last_update', crl.last_update)
    print('CRL next_update:', crl.next_update)

    if revoked != None:
        print(f'{cert_name}: Revoked')
        print('Revocation Date:',revoked.revocation_date)
    else:
        print('Cert Status: good')
else:
    print('Too few arguments! Please enter the certificate file name.')