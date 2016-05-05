app.controller("SearchBarController", function($scope){
  $scope.checkButton = function($event){
    if($event.keyCode == 13){
      window.location.pathname = "/search/" + $scope.text;
    }
  }
});
/***

This is a big no-no, but a quick hacky fix.
I think bootstrap.js is manipulating the navbar in some way, causing
the ng-controller directive to be ignored. In order to work around
that issue, pure jquery is being used instead

***/

$().ready(function(){
  function execSearch(e){
    e.preventDefault();
    window.location.pathname = "/search/" + $('#navbar-search-bar').val();
  }

  $('#navbar-search-btn').click(execSearch);
  $('#navbar-search-bar').keydown(function(e){
    if(e.which == 13){
      execSearch(e);
    }
  })
});
