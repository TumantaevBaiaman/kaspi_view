import asyncio
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = 'sheets_logic/sheets_auth.json'

credentials = sac.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(credentials)


async def gsheet2df(spreadsheet_name, sheet_num):

    sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records(numericise_ignore=['all'])
    df = pd.DataFrame.from_dict(sheet)
    return sheet


async def kaspi_umag_name():
    kaspi_umag_sheets_name = "Названия Каспи-Umag"
    result = {}

    try:
        result_sheet = await gsheet2df(kaspi_umag_sheets_name, 0)
        result["data"] = {i["Штрихкод"]: i["Название товара  в Umag"] for i in result_sheet}
        result["status"] = "success"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


async def product_name_kaspi():
    stock_sheets_name = "Склад_export_1678877246390_testing"
    result = {}

    try:
        result_sheet = await gsheet2df(stock_sheets_name, 0)
        result["data"] = {i["Штрихкод"]: i["Название товара "] for i in result_sheet}
        result["status"] = "success"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


async def count_product_kaspi():
    stock_sheets_name = "Склад_export_1678877246390_testing"
    result = {"data_product": []}
    try:
        result_sheet = await gsheet2df(stock_sheets_name, 0)
        for product in result_sheet:
            if int(product["Кол-во"])<=0:
                result["data_product"].append(product)
        if len(result["data_product"]) == 0:
            result["count_del"] = 0
        else:
            result["count_del"] = len(result["data_product"])
        result["status"] = "success"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


def main():
    print(asyncio.run(count_product_kaspi()))
