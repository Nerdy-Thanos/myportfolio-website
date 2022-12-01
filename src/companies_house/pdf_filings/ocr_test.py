import pytesseract
from pandas import DataFrame, concat
from pdf2image import convert_from_bytes
from PIL import Image
import re

from .consts import get_list_of_coordinates, init_fields

def convert_to_image(path):
    directors, current_cash, prev_cash, current_total_revenue, prev_total_revenue, current_total_turnover, previous_total_turnover, current_uk_revenue, previous_uk_revenue, current_uk_turnover, previous_uk_turnover, possible_cash_pages, possible_total_revenue_pages, possible_revenue_pages = init_fields()
    vat_debtor_ext_curr, vat_debtor_ext_prev = None, None
    vat_creditor_ext_curr, vat_creditor_ext_prev = None, None
    directors=DataFrame()
    cash = DataFrame()
    uk_revenue, uk_turnover = DataFrame(), DataFrame()
    vat_debtor, vat_creditor = DataFrame(), DataFrame() 
    total_revenue, total_turnover = DataFrame(), DataFrame()
    possible_director_pages = [1,2]
    img = convert_from_bytes(path, dpi=400, output_folder="output")

    for page_number, page_data in enumerate(img):
        print(f"EXTRACTING PAGE NUMBER: {page_number}")
        data = pytesseract.image_to_data(page_data, config='--psm 6', output_type=pytesseract.Output.DATAFRAME)
        data = data.dropna()
        
        if page_number in possible_director_pages:
            
            ###########
            
            d_ext_data = extract_directors_from_data(data)
            if not d_ext_data.empty:
                directors = concat([directors, d_ext_data])
            ###########
        if page_number in possible_cash_pages:

            ############
            
            bal_ext_data = extract_cash_balance_from_data(data)
            if not bal_ext_data.empty:
                cash = concat([cash, bal_ext_data])
            ############
        if page_number in possible_total_revenue_pages:

            ############
            
            t_rev_ext= extract_total_revenue_from_data(data)
            t_turn_ext = extract_total_turnover_from_data(data)
            if not t_rev_ext.empty:
                total_revenue = concat([total_revenue, t_rev_ext])
            if not t_turn_ext.empty:
                total_turnover = concat([total_turnover, t_turn_ext])
            ############

        if page_number in possible_revenue_pages:

            ###############
            
            uk_rev_ext = extract_uk_revenue_from_data(data)
            uk_tur_ext = extract_uk_turnover_from_data(data)
            if not uk_rev_ext.empty:
                uk_revenue = concat([uk_revenue, uk_rev_ext])
            if not uk_tur_ext.empty:
                uk_turnover = concat([uk_turnover, uk_tur_ext])

            ###############
        
        #######################
        
        vat_debt_ext = extract_vat_debtor_from_data(data)
        vat_cred_ext = extract_vat_creditor_from_data(data)
        if not vat_debt_ext.empty:
            vat_debtor = concat([vat_debtor, vat_debt_ext])
        if not vat_cred_ext.empty:
            vat_creditor = concat([vat_creditor, vat_cred_ext])
        ######################
         
    current_cash_field, previous_cash_field = extract_cash_values(cash, check=True)
    
    current_total_revenue_field, previous_total_revenue_field = extract_cash_values(total_revenue, check=False)
    
    current_uk_revenue_field, previous_uk_revenue_field = extract_cash_values(uk_revenue, check=False)
    
    current_total_turnover_field, previous_total_turnover_field = extract_cash_values(total_turnover, check=False)

    current_uk_turnover_field, previous_uk_turnover_field = extract_cash_values(uk_turnover, check=False)
    
    current_vat_debtor_field, previous_vat_debtor_field = extract_cash_values(vat_debtor, check=True)
    current_vat_creditor_field, previous_vat_creditor_field = extract_cash_values(vat_creditor, check=True)
    if not directors.empty:
        directors_field = directors["text"].tolist()
    else:
        directors_field=None
    try:
        if current_uk_revenue_field and previous_uk_revenue_field:
            current_overseas_revenue_field = abs(current_total_revenue_field - current_uk_revenue_field)
            previous_overseas_revenue_field = abs(previous_total_revenue_field - previous_uk_revenue_field)
        else:
            current_uk_revenue_field = current_total_revenue_field
            previous_uk_revenue_field = previous_total_revenue_field
            current_overseas_revenue_field=None
            previous_overseas_revenue_field=None
    except:
        current_overseas_revenue_field = None
        previous_overseas_revenue_field = None
        
    try:
        if current_uk_turnover_field and previous_uk_turnover_field:
            current_overseas_turnover_field = abs(current_total_turnover_field - current_uk_turnover_field)
            previous_overseas_turnover_field = abs(previous_total_turnover_field - previous_uk_turnover_field)
        else:
            current_uk_turnover_field = current_total_turnover_field
            previous_uk_turnover_field = previous_total_turnover_field
            current_overseas_turnover_field = None
            previous_overseas_turnover_field=None
    except:
        current_overseas_turnover_field = None
        previous_overseas_turnover_field = None
    
    final_details = {"uk_revenue_current_year":[current_uk_revenue_field],
                    "uk_revenue_prev_year":[previous_uk_revenue_field],
                    "overseas_revenue_current":[current_overseas_revenue_field],
                    "overseas_revenue_prev_year":[previous_overseas_revenue_field],
                    "uk_turnover_current_year":[current_uk_turnover_field],
                    "uk_turnover_prev_year":[previous_uk_turnover_field],
                    "overseas_turnover_current_year":[current_overseas_turnover_field],
                    "overseas_turnover_prev_year":[previous_overseas_turnover_field],
                    "vatdebtor_current_year":[current_vat_debtor_field],
                    "vatdebtor_prev_year":[previous_vat_debtor_field],
                    "vat_creditor_current_year":[current_vat_creditor_field],
                    "vat_creditor_prev_year":[previous_vat_creditor_field],
                    "cash_at_bank_current_year":[current_cash_field],
                    "cash_at_bank_prev_year":[previous_cash_field],
                    "directors":[directors_field]}
    return DataFrame(final_details)

