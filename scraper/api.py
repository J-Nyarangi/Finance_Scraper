from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
from contextlib import contextmanager
from datetime import datetime
import logging
from typing import List, Dict, Any

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration - Consider moving to environment variables
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Truphy@11343',
    'database': 'finance_db',
    'cursorclass': pymysql.cursors.DictCursor  # This will return results as dictionaries
}

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
    except pymysql.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if connection:
            connection.close()

def format_stock_data(row: Dict[str, Any]) -> Dict[str, Any]:
    """Format the stock data for JSON response"""
    try:
        amount_str = row['amount'].replace('$', '')  # Remove the currency symbol
        current_price = float(amount_str)  # Convert to float
    except ValueError:
        current_price = None  

    return {
        "stock_id": row['id'],
        "symbol": row['stock_code'],
        "company_name": row['description'],
        "current_price": current_price,
        "last_updated": row['date']
    }

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Endpoint to fetch all stocks data"""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, stock_code, description,amount, date 
                    FROM stocks
                    ORDER BY stock_code
                """)
                stocks = cursor.fetchall()
                
        return jsonify({
            "status": "success",
            "data": [format_stock_data(stock) for stock in stocks],
            "count": len(stocks)
        })

    except pymysql.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            "status": "error",
            "message": "Database error occurred",
            "error_code": "DB_ERROR"
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred",
            "error_code": "INTERNAL_ERROR"
        }), 500

@app.route('/api/stocks/<symbol>', methods=['GET'])
def get_stock_by_symbol(symbol: str):
    """Endpoint to fetch specific stock data by symbol"""
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, stock_code, description,amount, date 
                    FROM stocks 
                    WHERE stock_code = %s
                """, (symbol.upper(),))
                stock = cursor.fetchone()
                
                if not stock:
                    return jsonify({
                        "status": "error",
                        "message": "Stock not found",
                        "error_code": "NOT_FOUND"
                    }), 404
                
                return jsonify({
                    "status": "success",
                    "data": format_stock_data(stock)
                })

    except pymysql.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({
            "status": "error",
            "message": "Database error occurred",
            "error_code": "DB_ERROR"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "status": "error",
        "message": "Resource not found",
        "error_code": "NOT_FOUND"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "error_code": "INTERNAL_ERROR"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')