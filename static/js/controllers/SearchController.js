app.controller("SearchController", function(DatabaseService, $scope){
  var url = window.location.pathname;
  var chunks = url.split("/"); // get the id of the beer from the url path
  $scope.searchTerm = chunks[2];
  $scope.maxPage = 10;
  $scope.currentPage = 1;

  $scope.execNewSearch = function(category){
    $scope.currentPage = 1;
    $scope.category = category;
    $scope.getSearchResults();
  }

  $scope.changePage = function(dir){
    var adjustment = dir == "left" ? -1 : 1;
    if($scope.currentPage + adjustment > 0 && $scope.currentPage + adjustment <= $scope.maxPage){
      $scope.currentPage += adjustment;
      $scope.getSearchResults();
    }
  }

  $scope.getSearchResults = function(){
    DatabaseService.search($scope.category, $scope.searchTerm, $scope.currentPage,
      function execNewSearchCallback(resp){
        $scope.data = resp.data;
        $scope.maxPage = resp.data.max_page;
        console.log(resp.data);
        if(!$scope.$$phase){
          $scope.$apply();
        }
    });
  }

  $scope.goToPage = function(page){
    $scope.currentPage = page;
    $scope.getSearchResults();
  }
});