def extract_uk_revenue_from_data(data):
    if data.empty:
        return DataFrame()
    notes_index = data.loc[data["text"].str.contains(r"(?:notes)",regex=True, flags=re.IGNORECASE)==True]
    if not notes_index.empty:
        revenue_index = data.loc[data["text"].str.contains(r"(?:revenue)",regex=True, flags=re.IGNORECASE)==True]
        if not revenue_index.empty:
            uk_revenue_df = data.loc[data["text"].str.contains(r"(?:United|Kingdom)",regex=True, flags=re.IGNORECASE)==True]
            if not uk_revenue_df.empty:
                if len(uk_revenue_df)<2:
                    return DataFrame()
                uk_revenue_coordinates = int(uk_revenue_df["top"].iloc[0])
                coordinates_list = get_list_of_coordinates(uk_revenue_coordinates)
                uk_revenue_values = data.loc[data["top"].isin(coordinates_list)]
                return uk_revenue_values
            return DataFrame()
        return DataFrame()
    return DataFrame()

def extract_uk_turnover_from_data(data):
    if data.empty:
        return DataFrame()
    notes_index = data.loc[data["text"].str.contains(r"(?:notes)",regex=True, flags=re.IGNORECASE)==True]
    if not notes_index.empty:
        turnover_index = data.loc[data["text"].str.contains(r"(?:turnover)",regex=True, flags=re.IGNORECASE)==True]
        if not turnover_index.empty:
            uk_turnover_df = data.loc[data["text"].str.contains(r"(?:United|Kingdom)",regex=True, flags=re.IGNORECASE)==True]
            if not uk_turnover_df.empty:
                if len(uk_turnover_df)<2:
                    return DataFrame()
                uk_turnover_coordinates = int(uk_turnover_df["top"].iloc[0])
                coordinates_list = get_list_of_coordinates(uk_turnover_coordinates)
                uk_turnover_values = data.loc[data["top"].isin(coordinates_list)]
                return uk_turnover_values
            return DataFrame()
        return DataFrame()
    return DataFrame()

def extract_vat_debtor_from_data(data):
    if data.empty:
        return DataFrame()
    debtor_index = data.loc[data["text"].str.contains(r"(?:debtor|debtors|receivables|recoverables)",regex=True, flags=re.IGNORECASE)==True]
    creditor_index = data.loc[data["text"].str.contains(r"(?:creditor|creditors|payables)",regex=True, flags=re.IGNORECASE)==True]
    if not debtor_index.empty and not creditor_index.empty:
        vat_debt = data.loc[debtor_index.index[0] + 1:creditor_index.index[0]]
        if not vat_debt.empty:
            vat_df = vat_debt.loc[vat_debt["text"].str.contains(r"(?:VAT)",regex=True)==True]
            if not vat_df.empty:
                vat_line = vat_df["line_num"].iloc[-1]
                vat = data.loc[data["line_num"]==vat_line]
                vat_values = vat.tail(2)
                return vat_values
            return DataFrame()
        return DataFrame()
    return DataFrame()

