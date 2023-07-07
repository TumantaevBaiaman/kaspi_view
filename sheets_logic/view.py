import asyncio
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
import pandas as pd

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = 'sheets_logic/sheets_auth.json'

credentials = sac.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(credentials)


async def gsheet2df(spreadsheet_name, sheet_num) -> dict:
    result: dict = {}
    try:
        sheet = client.open(spreadsheet_name).get_worksheet(sheet_num).get_all_records(numericise_ignore=['all'])
        df = pd.DataFrame.from_dict(sheet)
        result["sheet"] = sheet
        result["df"] = df
        result["status"] = "success"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


async def kaspi_umag_name() -> dict:
    kaspi_umag_sheets_name: str = "Названия Каспи-Umag"
    result: dict = {}

    try:
        result_sheet = await gsheet2df(kaspi_umag_sheets_name, 0)
        result["data"] = {i["Штрихкод"]: i["Название товара  в Umag"] for i in result_sheet}
        result["status"] = "success"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


async def product_name_kaspi() -> dict:
    stock_sheets_name: str = "Склад_export_1678877246390_testing"
    result: dict = {}

    try:
        result_sheet = await gsheet2df(stock_sheets_name, 0)
        if result_sheet["status"] == "success":
            result["data"] = {i["Штрихкод"]: i["Название товара "] for i in result_sheet["sheet"]}
            result["status"] = "success"
        else:
            result["error"] = result_sheet["error"]
            result["status"] = "error"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


async def count_product_kaspi() -> dict:
    stock_sheets_name: str = "Склад_export_1678877246390_testing"
    result: dict = {"data_product": []}
    try:
        result_sheet = await gsheet2df(stock_sheets_name, 0)
        if result_sheet["status"] == "success":
            for product in result_sheet["sheet"]:
                if int(product["Кол-во"]) <= 0:
                    result["data_product"].append(product)
            if len(result["data_product"]) == 0:
                result["count_del"] = 0
            else:
                result["count_del"] = len(result["data_product"])
            result["status"] = "success"
        else:
            result["error"] = result_sheet["error"]
            result["status"] = "error"
    except Exception as ex:
        result["error"] = ex
        result["status"] = "error"

    return result


async def info_del_product() -> dict:
    name_umag: dict = await kaspi_umag_name()
    del_product: dict = await count_product_kaspi()
    result: dict = {
        "ls_del_product": []
    }

    if del_product["status"] == "success":
        if del_product["count_del"] > 0:
            if name_umag["status"] == "success":

                print(del_product["data_product"])
        result["status"]: str = "success"
    else:
        result["status"]: str = "error"

    return result


def main():
    asyncio.run(info_del_product())
