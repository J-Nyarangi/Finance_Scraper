import 'package:intl/intl.dart';

class Stock {
  final int stockId;
  final String symbol;
  final String companyName;
  final double? currentPrice;
  final DateTime? lastUpdated;


  Stock({
    required this.stockId,
    required this.symbol,
    required this.companyName,
    this.currentPrice,
    this.lastUpdated,
  });

  factory Stock.fromJson(Map<String, dynamic> json) {
    return Stock(
      stockId: json['stock_id'],
      symbol: json['symbol'],
      companyName: json['company_name'],
      currentPrice: json['current_price'] != null ? double.tryParse(json['current_price'].toString()) : null,
      lastUpdated: json['last_updated'] != null 
        ? DateFormat('EEE, dd MMM yyyy HH:mm:ss zzz').parse(json['last_updated'])
        : null,
    );
  }
}
