import requests
from bs4 import BeautifulSoup
from datetime import datetime
from mysql.connector import connect, Error
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_scraper.log'),
        logging.StreamHandler()
    ]
)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "user",
    "password": "password",
    "database": "finance_db"
}

def initialize_database():
    """Ensure the stock_data table exists."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS stocks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(50) NOT NULL,
    description TEXT,
    amount VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
    try:
        with connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(create_table_query)
                conn.commit()
        logging.info("Database initialized successfully.")
    except Error as e:
        logging.error(f"Error creating table: {e}")

def jinaAI_webapi_scraper(target_url, headers):
    """Scrape the target URL using a web API."""
    api_url = "https://r.jina.ai/"
    response = requests.get(api_url + target_url, headers=headers)
    return response.text

def stock_data(html, stock_code):
    """Extract stock data from HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Extract stock price
    price_tag = soup.find("div", {"class": "YMlKec fxKbKc"})
    price = price_tag.text.strip() if price_tag else "Price not found"

    # Extract description
    description_tag = soup.find("div", {"class": "zzDege"})
    description = description_tag.text.strip() if description_tag else "Description not found"

    # Get the current date when the data is fetched
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "Stock Code": stock_code,
        "Description": description,
        "Amount": price,
        "Date": current_date
    }

def insert_stock_data(stock_info):
    """Insert stock data into the database."""
    insert_query = """
    INSERT INTO stocks (stock_code, description, amount, date)
    VALUES (%s, %s, %s, %s)
    """
    try:
        with connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, (
                    stock_info["Stock Code"],
                    stock_info["Description"],
                    stock_info["Amount"],
                    stock_info["Date"]
                ))
                conn.commit()
        logging.info(f"Inserted stock data for {stock_info['Stock Code']}.")
    except Error as e:
        logging.error(f"Error inserting stock data: {e}")