def extract_vat_creditor_from_data(data):
    if data.empty:
        return DataFrame()
    creditor_index = data.loc[data["text"].str.contains(r"(?:creditor|creditors|payables)",regex=True, flags=re.IGNORECASE)==True]
    if not creditor_index.empty:
        vat_cred = data.loc[creditor_index.index[0] + 1:]
        if not vat_cred.empty:
            vat_df = vat_cred.loc[vat_cred["text"].str.contains(r"(?:VAT)",regex=True)==True]
            if not vat_df.empty:
                vat_line = vat_df["line_num"].iloc[-1]
                vat = data.loc[data["line_num"]==vat_line]
                vat_values = vat.tail(2)
                return vat_values
            return DataFrame()
        return DataFrame()
    return DataFrame()


def extract_total_revenue_from_data(data):
    if data.empty:
        return DataFrame()
    income_index = data.loc[data["text"].str.contains(r"(?:income|earning)", regex=True, flags=re.IGNORECASE)==True]
    if not income_index.empty:
        revenue_df = data.loc[data["text"].str.contains(r"(?:revenue)", regex=True, flags=re.IGNORECASE)==True]
        if not revenue_df.empty:
            revenue_coordinates = int(revenue_df["top"].iloc[0])
            coordinates_list = get_list_of_coordinates(revenue_coordinates)
            revenue_values = data.loc[data["top"].isin(coordinates_list)]
            return revenue_values
        return DataFrame()
    return DataFrame()

def extract_total_turnover_from_data(data):
    if data.empty:
        return DataFrame()
    income_index = data.loc[data["text"].str.contains(r"(?:income|earning)", regex=True, flags=re.IGNORECASE)==True]
    if not income_index.empty:
        turnover_df = data.loc[data["text"].str.contains(r"(?:turnover)", regex=True, flags=re.IGNORECASE)==True]
        if not turnover_df.empty:
            turnover_coordinates = int(turnover_df["top"].iloc[0])
            coordinates_list = get_list_of_coordinates(turnover_coordinates)
            turnover_values = data.loc[data["top"].isin(coordinates_list)]
            return turnover_values
        return DataFrame()
    return DataFrame()


def extract_cash_balance_from_data(data):
    if data.empty:
        return DataFrame()
    current_index = data.loc[data["text"].str.contains(r"(?:current)", regex=True, flags=re.IGNORECASE)==True]
    if not current_index.empty:
        cash_df = data.loc[data["text"].str.contains(r"(?:cash)", regex=True, flags=re.IGNORECASE)==True]
        hand_bank = data.loc[data["text"].str.contains(r"(?:hand|bank|equivalent)", regex=True, flags=re.IGNORECASE)==True]
    
        if not cash_df.empty and not hand_bank.empty:
            cash_line=cash_df["line_num"].iloc[-1]
            hand_line = hand_bank["line_num"].iloc[-1]
            if cash_line==hand_line:
                cash = data.loc[data["line_num"]==cash_line]
                cash_values = cash.tail(2)
                return cash_values
            return DataFrame()
        return DataFrame()
    return DataFrame()

def extract_directors_from_data(data):
    if data.empty:
        return DataFrame()
    director_index = data.loc[data["text"].str.contains(r"(?:director|directors)", regex=True, flags=re.IGNORECASE)==True]
    company_index = data.loc[data["text"].str.contains(r"(?:registered)", regex=True, flags=re.IGNORECASE)==True]

    if not director_index.empty and not company_index.empty:
        directors = data.loc[director_index.index[0] + 1 : company_index.index[0]]
    else:
        directors = DataFrame()
    return directors


def extract_cash_values(values: DataFrame, check: bool=False):


    if values.empty:
        return None, None
    if not check:
        values = values.sort_values(by="left", ascending=True).reset_index()
    values_list = values["text"].tolist()
    values_string = ' '.join(str(v) for v in values_list)

    cur,prev = get_amount_regex(values_string, check_flag=check)
    
    try:
        cur_str = cur.replace(",","")
        current_value=float(cur_str)
    except Exception as e:
        current_value=None
    try:
        prev_str = prev.replace(",","")
        previous_value = float(prev_str)
    except Exception as e:
        previous_value=None
    
    return current_value, previous_value

    
def get_amount_regex(string, check_flag:bool=False):
    regex = re.compile("(?:[0-9]{1,3},([0-9]{3},)*[0-9]{3}|(?:-))")
    if check_flag:
        regex = re.compile("(?:[0-9]{1,3},([0-9]{3},)*[0-9]{3}|(?:[0-9]{2,3})|(?:-))")
    groups = re.finditer(regex, string)
    cur=None
    prev=None
    amount=[]
    if groups:
        for g in groups:
            amount.append(g.group(0))
    if amount:
        try:
            cur=amount[0]
        except Exception as e:
            cur=None 
        try:   
            prev=amount[1]
        except Exception as e:
            prev=None
        return cur, prev
    return cur, prev

