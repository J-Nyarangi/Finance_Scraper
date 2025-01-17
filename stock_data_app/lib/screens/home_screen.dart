import 'package:flutter/material.dart';
import '../models/stock.dart';
import '../services/stock_service.dart';
import '../widgets/stock_list_item.dart';
import 'stock_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final StockService _stockService = StockService();
  List<Stock> _stocks = [];
  List<Stock> _filteredStocks = [];
  bool _isLoading = true;
  String _error = '';
  String searchQuery = '';
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadStocks();
  }

  Future<void> _loadStocks() async {
    try {
      setState(() => _isLoading = true);
      final stocks = await _stockService.getAllStocks();
      setState(() {
        _stocks = stocks;
        _filteredStocks = stocks;
        _isLoading = false;
        _error = '';
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  void _filterStocks(String query) {
    final filtered = _stocks.where((stock) {
      return stock.companyName.toLowerCase().contains(query.toLowerCase()) ||
          stock.symbol.toLowerCase().contains(query.toLowerCase());
    }).toList();
    setState(() {
      searchQuery = query;
      _filteredStocks = filtered;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Stock Tracker'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadStocks,
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.white, // Background color for search bar
                borderRadius: BorderRadius.circular(20), // Rounded corners
                boxShadow: [
                  BoxShadow(
                    color: Colors.grey.withOpacity(0.3),
                    spreadRadius: 2,
                    blurRadius: 5,
                    offset: const Offset(0, 2), // Shadow positioning
                  ),
                ],
              ),
              child: TextField(
                controller: _searchController,
                decoration: const InputDecoration(
                  hintText: 'Search Stocks',
                  prefixIcon: Icon(Icons.search, color: Colors.grey),
                  border: InputBorder.none, // Remove border
                  contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
                onChanged: _filterStocks,
              ),
            ),
          ),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _error.isNotEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(_error, style: const TextStyle(color: Colors.red)),
                            ElevatedButton(
                              onPressed: _loadStocks,
                              child: const Text('Retry'),
                            ),
                          ],
                        ),
                      )
                    : _filteredStocks.isEmpty
                        ? const Center(
                            child: Text(
                              'No stocks found.',
                              style: TextStyle(fontSize: 18, color: Colors.grey),
                            ),
                          )
                        : RefreshIndicator(
                            onRefresh: _loadStocks,
                            child: ListView.separated(
                              itemCount: _filteredStocks.length,
                              separatorBuilder: (context, index) => const Divider(
                                thickness: 0.8,
                                color: Colors.grey,
                                indent: 16,
                                endIndent: 16,
                                height: 0,
                              ),
                              itemBuilder: (context, index) {
                                final stock = _filteredStocks[index];
                                return StockListItem(
                                  stock: stock,
                                  onTap: () => Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => StockDetailScreen(symbol: stock.symbol),
                                    ),
                                  ),
                                );
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}