def main():
    # Initialize the database
    initialize_database()

    # List of stock codes
    stock_codes = [
    # Existing Companies (225)
    "AAPL:NASDAQ", "GOOGL:NASDAQ", "MSFT:NASDAQ", "NVDA:NASDAQ", "TSLA:NASDAQ",
    "AMZN:NASDAQ", "META:NASDAQ", "NFLX:NASDAQ", "ADBE:NASDAQ", "INTC:NASDAQ",
    "AMD:NASDAQ", "CRM:NYSE", "PYPL:NASDAQ", "ORCL:NYSE", "CSCO:NASDAQ",
    "QCOM:NASDAQ", "SHOP:NYSE", "NOW:NYSE", "SQ:NYSE", "DOCU:NASDAQ",
    "JPM:NYSE", "BAC:NYSE", "C:NYSE", "WFC:NYSE", "GS:NYSE",
    "MS:NYSE", "AXP:NYSE", "BLK:NYSE", "COF:NYSE", "SCHW:NYSE",
    "V:NYSE", "MA:NYSE", "TROW:NASDAQ", "BX:NYSE", "KKR:NYSE",
    "WMT:NYSE", "COST:NASDAQ", "TGT:NYSE", "HD:NYSE", "LOW:NYSE",
    "M:NYSE", "KSS:NYSE", "BBY:NYSE", "TJX:NYSE", "ROST:NASDAQ",
    "EL:NYSE", "PG:NYSE", "KO:NYSE", "PEP:NASDAQ", "CL:NYSE",
    "KMB:NYSE", "HSY:NYSE", "GIS:NYSE", "K:NYSE", "CAG:NYSE",
    "JNJ:NYSE", "PFE:NYSE", "MRK:NYSE", "ABBV:NYSE", "BMY:NYSE",
    "LLY:NYSE", "UNH:NYSE", "CVS:NYSE", "HCA:NYSE", "ISRG:NASDAQ",
    "ZTS:NYSE", "VRTX:NASDAQ", "REGN:NASDAQ", "BIIB:NASDAQ", "GILD:NASDAQ",
    "AMGN:NASDAQ", "MDT:NYSE", "SYK:NYSE", "BDX:NYSE", "TMO:NYSE",
    "XOM:NYSE", "CVX:NYSE", "COP:NYSE", "PSX:NYSE", "SLB:NYSE",
    "HAL:NYSE", "BKR:NYSE", "MRO:NYSE", "VLO:NYSE", "EOG:NYSE",
    "PXD:NYSE", "OXY:NYSE", "HES:NYSE", "FANG:NASDAQ", "DVN:NYSE",
    "BA:NYSE", "LMT:NYSE", "GD:NYSE", "RTX:NYSE", "NOC:NYSE",
    "GE:NYSE", "HON:NYSE", "MMM:NYSE", "CAT:NYSE", "DE:NYSE",
    "EMR:NYSE", "ITW:NYSE", "ETN:NYSE", "ROK:NYSE", "DHR:NYSE",
    "FAST:NASDAQ", "UPS:NYSE", "FDX:NYSE", "UNP:NYSE", "CSX:NASDAQ",
    "AMT:NYSE", "PLD:NYSE", "CCI:NYSE", "EQIX:NASDAQ", "PSA:NYSE",
    "SPG:NYSE", "EQR:NYSE", "AVB:NYSE", "O:NYSE", "DLR:NYSE",
    "DIS:NYSE", "NFLX:NASDAQ", "CMCSA:NASDAQ", "CHTR:NASDAQ", "T:NYSE",
    "VZ:NYSE", "TMUS:NASDAQ", "ATVI:NASDAQ", "TTWO:NASDAQ", "EA:NASDAQ",
    "ZM:NASDAQ", "SPOT:NYSE", "RBLX:NYSE", "PINS:NYSE", "TWTR:NYSE",
    "F:NYSE", "GM:NYSE", "TM:NYSE", "HMC:NYSE", "TSLA:NASDAQ",
    "RIVN:NASDAQ", "LCID:NASDAQ", "NIO:NYSE", "XPEV:NYSE", "LI:NASDAQ",
    "DAL:NYSE", "UAL:NASDAQ", "AAL:NASDAQ", "LUV:NYSE", "ALK:NYSE",
    "SAVE:NASDAQ", "HA:NASDAQ", "JBLU:NASDAQ", "RYAAY:NASDAQ", "CPA:NYSE",
    "NEM:NYSE", "FMC:NYSE", "ALB:NYSE", "SCCO:NYSE", "FCX:NYSE",
    "RIO:NYSE", "BHP:NYSE", "VALE:NYSE", "AA:NYSE", "CLF:NYSE",
    "AAPL:NASDAQ", "HPQ:NYSE", "DELL:NYSE", "LEN:NYSE", "HPE:NYSE",
    "STX:NASDAQ", "WDC:NASDAQ", "NTAP:NASDAQ", "CRSR:NASDAQ", "LOGI:NASDAQ",
    "NVDA:NASDAQ", "AMD:NASDAQ", "INTC:NASDAQ", "AVGO:NASDAQ", "TXN:NASDAQ",
    "QCOM:NASDAQ", "ADI:NASDAQ", "MU:NASDAQ", "LRCX:NASDAQ", "KLAC:NASDAQ",
    "PLTR:NYSE", "SNOW:NYSE", "ZS:NASDAQ", "OKTA:NASDAQ", "CRWD:NASDAQ",
    "DDOG:NASDAQ", "MDB:NASDAQ", "TWLO:NYSE", "TTD:NASDAQ", "AFRM:NASDAQ",
    "ROKU:NASDAQ", "YUM:NYSE", "DPZ:NYSE", "SBUX:NASDAQ", "CMG:NYSE",
    "DASH:NYSE", "BROS:NYSE", "MCD:NYSE", "QSR:NYSE", "WING:NASDAQ",
    "PTON:NASDAQ", "NKE:NYSE", "ADDYY:OTC", "LULU:NASDAQ", "VFC:NYSE",
    "TAP:NYSE", "BUD:NYSE", "STZ:NYSE", "SAM:NYSE", "MO:NYSE",
    "PM:NYSE", "CCL:NYSE", "RCL:NYSE", "NCLH:NYSE", "HLT:NYSE",
    "MAR:NASDAQ", "H:NYSE", "WH:NYSE", "IHG:NYSE", "VAC:NYSE",

    # New Additions to Reach 500
    "Z:NASDAQ", "ZG:NASDAQ", "REZI:NYSE", "CHWY:NYSE", "W:NYSE",
    "RH:NYSE", "BBBY:NASDAQ", "WSM:NYSE", "HIBB:NASDAQ", "BJ:NYSE",
    "DLTH:NASDAQ", "OSTK:NASDAQ", "PRTS:NASDAQ", "ETSY:NASDAQ", "REAL:NASDAQ",
    "WAY:NASDAQ", "CVNA:NYSE", "VRTV:NYSE", "PACK:NYSE", "TUP:NYSE",
    "CARR:NYSE", "AAON:NASDAQ", "APOG:NASDAQ", "AWI:NYSE", "FBHS:NYSE",
    "MAS:NYSE", "JELD:NYSE", "MHK:NYSE", "DOOR:NYSE", "SWK:NYSE",
    "TT:NYSE", "GTES:NYSE", "ALLE:NYSE", "BLD:NYSE", "TREX:NYSE",
    "MED:NYSE", "NTRA:NASDAQ", "GH:NASDAQ", "EXAS:NASDAQ", "NVCR:NASDAQ",
    "TNDM:NASDAQ", "LIVN:NASDAQ", "ICUI:NASDAQ", "AXGN:NASDAQ", "HAE:NASDAQ",
    "A:NYSE", "MTD:NYSE", "WAT:NYSE", "PKI:NYSE", "BIO:NYSE",
    "QIAGEN:NYSE", "TECH:NASDAQ", "HOLX:NASDAQ", "RGEN:NASDAQ", "VIVO:NASDAQ",
    "HUBB:NYSE", "DOV:NYSE", "LECO:NASDAQ", "ROK:NYSE", "AME:NYSE",
    "AOS:NYSE", "CIR:NYSE", "NDSN:NASDAQ", "XYL:NYSE", "TSCO:NASDAQ",
    "LZ:NYSE", "MGY:NYSE", "CPE:NYSE", "PBF:NYSE", "MTDR:NYSE",
    "PDCE:NASDAQ", "SM:NYSE", "SBOW:NASDAQ", "EGY:NYSE", "REI:NYSE",
    "OAS:NASDAQ", "TALO:NYSE", "CDEV:NASDAQ", "PTEN:NASDAQ", "HP:NYSE",
    "NBR:NYSE", "NE:NYSE", "DO:NYSE", "ESV:NYSE", "HESM:NYSE",
    "PAA:NYSE", "MPLX:NYSE", "ET:NYSE", "EPD:NYSE", "ENB:NYSE",
    "TRP:NYSE", "OKE:NYSE", "WMB:NYSE", "KMI:NYSE", "AM:NYSE",
    "RTLR:NASDAQ", "CEQP:NYSE", "KNOP:NYSE", "FLNG:NYSE", "DLNG:NASDAQ",
    "GLOP:NYSE", "GLNG:NYSE", "SFL:NYSE", "DAC:NYSE", "GMLP:NASDAQ",
    "CMRE:NYSE", "CPLP:NASDAQ", "NMM:NYSE", "STNG:NYSE", "ASC:NYSE",
    "EURN:NYSE", "DSSI:NYSE", "TNP:NYSE", "INSW:NYSE", "LPG:NYSE",
    "NVGS:NYSE", "GASS:NASDAQ", "BWLL:NYSE", "INTT:NASDAQ", "SPWR:NASDAQ",
    "VSLR:NYSE", "ENPH:NASDAQ", "SEDG:NASDAQ", "FSLR:NASDAQ", "CSIQ:NASDAQ",
    "MAXN:NASDAQ", "ARRY:NASDAQ", "RUN:NASDAQ", "SHLS:NASDAQ", "BLNK:NASDAQ",
    "CHPT:NASDAQ", "VLTA:NASDAQ", "SPKE:NASDAQ", "AMP:NYSE", "AFG:NYSE",
    "MFA:NYSE", "BRMK:NYSE", "TWO:NYSE", "AGNC:NASDAQ", "NLY:NYSE",
    "DX:NYSE", "CHMI:NYSE", "ARR:NYSE", "ORC:NYSE", "IVR:NYSE"
]



    # Fetch and store stock data for each stock code
    for stock_code in stock_codes:
        target_url = f"https://www.google.com/finance/quote/{stock_code}"
        headers = {"User-Agent": "Mozilla/5.0", "X-Return-Format": "html"}
        html = jinaAI_webapi_scraper(target_url, headers)
        stock_info = stock_data(html, stock_code)
        insert_stock_data(stock_info)
        print(stock_info)

if __name__ == "__main__":
    main()
