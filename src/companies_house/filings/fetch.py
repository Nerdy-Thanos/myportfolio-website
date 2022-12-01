"""Functions for fetching filings from companies house."""
from ..ch_object import CompaniesHouseService


def get_filings_details(ch: CompaniesHouseService) -> dict:
    """
    Get all ixbrl documents for a company from companies house.

    Args:
        company_number (str): Companies house number of the company

    Returns:
        dict: Dictionary of all ixbrl documents for the company
              {"date": [], "category":[], "description": [], "links": []}
    """
    url = f"{ch.company_url}{ch.ch_number}/filing-history"
    parameters = {"items_per_page": 1000, "category": "accounts", "type": "AA"}

    whole_query = ch.query_ch_api(url, "filing_history", parameters=parameters)
    table = {
        "date": [],
        "category": [],
        "description": [],
        "transaction_id": [],
        "links": [],
        "document_metadata": [],
    }

    if "items" in whole_query:
        for item in whole_query["items"]:
            if item["type"] == "AA":
                [
                    table[key].append(value)
                    for key, value in item.items()
                    if key in table.keys()
                ]

        return table
    else:
        return False
