angular.module("mainApp").directive('dinaList', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


/*
$('.dinamicas_list').slick({
  infinite: false,
  slidesToShow: 3,
  slidesToScroll: 3
});

*/


        elm.slick({
          infinite: false,
          slidesToShow: 3,
          slidesToScroll: 3,
          lazyLoad: 'ondemand',
            responsive: [
                {
                  breakpoint: 768,
                  settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 1
                  }
                },
                {
                  breakpoint: 480,
                  settings: {
                    arrows: false,
                    centerMode: true,
                    centerPadding: '40px',
                    slidesToShow: 1
                  }
                }
              ]

        });



    }
  };

});


  


angular.module("mainApp").directive('jugandoTrivia', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      scope.preguntastotal = 1;
      scope.preguntastotal = jQuery('.noseve').length-2;
      jQuery('.pregunta_'+scope.preguntaindex).show();
    }
  };

});



angular.module("mainApp").directive('nextTrivia', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      
      elm.click(function(e){
        scope.preguntaindex++;
        indexe = scope.preguntaindex;
        jQuery('.noseve').hide();
        jQuery('.pregunta_'+indexe).show();
        scope.$apply();        
      });
      
    }
  };

});





angular.module("mainApp").directive('backTrivia', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      
      elm.click(function(e){
        scope.preguntaindex--;
        indexe = scope.preguntaindex;
        jQuery('.noseve').hide();
        jQuery('.pregunta_'+indexe).show();
        scope.$apply();        
      });
      
    }
  };

});





angular.module("mainApp").directive('respondePregunta', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      
      elm.click(function(e){


        var resultado = [
            {'name':'pregunta','value':attrs.pregunta},
            {'name':'respuesta_'+attrs.pregunta,'value':attrs.value}
          ];
          scope.resultados_juego[attrs.pregunta]=resultado;
        scope.$apply();        


      });
      
    }
  };

});



angular.module("mainApp").directive('finTrivia', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      
      elm.click(function(e){
        console.log('as');
        jQuery('.noseve,.botonera .btn').hide();
        jQuery('.preguntafinal,.cerrarbtn').show();
        
      });
      
    }
  };

});



angular.module("mainApp").directive('veDetalle', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

      elm.click(function(e){
        window.location.href='/promo/'+attrs.pk+'/';

      });

    }
  };

});
