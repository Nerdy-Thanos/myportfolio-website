from pandas import DataFrame
import io
import base64
from pathlib import Path

from src.companies_house.ch_object import CompaniesHouseService
from src.companies_house.filings.fetch import get_filings_details


def extract_filing_details(ch: CompaniesHouseService, company_number) -> dict:
    """
    Extract details from ixbrl filing documents.
    NOTE: We can use the api but since it works differently to every other hmrc api we will scrape it instead.
    https://developer-specs.company-information.service.gov.uk/document-api/reference/document-location/fetch-a-document

    Returns:
        dict: Dictionary of all ixbrl documents for the company
              {"date": [], "category":[], "description": [], "url": []}
    """
    documents = get_filings_details(ch)
    content_bytes = bytearray()
    if documents["transaction_id"]:
        parameters = {"format": "pdf", "download": 1}
        base_url = "https://find-and-update.company-information.service.gov.uk/company/"

        transaction_id = documents["transaction_id"][0]
        print(f"extracting document {transaction_id}")
        url = f"{base_url}{ch.ch_number}/filing-history/{transaction_id}/document"
        content = ch.query_ch_document_api(
            url, "document", parameters=parameters, extract=False
        )
        content_bytes += content
        if len(content_bytes) == 0:
            print(f"Document not found")
            return None
        return content_bytes
    return None
