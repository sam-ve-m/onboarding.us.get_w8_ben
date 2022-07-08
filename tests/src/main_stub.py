
stub_w8_response = {
    "result": "https://d1gfu8yyntzl2k.cloudfront.net/02e73c7d-fd38-44f0-acfe-d877de5e037d.pdf",
    "message": "The W8 BEN Link was generated successfully",
    "success": True,
    "code": 0}

jwt_decoded_stub = {
    "user": {
        "unique_id": "40db7fee-6d60-4d73-824f-1bf87edc4491",
        "nick_name": "RAST3",
        "portfolios": {
            "br": {
                "bovespa_account": "000000014-6",
                "bmf_account": "14"
            },
            "us": {
                "dw_account": "89c69304-018a-40b7-be5b-2121c16e109e.1651525277006",
                "dw_display_account": "LX01000001"}
        }}}

stub_dw_link = "https://d1gfu8yyntzl2k.cloudfront.net/02e73c7d-fd38-44f0-acfe-d877de5e037d.pdf"

response_bytes_stub = \
               b'{"result": "https://d1gfu8yyntzl2k.cloudfront.net/02e73c7d-fd38-44f0-acfe-d877de5e037d.pdf", ' \
               b'"message": "The W8 BEN Link was generated ' \
               b'successfully", ' \
               b'"success": true, ' \
               b'"code": 0}'

user_dw_id_stub = '89c69304-018a-40b7-be5b-2121c16e109e'
request_body_stub = ""