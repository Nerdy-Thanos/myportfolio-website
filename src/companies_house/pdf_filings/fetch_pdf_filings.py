from .ocr_test import convert_to_image
from .parse_pdf_filings import extract_filing_details
from ..ch_object import CompaniesHouseService


def extract_filings_documents(company_number):
    if not company_number:
        return None
    ch = CompaniesHouseService(company_number)
    print(f"FETCHING BYTES FOR COMPANY NUMBER: {company_number}")
    docs_bytes = extract_filing_details(ch, company_number)
    if not docs_bytes:
        return None
    with open("src/webapp/static/output/temp.pdf", "wb") as temp:
        temp.write(docs_bytes)
    ocr_df = ocr_all_filings(docs_bytes, company_number)
    return ocr_df.T


def ocr_all_filings(bytes, company_number):

    print(f"EXTRACTING FIELDS FOR COMPANY NUMBER: {company_number}")
    img = convert_to_image(bytes)
    return img
