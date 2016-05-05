app.factory("BeerFactory", function(){
  var beerFactory = this;

  beerFactory.buildBeer = function(id, name, style, brewery, abv, ibu){
    var beer = {
      id: id,
      name: name,
      style: style,
      brewery: brewery,
      abv: abv,
      ibu: ibu
    };

    return beer;
  }
  return beerFactory;
});
