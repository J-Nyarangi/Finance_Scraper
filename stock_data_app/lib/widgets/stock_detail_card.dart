import 'package:flutter/material.dart';
import '../models/stock.dart';
import 'package:intl/intl.dart';

class StockDetailCard extends StatelessWidget {
  final Stock stock;

  const StockDetailCard({
    Key? key,
    required this.stock,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20), // Rounded corners
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.2),
              spreadRadius: 2,
              blurRadius: 6,
              offset: const Offset(0, 4), // Shadow positioning
            ),
          ],
        ),
        padding: const EdgeInsets.all(20), // Inner padding
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              stock.companyName,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Colors.pink,
                  ),
            ),
            const SizedBox(height: 20),
            _buildInfoRow('Stock ID', stock.stockId.toString(), context),
            _buildInfoRow('Symbol', stock.symbol, context),
            _buildInfoRow(
              'Current Price',
              '\$${stock.currentPrice?.toStringAsFixed(2) ?? 'N/A'}',
              context,
            ),
            _buildInfoRow(
              'Last Updated',
              stock.lastUpdated != null
                  ? DateFormat('EEE, dd MMM yyyy HH:mm:ss').format(stock.lastUpdated!)
                  : 'N/A',
              context,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(String label, String value, BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  fontWeight: FontWeight.w600,
                  color: Colors.grey.shade600,
                ),
          ),
          Text(
            value,
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
          ),
        ],
      ),
    );
  }
}
