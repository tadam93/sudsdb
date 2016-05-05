app.factory("BreweryFactory", function(){
  var breweryFactory = this;

  breweryFactory.buildBrewery = function(id, name, location, brewingSince, isOrganic, website, icon){
    var brewery = {
      id: id,
      name: name,
      location: location,
      brewingSince: brewingSince,
      isOrganic: isOrganic,
      website: website,
      icon: icon
    };

    return brewery;
  }
  return breweryFactory;
});
