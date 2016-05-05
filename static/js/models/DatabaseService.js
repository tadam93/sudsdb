
 app.service("DatabaseService", function(BeerFactory, BreweryFactory, StyleFactory, $http){
     var dbService = this;

    /*
      Queries the api and returns a listing of beers
      page is the page to gather the listings from
      limit is the number of listings to gather
    */
    dbService.getBeerListings = function(page, sortCol, sortDir, callback){
      beers = {};
      //todo: connect with ajax
      $http({
        method: 'GET',
        url: '/api/beers/get_num',
      }).then(function successCallback(response) {
        beers.count = response.data.beers_get_num;
        $http({
          method: 'GET',
          url: '/api/beers/' + page + '/sort/' + sortCol + '/' + sortDir + '',
        }).then(function successCallback(response) {
            beers.beers_sorted = response.data.beers_sorted;
            if(callback){
              callback(beers);
            }
          }, function errorCallback(response) {
            console.log(response);
        });
      });
    }
    dbService.getNumBeers = function(cb){
      $http({
        method: 'GET',
        url: '/api/beers/get_num',
      }).then(function successCallback(response) {
        if(cb){
          cb(response.data)
        }
      });
    }

    dbService.getBeer = function(beer_id, callback){
      $http({
        method: 'GET',
        url: '/api/beers/' + beer_id
      }).then(function successCallback(response) {
          if(callback){
            callback(response.data.beer);
          }
        }, function errorCallback(response) {
          console.log(response);
          if(callback){
            callback(response);
          }
      });
    }

    dbService.getBreweryListings = function(page, sortCol, sortDir, callback){
      breweries = {};
      //todo: connect with ajax
      $http({
        method: 'GET',
        url: '/api/breweries/get_num',
      }).then(function successCallback(resp) {
        breweries.count = resp.data.breweries_get_num;
        $http({
          method: 'GET',
          url: '/api/breweries/' + page + '/sort/' + sortCol + '/' + sortDir + '',
        }).then(function successCallback(response) {
            breweries.breweries_sorted = response.data.breweries_sorted;
            if(callback){
              callback(breweries);
            }
          }, function errorCallback(response) {
            console.log(response);
        });
      })
    }

    dbService.getNumBreweries = function(cb){
      $http({
        method: 'GET',
        url: '/api/breweries/get_num',
      }).then(function successCallback(response) {
        if(cb){
          cb(response.data)
        }
      });
    }

    dbService.getBrewery = function(brewery_id, callback){
      $http({
        method: 'GET',
        url: '/api/breweries/' + brewery_id
      }).then(function successCallback(response) {
          if(callback){
            callback(response.data.brewery);
          }
        }, function errorCallback(response) {
          console.log(response);
          if(callback){
            callback(response);
          }
      });
    }

    dbService.getStyleListings = function(page, sortCol, sortDir, callback){
      data = {};
      //todo: connect with ajax
      $http({
        method: 'GET',
        url: '/api/styles/get_num',
      }).then(function (resp){
        data.count = resp.data.styles_get_num;
        $http({
          method: 'GET',
          url: '/api/styles/' + page + '/sort/' + sortCol + '/' + sortDir + '',
        }).then(function successCallback(response) {
            data.styles_sorted  = response.data.styles_sorted;
            console.log(data);
            if(callback){
              callback(data);
            }
          }, function errorCallback(response) {
            console.log(response);
          });
      })
    }

    dbService.getNumStyles = function(cb){
      $http({
        method: 'GET',
        url: '/api/styles/get_num',
      }).then(function successCallback(response) {
        if(cb){
          cb(response.data)
        }
      });
    }


    dbService.getStyle = function(style_id, callback){
      $http({
        method: 'GET',
        url: '/api/styles/' + style_id
      }).then(function successCallback(response) {
          if(callback){
            callback(response.data.style);
          }
        }, function errorCallback(response) {
          console.log(response);
          if(callback){
            callback(response);
          }
        });
    }

    dbService.search = function(category, terms, page, callback){
      data = {};
      //todo: connect with ajax
      $http({
        method: 'GET',
        url: '/search/' + category + '/' + terms + '/' + --page,
      }).then(function (resp){
        if(callback){
          callback(resp);
        }
      })
    }

    return dbService;
  });
