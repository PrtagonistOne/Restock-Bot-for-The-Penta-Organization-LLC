import sqlite3

from config.init_logging import init_logging
from config.loggers import get_core_logger

import uuid


init_logging()
logger = get_core_logger()


def add_to_catalog(update, context):
    logger.info('Catalog add db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Adding a product..")

    strings = update.message.text.lower().split()

    if len(strings) == 2:
        strings.remove('/add_to_catalog')
        logger.info(f'Message info: {strings}')
        # Connecting to the SQL database
        conn = sqlite3.connect('list.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS Catalog
                      (Retailer_name TEXT, Product_name TEXT, Stock_status BOOLEAN, Location TEXT, Unique_Id TEXT)''')

        conn.commit()

        unique_id = str(uuid.uuid4())

        c.execute("INSERT INTO Catalog VALUES(?,?,?,?,?)", ('Walmart', 'Lenovo Laptop', True, 3051,
                                                            unique_id.replace('-', '')))

        conn.commit()
        conn.close()

        update.message.reply_text("A product was added to the catalog.")
    else:
        update.message.reply_text("Syntax error. Press /help for more info")


def clear_list(update, context):
    logger.info('Catalog remove all db request')
    context.bot.send_message(chat_id=update.message.chat_id, text="Removing all products..")

    # Connecting to the SQL database
    conn = sqlite3.connect('list.db')
    c = conn.cursor()

    report = "❗Report\n✔️ Items successfully deleted from the catalog.\n"

    c.execute("DELETE FROM Catalog")

    conn.commit()
    conn.close()

    update.message.reply_text(report)


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
            update.message.reply_text(f"RETAILER - {row[0]},\nPRDUCT - {row[1]}\n"
                                      f"STOCK STATUS - {bool(row[2])},\nLOCATION - {row[3]}\n"
                                      f"ID - {row[4]}")
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
