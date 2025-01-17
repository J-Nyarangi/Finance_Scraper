import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/stock.dart';

class StockService {
  final String baseUrl = 'http://192.168.1.228:8000/api';

  Future<List<Stock>> getAllStocks() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/stocks'));
      
      if (response.statusCode == 200) {
        final Map<String, dynamic> body = json.decode(response.body);
        final List<dynamic> stocksJson = body['data'];
        return stocksJson.map((json) => Stock.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load stocks: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');

    }
  }

  Future<Stock> getStockBySymbol(String symbol) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/stocks/$symbol'));
      
      if (response.statusCode == 200) {
        final Map<String, dynamic> body = json.decode(response.body);
        return Stock.fromJson(body['data']);
      } else {
        throw Exception('Failed to load stock: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Network error: $e');
    }
  }
}