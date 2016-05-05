
  app.controller("BeerListingsController", function(DatabaseService, $scope){
    $scope.sortCol = "beer.name";
    $scope.sortDir = "asc";
    $scope.currentPage = 1;
    $scope.maxPage = 10;
    $scope.loading = true;

    DatabaseService.getBeerListings($scope.currentPage, $scope.sortCol, $scope.sortDir, function(data){
      $scope.beers = data.beers_sorted;
      $scope.maxPage = data.count;
      $scope.loading = false;
    });

    $scope.applySort = function(column){
      if($scope.loading){
        return;
      }
      $scope.loading = true;
      if($scope.sortCol == column){
        $scope.sortDir = $scope.sortDir == "desc" ? "asc" : "desc";
      }else{
        $scope.sortCol = column;
        $scope.sortDir = "desc";
      }
      DatabaseService.getBeerListings($scope.currentPage, $scope.sortCol, $scope.sortDir, function(data){
        $scope.beers = data.beers_sorted;
        $scope.maxPage = data.count;
        $scope.loading = false;
      });
    }

    $scope.changePage = function(dir){
      if($scope.loading){
        return;
      }
      $scope.loading = true;
      $scope.currentPage += dir == "left" ? ($scope.currentPage - 1 > 0 ? - 1 : 0 ) : ($scope.currentPage + 1 <= $scope.maxPage ? 1 : 0 );
      DatabaseService.getBeerListings($scope.currentPage, $scope.sortCol, $scope.sortDir, function(data){
        $scope.beers = data.beers_sorted;
        $scope.maxPage = data.count;
        $scope.loading = false;
      });
    }

    $scope.goToPage = function(page){
      $scope.currentPage = page;
      $scope.loading = true;
      DatabaseService.getBeerListings($scope.currentPage, $scope.sortCol, $scope.sortDir, function(data){
        $scope.beers = data.beers_sorted;
        $scope.maxPage = data.count;
        $scope.loading = false;
      });
    }
  });
