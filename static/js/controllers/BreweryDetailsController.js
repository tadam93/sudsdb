app.controller("BreweryDetailsController", function(DatabaseService, $scope){
  var url = window.location.pathname;
  var chunks = url.split("/"); // get the id of the beer from the url path
  $scope.breweryId = chunks[2];

  DatabaseService.getBrewery($scope.breweryId, function(data){
    console.log(data);
    $scope.brewery = data;
    $('iframe').attr("src", 'https://www.google.com/maps/embed/v1/place?q=' + $scope.brewery.name + '&zoom=17&key=AIzaSyA_qj2Y6KHUXnfqDOL4ivsPWEI6dE2KmeM');
  });
});
