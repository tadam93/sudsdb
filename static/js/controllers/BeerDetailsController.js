app.controller("BeerDetailsController", function(DatabaseService, $scope){
  var url = window.location.pathname;
  var chunks = url.split("/"); // get the id of the beer from the url path
  $scope.beerId = chunks[2];

  DatabaseService.getBeer($scope.beerId, function(data){
    $scope.beer = data;
  });
});
