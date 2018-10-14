
angular.module("mainApp").directive('participaDin', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            scope.$apply();
        });



    }
  };

});
