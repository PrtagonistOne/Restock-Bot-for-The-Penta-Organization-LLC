import sqlite3

from config.init_logging import init_logging
from config.loggers import get_core_logger
import datetime

import uuid

from utils.retailer_utils.BBB_handlers import get_bbb_shipment_status
from utils.retailer_utils.home_depot_handlers import get_hd_shipment_status

init_logging()
logger = get_core_logger()


def cursor_connection():
    # Connecting to the SQL database
    conn = sqlite3.connect('list.db')
    return conn.cursor(), conn


def table_init_check():
    c, conn = cursor_connection()
    c.execute('''CREATE TABLE IF NOT EXISTS Catalog
                              (Retailer_name TEXT, Product_name TEXT, Location TEXT, Stock_status TEXT,
                              Shipping_details TEXT, Unique_Id TEXT, Date_Created timestamp)''')
    conn.commit()
    conn.close()


def check_for_the_same_entry(product, zip, c):
    query = f"""SELECT COUNT(*)
                FROM Catalog
                WHERE Product_name IN ('{product}')
                and Location in ('{zip}')"""

    flag = c.execute(query).fetchall()[0][0]
    return flag == 0


def create_entry_query(retailer, product, location, in_stock, shipping, product_id: str = None):
    if product_id is None:
        product_id = str(uuid.uuid4()).replace('-', '')

    table_init_check()
    c, conn = cursor_connection()
    c.execute("INSERT INTO Catalog VALUES(?,?,?,?,?,?,?)", (retailer, product, location, in_stock, shipping,
                                                            product_id, datetime.datetime.now()))
    conn.commit()
    conn.close()
    return product_id

def delete_all_entries():
    c, conn = cursor_connection()
    c.execute("DELETE FROM Catalog")

    conn.commit()
    conn.close()


def add_HD_to_catalog(update, context):
    logger.info('Catalog add db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Adding a product for Home Depot..")

    strings = update.message.text.lower().split()
    logger.info(f'Message info: {strings}')

    if len(strings) >= 2:
        strings.remove('/add_hd_to_catalog')
        logger.info(f'Message info: {strings}')

        c, _ = cursor_connection()
        if check_for_the_same_entry(strings[0], strings[1], c):
            ret_name, prod_name, location, in_stock, shipping = get_hd_shipment_status(strings[0], strings[1])

            product_id = create_entry_query(ret_name, prod_name, location, in_stock, shipping)

            update.message.reply_text("A product was added to the catalog.")
            show_one_record(update, context, product_id)
        else:
            update.message.reply_text("This item already added.")
    else:
        update.message.reply_text("Syntax error. Press /help for more info")


def add_bbb_to_catalog(update, context):
    logger.info('Catalog add db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Adding a product for Bed Bath and Beyond..")

    strings = update.message.text.lower().split()
    logger.info(f'Message info: {strings}')

    if len(strings) >= 2:
        strings.remove('/add_bbb_to_catalog')
        logger.info(f'Message info: {strings}')

        c, _ = cursor_connection()
        if check_for_the_same_entry(strings[0], strings[1], c):
            ret_name, prod_name, location, in_stock, shipping = get_bbb_shipment_status(strings[0], strings[1])

            product_id = create_entry_query(ret_name, prod_name, location, in_stock, shipping)

            update.message.reply_text("A product was added to the catalog.")
            show_one_record(update, context, product_id)
        else:
            update.message.reply_text("This item already added.")
    else:
        update.message.reply_text("Syntax error. Press /help for more info")


def clear_list(update, context):
    logger.info('Catalog remove all db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Removing all products..")
    strings = update.message.text.lower().split()

    if len(strings) == 2 and strings[1] == '!!!':
        # Connecting to the SQL database

        report = "❗Report\n✔️ Items successfully deleted from the catalog.\n"
        delete_all_entries()
        update.message.reply_text(report)
    else:
        update.message.reply_text("Syntax error. Press /help for more info")


def show_one_record(update, context, product_id):
    logger.info('Catalog shows added product')
    context.bot.send_message(chat_id=update.message.chat_id, text="Showing added product..")

    # Connecting to the SQL database
    c, conn = cursor_connection()

    c.execute("SELECT * FROM Catalog WHERE Unique_Id=?", (product_id,))

    row = c.fetchall()[0]
    conn.close()

    update.message.reply_text(f"RETAILER - {row[0]}\nPRODUCT - {row[1]}\n"
                              f"LOCATION - {row[2]}\nSTOCK - {row[3]}\n"
                              f"Type of Shipping - {row[4]}\n\nTIME ADDED - {row[6]}"
                              f"\nID - {row[5]}\n")


def show_list(update, context):
    logger.info('Catalog showing all products db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Showing all products..")

    # Connecting to the SQL database
    conn = sqlite3.connect('list.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Catalog")
    rows = c.fetchall()
    conn.close()
    if len(rows) > 0:
        logger.info(rows)
        for row in rows:
            update.message.reply_text(f"RETAILER - {row[0]}\nPRODUCT - {row[1]}\n"
                                      f"LOCATION - {row[2]}\nSTOCK - {row[3]}\n"
                                      f"Type of Shipping - {row[4]}\n\nTIME ADDED - {row[6]}"
                                      f"\nID - {row[5]}\n")
    else:
        update.message.reply_text("No items in the catalog.")


def remove_from_list(update, context):
    logger.info('Reming a item from a catalog db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Removing an Item..")

    strings = update.message.text.lower().split()

    if len(strings) == 2:
        strings.remove('/remove_from_catalog')

        # Connecting to the SQL database
        conn = sqlite3.connect('list.db')
        c = conn.cursor()

        report = "❗Report\n✔️ Items successfully deleted from your list:\n"

        query = "DELETE FROM Catalog WHERE Unique_Id = '" + strings[0] + "' "
        c.execute(query)

        conn.commit()
        conn.close()

        update.message.reply_text(report)
    else:
        update.message.reply_text("Syntax error. Press /help for more info")
