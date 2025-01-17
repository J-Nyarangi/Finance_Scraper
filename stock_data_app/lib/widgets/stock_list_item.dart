import 'package:flutter/material.dart';
import '../models/stock.dart';

class StockListItem extends StatelessWidget {
  final Stock stock;
  final VoidCallback onTap;

  const StockListItem({
    Key? key,
    required this.stock,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Improved avatar color generation based on the stock symbol
    Color _getAvatarColor(String symbol) {
      final int hash = symbol.hashCode;
      final double hue = (hash % 360).toDouble();
      return HSLColor.fromAHSL(0.8, hue, 0.6, 0.6).toColor();
    }

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: ListTile(
        onTap: onTap,
        leading: CircleAvatar(
          backgroundColor: _getAvatarColor(stock.symbol),
          child: Text(
            stock.symbol[0],
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
          ),
        ),
        title: Text(
          stock.companyName,
          style: Theme.of(context).textTheme.bodyLarge,
        ),
        subtitle: Text(
          stock.symbol,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey),
        ),
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      ),
    );
  }
}
