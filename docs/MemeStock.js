$(document).ready(function() {
  var stocks = [
    ["BABA", 186.41, 3268, "Long"],
    ["MTCH", 28.46, 1434, "Short"],
    ["NFLX", 192.02, 15, "Short"],
    ["SNAP", 12.76, 1599, "Short"],
    ["ALGN", 249.46, 210, "Short"],
    ["JD", 39.96, 6566, "Long"],
    ["FIZZ", 96.41, 120, "Short"]
  ];

  stocks.forEach(function(stock) {
    newStock = `<div id=${stock[0]}><h3>$${stock[0]}</h3><ul><li>Shares: ${
      stock[2]
    }</li><li>Equity: $${(stock[2] * stock[1]).toLocaleString(undefined, {
      minimumFractionDigits: 2
    })}</li><li>Position: ${stock[3]}</li></ul><br>`;
    $("#stocks").append(newStock);
  });
});