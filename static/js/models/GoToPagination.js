app.directive('goToPagination', function() {
  return {
    replace: true,
    restrict: 'E',
    scope: {
      currentPage: "=",
      maxPage: "=",
      goToPage: "&"
    },
    template: '<div id="go-to-pagination"><p ng-click="showInput = true"ng-hide="showInput">Page: [[ currentPage ]] / [[ maxPage ]]</p>' +
              '<div class="input-group" ng-show="showInput">' +
                '<input type="text" class="form-control" ng-keydown="keydown($event)" ng-model="currentPage">' +
                '<span class="input-group-btn">' +
                  '<button class="btn btn-secondary" ng-click="onClick()" type="button">Go!</button>' +
                '</span>'+
              '</div></div>',
    link: function(scope, elem, attr){
      scope.showInput = false;
      scope.onClick = function(){
        scope.showInput = false;
        if(scope.currentPage > scope.maxPage){
          scope.currentPage = scope.maxPage;
        }else if(scope.currentPage < 1){
          scope.currentPage = 1;
        }
        scope.goToPage({page: scope.currentPage});
      }

      scope.keydown = function($event){
        if($event.keyCode == 13){
          scope.onClick();
        }
      }
    }
  }
});
