

myapp.controller('pageCtr',function($scope,$http){

    $scope.us = null;
    $scope.pas = null;
    $scope.err = false;




    $scope.enviando = function(ev){
        ev.preventDefault();

        console.log('logueame');

            data = {
                'csrf':csrf,
                'usuarius':$scope.us,
                'passo':$scope.pas
            };

           data = $.param(data);

            params = {'url':'/sin/','method':'POST','data':data};
            $http(params).then(function(response){
                console.log(response.data);
                if(response.data.errors){
                    $scope.err = response.data.errors;
                }
                if(response.data.callback){
                    window.location.href = '/';
                }
            });

    }


});

