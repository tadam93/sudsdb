app.controller("StyleDetailsController", function(DatabaseService, $scope){
  var url = window.location.pathname;
  var chunks = url.split("/"); // get the id of the beer from the url path
  $scope.styleId = chunks[2];

  DatabaseService.getStyle($scope.styleId, function(data){
    $scope.style = data;
    var numBeers = $scope.style.beers.length;
    if(numBeers > 10){
      var nums = [];
      var beers = [];
      while(nums.length < 10){
        var newNum = Math.floor(Math.random() * numBeers);
        if(nums.indexOf(newNum) == -1){
          beers.push($scope.style.beers[newNum]);
          nums.push(newNum);
        }
      }
      $scope.style.beers = beers;
    }
  });
});
