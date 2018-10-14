angular.module("mainApp").directive('addDinCat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){


        	  newcat = {'cpk':0,'name':'categoría',
                 'slug':'','orden':1,
                 'subcats':[
                 {'scpk':0,'name':'subcat','slug':'','orden':1}
                 ]
                };



                scope.cats.push(newcat);

              scope.$apply();
        });        

    }
  };

}]);



angular.module("mainApp").directive('rmDinCat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){        	
        	inx = scope.$parent.cats.indexOf(scope.c);
        	if(inx>-1){
        		scope.$parent.cats.splice(inx,1);
        		scope.$apply();
        	}
        	return true;
        	  newcat = {'cpk':0,'name':'categoría',
                 'slug':'','orden':1,
                 'subcats':[
                 {'scpk':0,'name':'subcat','slug':'','orden':1}
                 ]
                };

                scope.$parent.cats.push(newcat);

             
        });        

    }
  };

}]);


angular.module("mainApp").directive('addSb', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){


          newsubcat = {'cpk':0,'name':'subcat','slug':'','orden':1,'parentcat':scope.c.cpk};

          params = {'url':'/promomanage/addscat/','method':'GET','params':newsubcat};
          $http(params).then(function(response){
            newsubcat.cpk = response.data.pk;
            scope.c.subcats.unshift(newsubcat);

          });
          scope.$apply();             
        });        
    }
  };

}]);



angular.module("mainApp").directive('addCat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){

       cat = {'cpk':0,'name':'Categoria',
         'slug':'','orden':1,
         'subcats':[],
         'parentcat':null
        };

        params = {'url':'/promomanage/addcat/','method':'GET','params':cat};
        $http(params).then(function(response){
          cat.cpk = response.data.pk;
          scope.cats.push(cat);

        });
        scope.$apply();             
      });        
    }
  };

}]);



angular.module("mainApp").directive('rmCat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
        params = {'url':'/promomanage/rmcat/','method':'GET','params':scope.c};
        $http(params).then(function(response){
          
          inx = scope.$parent.cats.indexOf(scope.c);
          scope.$parent.cats.splice(inx,1);

        });
        scope.$apply();             
      });        
    }
  };

}]);


angular.module("mainApp").directive('rmScat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
        params = {'url':'/promomanage/rmcat/','method':'GET','params':scope.sb};
        $http(params).then(function(response){
          
          inx = scope.$parent.c.subcats.indexOf(scope.sb);
          scope.$parent.c.subcats.splice(inx,1);

        });
        scope.$apply();             
      });        
    }
  };

}]);


angular.module("mainApp").directive('savePromocat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.blur(function(e){


        params = {'url':'/promomanage/addcat/','method':'GET','params':scope.c};
        $http(params).then(function(response){
          guardado = true;
        });
        scope.$apply();             
      });        
    }
  };

}]);



angular.module("mainApp").directive('savePromoScat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.blur(function(e){


        params = {'url':'/promomanage/addcat/','method':'GET','params':scope.sb};
        $http(params).then(function(response){
          guardado = true;
        });
        scope.$apply();             
      });        
    }
  };

}]);





angular.module("mainApp").directive('rm-din-sbcat', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
        	console.log(scope);
        	newsubcat = {'scpk':0,'name':'subcat','slug':'','orden':1};
            scope.c.subcats.push(newsubcat);
            scope.$apply();             
        });        
    }
  };

}]);




angular.module("mainApp").directive('launchDinamicaFoto', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            jQuery('#cropperboxdinamica').show();
            var $image = $('#imagex');                  
            $image.attr('src','/static/statics/imgs/defaults/grid.png');
            $image.cropper('destroy');
            scope.launchDinamicaDrop();
        });

    }
  };

});



angular.module("mainApp").directive('launchPreguntaFoto', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){


          var myDropzone = new Dropzone("div#dropimg", { url: "/"});
          

            return true;

            jQuery('#cropperboxdinamica').show();
            var $image = $('#imagex');                  
            $image.attr('src','/static/statics/imgs/defaults/grid.png');
            $image.cropper('destroy');
            scope.droppreguntaimg();
        });

    }
  };

});





angular.module("mainApp").directive('prevQuiz', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          actualquiz = parseInt(scope.quiz);
          if(actualquiz>0)
            scope.quiz -=1;

          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('nextQuiz', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          actualquiz = parseInt(scope.quiz);
          dinamicaqt = scope.dinamica.quiz_info.length;
          console.log(dinamicaqt);
          if(actualquiz < dinamicaqt-1)
            scope.quiz +=1;
          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('addQuiz', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          targetvi = scope.$parent.$parent.$parent.promocion_edit;

          modul = new MODULOS;
          newquiz = modul.getQuiz(targetvi.dinamica);
          newquiz.orden = targetvi.dins.length;

          data = newquiz;
          data.promopk = targetvi.pk;
          params = {'url':'/promomanage/savequiz/','method':'GET','params':data};
          $http(params).then(function(response){
            newquiz.pk=response.data.preg;
            targetvi.dins.push(newquiz);

          });

          
          scope.$apply();
        });

    }
  };

});




angular.module("mainApp").directive('saveQuiz', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          data = {};
          data.pk = scope.t.pk;
          data.pregunta = scope.t.pregunta;
          data.options = scope.t.options;

          data.promopk = scope.$parent.$parent.$parent.$parent.promocion_edit.pk;
          params = {'url':'/promomanage/savequiz/','method':'GET','params':data};
          $http(params).then(function(response){
            console.log(response.data);
            scope.t.pk=response.data.preg
          });


          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('rmQuiz', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          console.log();
          dins = scope.$parent.$parent.$parent.$parent.promocion_edit.dins;
          inx = dins.indexOf(scope.t);
          
          data = {'pk':scope.t.pk};
          data = $.param(data);
          params = {'url':'/promomanage/rmquiz/','method':'POST','data':data};
          $http(params).then(function(response){
            dins.splice(inx,1);  
          });


          scope.$apply();
        });

    }
  };

});




angular.module("mainApp").directive('checkCor', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          checado = $(elm).is(':checked');
          console.log(checado);
          scope.a.cor=true;
          scope.$apply();
        });

    }
  };

});






function convertMS(ms) {
  var d, h, m, s;
  s = Math.floor(ms / 1000);
  m = Math.floor(s / 60);
  s = s % 60;
  h = Math.floor(m / 60);
  m = m % 60;
  d = Math.floor(h / 24);
  h = h % 24;
  return { d: d, h: h, m: m, s: s };
};


angular.module("mainApp").directive('watchVigencia', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {



      scope.$watch('dinamica.finaliza',function(x,y){

        
        inicial = new Date(scope.dinamica.inicia);
        final = new Date(scope.dinamica.finaliza);

        if(isNaN(final)){

          scope.dinamica.tiempo = '00:00:00:00';        

        }
        else{
          var timeDiff = Math.abs(final.getTime() - inicial.getTime());
          convtime = convertMS(timeDiff);
          scope.dinamica.tiempo = convtime.d + ':'+convtime.h+':'+convtime.m+':'+convtime.s;                  
        }


      });



    }
  };

});





angular.module("mainApp").directive('saveDinamicax', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){  
            scope.dinamica.bases = safeText(scope.dinamica.bases);
            scope.dinamica.titulo = safeText(scope.dinamica.titulo);        
            data = scope.dinamica;
            params = {'url':'/dinamicas/savedin/','method':'GET','params':data};
            $http(params).then(function(response){
              
              scope.dinamica.dpk = response.data.dpk;

            });




          scope.$apply();
        });

    }
  };

});





angular.module("mainApp").directive('newDinamica', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){  

          scope.dinamica.bases = safeText(scope.dinamica.bases);
            scope.dinamica.titulo = safeText(scope.dinamica.titulo);        
            data = scope.dinamica;
            params = {'url':'/dinamicas/savedin/','method':'GET','params':data};
            $http(params).then(function(response){
              
              scope.dinamica.dpk = response.data.dpk;
              window.location.href='/dinamicas/dinamica/'+response.data.dpk+'/';

            });

          scope.$apply();
        

        });

    }
  };

});



angular.module("mainApp").directive('saveCrodinamiva', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){


            jQuery('#cropperboxdinamica').hide();
            $('#imagex').cropper("destroy");
            $('#velo').show();


            datas = {
                    'dpk':scope.dinamica.dpk,
                    'cropimg':scope.dinamica.media.img,
                    'slug':'dinamica'
                   };
      
 

            data = $.param(datas);

            params = {'url':'/motor/imagen/','method':'POST','data':data};
            
            $http(params).then(function(response){
                var nochaestring = Date.now();
                scope.dinamica.media.img = '/'+response.data.img+'?p='+nochaestring;
                $('#velo').hide();              
            });
            
            scope.$apply();

        });

    }
  };

}]);





angular.module("mainApp").directive('lauchFotoGeneral', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
          var csrf = jQuery("[name=csrfmiddlewaretoken]").val();
          var myDropzone = new Dropzone("div#dropgeneral", { url: "/motor/dropimage/",
            'paramName':'filex',
            'method':'POST',
            'params':{'pk':scope.promocion_edit.pk,
                      'typo':'p',
                      'slug':'dinamica_params',
                      'csrfmiddlewaretoken':csrf},
            'success':function(e,response){
              fecha = Date.now();
              scope.promocion_edit.media.firstimg=response.cropimg+'?p='+fecha;
              fercha = new Date();
              droper = $('#dropgeneral');
              droper[0].dropzone.removeAllFiles();
              scope.$apply();
              myDropzone.destroy();
              jQuery('#dropgeneral').html('');
            },
            'complete':function(e,response){
              myDropzone.destroy();
            }
          });

          jQuery('#dropgeneral').click();
        });

    }
  };

});



angular.module("mainApp").directive('lauchFotoPortada', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){
          var csrf = jQuery("[name=csrfmiddlewaretoken]").val();
          var myDropzone = new Dropzone("div#dropgeneral", { url: "/motor/addimagefinal/",
            'paramName':'filex',
            'method':'POST',
            'params':{'pk':scope.promocion_edit.pk,
                      'typo':attrs.tipoimg,
                      'slug':'dinamica_params',
                      'csrfmiddlewaretoken':csrf},
            'success':function(e,response){
              fecha = Date.now();
              fercha = new Date();
              droper = $('#dropgeneral');
              droper[0].dropzone.removeAllFiles();

              scope.promocion_edit[attrs.tipoimg]='/'+response.imagen+'?p='+fecha;                
              
              scope.$apply();
              myDropzone.destroy();
              jQuery('#dropgeneral').html('');
            },
            'complete':function(e,response){
              myDropzone.destroy();
            }
          });

          jQuery('#dropgeneral').click();
        });

    }
  };

});



angular.module("mainApp").directive('lauchFotoFinal', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){
          var csrf = jQuery("[name=csrfmiddlewaretoken]").val();
          var myDropzone = new Dropzone("div#dropgeneral", { url: "/motor/addimagegaleria/",
            'paramName':'filex',
            'method':'POST',
            'params':{'pk':scope.promocion_edit.pk,
                      'typo':attrs.tipoimg,
                      'slug':'dinamica_params',
                      'csrfmiddlewaretoken':csrf},
            'success':function(e,response){
              fecha = Date.now();
              fercha = new Date();
              droper = $('#dropgeneral');
              droper[0].dropzone.removeAllFiles();

              scope.promocion_edit.galeria.push({'ipk':response.ipk,'imagen':response.imagen+'?p='+fecha});

              scope.$apply();
              myDropzone.destroy();
              jQuery('#dropgeneral').html('');
            },
            'complete':function(e,response){
              myDropzone.destroy();
            }
          });

          jQuery('#dropgeneral').click();
        });

    }
  };

});



angular.module("mainApp").directive('lauchFotoQuiz', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
          var promo = scope.$parent.promocion_edit;
          var csrf = jQuery("[name=csrfmiddlewaretoken]").val();

          var myDropzone = new Dropzone("div#dropgeneral", { url: "/motor/dropimagelg/",
            'paramName':'filex',
            'method':'POST',
            'params':{'pk':promo.pk,'typo':'p','slug':'dinamica_params','csrfmiddlewaretoken':csrf},
            'success':function(e,response){
              fecha = Date.now();
              promo.media.imglg=response.cropimg+'?p='+fecha;
              fercha = new Date();
              droper = $('#dropgeneral');
              droper[0].dropzone.removeAllFiles();
              scope.$apply();
              myDropzone.destroy();
              jQuery('#dropgeneral').html('');
            }
          });

          jQuery('#dropgeneral').click();
        });

    }
  };

});



/* ------------------------------   PROMOCIONES   ---------------- */


angular.module("mainApp").directive('addPromo', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var csrf = jQuery("[name=csrfmiddlewaretoken]").val();
            promo = {
             'pk':0,
             'titulo':'TITULO',
             'linea_uno':'linea de texto',
             'linea_dos':'linea de texto',
             'vigencia':'',
             'shares':120,
             'likes':340,
             'media':{
                'firstimg':'/static/statics/imgs/defaults/grid.png',
                'galery':[],
                'videos':[]
             },
            'categorias':[],
            'mercado':[],
            'ganadores':[],
            'status':'',
            'color':'c227b9',
            'bases':'',
            'terms':'',
            'fecha_evento':'',
            'ciudad':'',
            'lugar':'',
            'premio':'',
            'modo':'neww',
            'segmentos':[],
            'categorias':[],
            'dinamica':'',
            'dins':[],
            'destacado':'normal',
            'status':'working',
            'orden':1             
            };

            orden = scope.promociones.length;
            promo.orden = orden;
            datas = promo;
            datas['csrf'] = csrf;
            scope.promocion_edit = promo;
            data = $.param(datas);
            params = {'url':'/promomanage/addpromo/','method':'POST','data':data};
            $http(params).then(function(response){
                var reloader = Date.now();
                scope.promocion_edit.pk = response.data.pk;
                scope.promocion_edit.modo='edt';
                scope.promociones.push(scope.promocion_edit);
                //scope.dinamica.media.img = '/'+response.data.img+'?p='+nochaestring;
                $('#velo').hide();              
            });
            scope.reloadform = new Date().getTime();
            scope.$apply();
        });



    }
  };

});




angular.module("mainApp").directive('savePromo', function($http) {

 return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var csrf = jQuery("[name=csrfmiddlewaretoken]").val();
            datas = scope.promocion_edit;
            scope.mensaje = 'guardando ...';


            datas['titulo'] = safeText(scope.promocion_edit.titulo);
            datas['bases'] = safeText(scope.promocion_edit.bases);
            datas['terms'] = safeText(scope.promocion_edit.terms);
            datas['texto_alterno'] = safeText(scope.promocion_edit.texto_alterno);
            datas['premioterms'] = safeText(scope.promocion_edit.premioterms);

            datas['csrf'] = csrf;
            data = $.param(datas);
            params = {'url':'/promomanage/addpromo/','method':'POST','data':data};
            $http(params).then(function(response){
                var reloader = Date.now();
                scope.promocion_edit.pk = response.data.pk;
                $('#velo').hide();
                scope.mensaje = 'Guardado con éxito!!';
            });
            scope.reloadform = new Date().getTime();
            scope.$apply();
        });



    }
  };

});




angular.module("mainApp").directive('edtPromo', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            scope.mensaje = '';
            params = {'url':'/allp/','method':'GET','params':{'pk':scope.d.pk}};
            $http(params).then(function(response){
                console.log(response.data.promocion,'scandal');
                scope.$parent.promocion_edit = response.data.promocion;
            });

        });



    }
  };

});




angular.module("mainApp").directive('datePick', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {



            var today = new Date();
            var tomorrow = new Date();
            var tm = tomorrow.setDate(today.getDate()+5);
            elm.datepicker({'dateFormat':'d/m/yy'});



    }
  };

});


angular.module("mainApp").directive('dateCusPick', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

            var today = new Date();
            var tomorrow = new Date();
            var tm = tomorrow.setDate(today.getDate()+5);
            elm.datepicker({'dateFormat':'d/m/yy'});



    }
  };

});




angular.module("mainApp").directive('cambioDinamica', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.change(function(e){
            valor = elm.val();
            scope.$parent.promocion_edit.dinamica = valor;
            scope.$parent.promocion_edit.dins = [];
            modul = new MODULOS;
            newquiz = modul.getQuiz(valor);
            scope.$parent.promocion_edit.dins.push(newquiz);

            scope.$apply();
        });



    }
  };

});


angular.module("mainApp").directive('cambioDest', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.change(function(e){
            valor = elm.val();
            scope.$parent.promocion_edit.destacado = valor;
            scope.$apply();
        });



    }
  };

});





angular.module("mainApp").directive('segmentaPromo', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            checado = $(elm).is(':checked');
            valor = $(elm).val();
            promo = scope.$parent.$parent.promocion_edit;
            if(checado){
              
              promo.segmentos.push(valor);
              //console.log(scope.$parent.$parent.promocion_edit);
            }
            else{
              inx = promo.segmentos.indexOf(valor);
              promo.segmentos.splice(inx,1);
            }
            scope.$apply();
        });



    }
  };

});





angular.module("mainApp").directive('catzPromo', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            checado = $(elm).is(':checked');
            valor = $(elm).val();
            promo = scope.$parent.$parent.promocion_edit;
            if(checado){
              
              promo.categorias.push(valor);
              
            }
            else{
              inx = promo.categorias.indexOf(valor);
              promo.categorias.splice(inx,1);
            }
            scope.$apply();
        });



    }
  };

});



angular.module("mainApp").directive('anserCh', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {



        elm.click(function(e){

            preg = scope.$parent.t;
            res = scope.a;


            angular.forEach(preg.options,function(v,k){
              v.cor = false;
            });

            res.cor = true;

            scope.$apply();
        });



    }
  };

});



angular.module("mainApp").directive('rmPromo', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){


          if(confirm('DEsea eliminar esta promoción')){

            data = {'pk':scope.d.pk};

            data = $.param(data);

            params = {'url':'/promomanage/rmpromo/','method':'POST','data':data};
            
            $http(params).then(function(response){
              promos = scope.$parent.promociones;
              promo = scope.d;
              inx = promos.indexOf(promo);
              promos.splice(inx,1);
            });
          }
            scope.$apply();
        });



    }
  };

});




angular.module("mainApp").directive('launchImagenP', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.change(function(e){
            

            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            reader.onload = function (e) {
              resultado = e.target.result;
              scope.t.img = resultado;


            data = {'pk':scope.t.pk,'img':scope.t.img};

            data = $.param(data);

            params = {'url':'/promomanage/addfoto/','method':'POST','data':data};
            
            $http(params).then(function(response){
              saved = true;
            });



              scope.$apply();
            };
            reader.readAsDataURL(file);
        });

    }
  };

}]);


/*
  JUEGO DE PALABRAS

*/



angular.module("mainApp").directive('launchImagenSs', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.change(function(e){
            

            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            reader.onload = function (e) {
              resultado = e.target.result;
              console.log('done');
              scope.$parent.t.img[scope.ims] = resultado;

              
            data = {'pk':scope.t.pk,'img':scope.t.img[scope.ims],'ims':scope.ims};

            data = $.param(data);

            params = {'url':'/promomanage/addfotopalabra/','method':'POST','data':data};
            
            $http(params).then(function(response){
              saved = true;
            });
            


              scope.$apply();
            };
            reader.readAsDataURL(file);
        });

    }
  };

}]);


angular.module("mainApp").directive('savePalabras', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          

          data = {};
          data.pk = scope.t.pk;
          data.description = scope.t.description;
          data.palabra = scope.t.palabra;
          data.promopk = scope.$parent.$parent.$parent.$parent.promocion_edit.pk;
          params = {'url':'/promomanage/savepalabra/','method':'GET','params':data};
          $http(params).then(function(response){
            
            scope.t.pk=response.data.pk;
          });


          scope.$apply();
        });

    }
  };

});


angular.module("mainApp").directive('blursavePalabras', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.blur(function(e){          

          data = {};
          data.pk = scope.t.pk;
          data.description = scope.t.description;
          data.palabra = scope.t.palabra;
          data.promopk = scope.$parent.$parent.$parent.$parent.promocion_edit.pk;
          params = {'url':'/promomanage/savepalabra/','method':'GET','params':data};
          $http(params).then(function(response){
            
            scope.t.pk=response.data.pk;
          });


          scope.$apply();
        });

    }
  };

});


angular.module("mainApp").directive('addPalabra', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          targetvi = scope.$parent.$parent.$parent.promocion_edit;

          modul = new MODULOS;
          newquiz = modul.getQuiz(targetvi.dinamica);
          newquiz.orden = targetvi.dins.length;

          data = newquiz;
          data.promopk = targetvi.pk;
          params = {'url':'/promomanage/savepalabra/','method':'GET','params':data};
          $http(params).then(function(response){
            newquiz.pk=response.data.pk;
            targetvi.dins.push(newquiz);

          });

          
          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('rmPalabra', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          
          dins = scope.$parent.$parent.$parent.$parent.promocion_edit.dins;
          inx = dins.indexOf(scope.t);
          data = {'pk':scope.t.pk};
          data = $.param(data);
          params = {'url':'/promomanage/rmpalabra/','method':'POST','data':data};
          $http(params).then(function(response){
              eliminado = true;
          });

          dins.splice(inx,1);
          scope.$apply();
        });

    }
  };

});




/* MARCADOR DE FUTBOL */

angular.module("mainApp").directive('addMarcador', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          targetvi = scope.$parent.$parent.$parent.promocion_edit;

          modul = new MODULOS;
          newquiz = modul.getQuiz(targetvi.dinamica);
          newquiz.orden = targetvi.dins.length;

          data = newquiz;
          data.promopk = targetvi.pk;
          params = {'url':'/promomanage/savemarcador/','method':'GET','params':data};
          $http(params).then(function(response){
            newquiz.pk=response.data.pk;
            targetvi.dins.push(newquiz);

          });

          
          scope.$apply();
        });

    }
  };

});


angular.module("mainApp").directive('saveMarcador', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          

          data = {};
          data.pk = scope.t.pk;
          data.description =  safeText(scope.t.description);
          data.marcador_uno = scope.t.imgs[0].marcador;
          data.marcador_dos = scope.t.imgs[1].marcador;
          data.respuesta = scope.t.respuesta;
          data.promopk = scope.$parent.$parent.$parent.$parent.promocion_edit.pk;
          params = {'url':'/promomanage/savemarcador/','method':'GET','params':data};
          $http(params).then(function(response){
            
            scope.t.pk=response.data.pk;
          });


          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('launchImagenMarcador', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.change(function(e){
            

            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            reader.onload = function (e) {
              resultado = e.target.result;
              scope.$parent.t.imgs[scope.ims].img = resultado;

              
            data = {'pk':scope.t.pk,'img':scope.t.imgs[scope.ims].img,'ims':scope.ims};


            data = $.param(data);

            params = {'url':'/promomanage/addfotomarcador/','method':'POST','data':data};
            
            $http(params).then(function(response){
              saved = true;
            });
            


              scope.$apply();
            };
            reader.readAsDataURL(file);
        });

    }
  };

}]);






angular.module("mainApp").directive('clickGanador', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){

          checado = $(elm).is(':checked');
          

          if(checado && confirm('Desea seleccionar esta participación como ganadora?')){

              data = {'promopk':attrs.promo,'usuario':attrs.user};
              data = $.param(data);
              params = {'url':'/promomanage/setwinner/','method':'POST','data':data};
              
              $http(params).then(function(response){
                saved = true;
                console.log(response);
                $(elm).attr('disabled','disabled');
              });

          }

            


              scope.$apply();
        });        

    }
  };

}]);


var sels = 0;        

angular.module("mainApp").directive('activadorDe', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        scope.activo = false;

        elm.click(function(e){
            selecions = [];
            
            if(scope.activo){
              scope.activo = false;
              sels--;
            }
            else{
              scope.activo = true;
              sels++;
            }     


            console.log(sels);

            scope.$parent.fkr = scope.kr;
            scope.$parent.fkc = scope.kc;
            console.log(scope.$parent.fkr,scope.$parent.fkc);
            scope.$apply();
        });        

    }
  };

}]);



angular.module("mainApp").directive('palabrasLoad', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        console.log(scope);

    }
  };

}]);



angular.module("mainApp").directive('addSopa', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          targetvi = scope.$parent.$parent.$parent.promocion_edit;

          modul = new MODULOS;
          newquiz = modul.getQuiz(targetvi.dinamica);
          newquiz.orden = targetvi.dins.length;

          data = newquiz;
          data.promopk = targetvi.pk;
          params = {'url':'/promomanage/savepalabra/','method':'GET','params':data};
          $http(params).then(function(response){
            newquiz.pk=response.data.pk;
            targetvi.dins.push(newquiz);

          });

          
          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('generaTableroSopa', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){ 
          cual = scope.$parent.$parent.$parent.$parent.promocion_edit;
          palabras = scope.$parent.$parent.$parent.$parent.promocion_edit.dins;
          submit_palabras = [];
          angular.forEach(palabras,function(x,y){
            submit_palabras.push(x.palabra);
          });

          data = {'palabras':submit_palabras,'promopk':cual.pk};
          params = {'url':'/createsopa/','method':'GET','params':data};
          $http(params).then(function(response){
           cual.matrix = response.data.matrix;
          });
          
          scope.$apply();
        });

    }
  };

});



angular.module("mainApp").directive('addVentaja', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){ 


          var v = scope.ventaja;
          var v_init = scope.ventaja_inicio;
          var v_end = scope.ventaja_fin;
          var vterminos = safeText(scope.ventaja_terminos);

          if(v && v_init && v_end){

            visibles = scope.ventajas.filter(function (elm) {
              return (elm.inicio === v_init);
            });
            
            if(visibles.length>0){
              alert('Ya hay una ventaja con esa fecha de inicio');
            }

            else{
              var ven = {'ventaja':v,'inicio':v_init,'fin':v_end,'vterminos':vterminos};

          params = {'url':'/promomanage/addventaja/','method':'GET','params':ven};
          $http(params).then(function(response){
            ven.pk = response.data.pk;
            scope.ventajas.unshift(ven);
            forma = document.getElementById('ventajas-form').reset();

          });


             
            }
          }
          


          scope.$apply();
        });

    }
  };

});


angular.module("mainApp").directive('rmVentaja', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){ 

          ven = {'pk':scope.v.pk};

          if(confirm('Desea eliminar esta ventaja')){
            inx = scope.$parent.ventajas.indexOf(scope.v);
            scope.$parent.ventajas.splice(inx,1);
            params = {'url':'/promomanage/rmventaja/','method':'GET','params':ven};
            $http(params).then(function(response){
              ok = true;

            });

            
            scope.$apply();


          }

        });

    }
  };

});


angular.module("mainApp").directive('rmGaleria', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){

            console.log(scope);
            data = {'gpk':scope.g.ipk};

            params = {'url':'/motor/rmgaleria/','method':'GET','params':data};
            
            $http(params).then(function(response){
                inx = scope.$parent.$parent.$parent.promocion_edit.galeria.indexOf(scope.g);
                scope.$parent.$parent.$parent.promocion_edit.galeria.splice(inx,1);
            });
            
            scope.$apply();

        });

    }
  };

}]);


angular.module("mainApp").directive('chPaso', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){    
          scope.pasos = attrs.paso; 
          scope.$apply();
        });

    }
  };

});



/*  [SWIPER SERVICES]   */

angular.module("mainApp").directive('addSwiper', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          targetvi = scope.$parent.$parent.$parent.promocion_edit;
          modul = new MODULOS;
          newquiz = modul.getQuiz(targetvi.dinamica);
          newquiz.orden = targetvi.dins.length;
          newquiz.promopk = targetvi.pk;
          data = newquiz;
          params = {'url':'/promomanage/saveswiper/','method':'GET','params':data};          
          $http(params).then(function(response){
            newquiz.pk = response.data.pk;
              targetvi.dins.push(newquiz);          
          });

        });

    }
  };

});



angular.module("mainApp").directive('saveSwiper', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          data = scope.t;
          params = {'url':'/promomanage/saveswiper/','method':'GET','params':data};          
          $http(params).then(function(response){
            scope.t.pk = response.data.pk;
          });

        });

    }
  };

});



angular.module("mainApp").directive('rmSwiper', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){    

          if(confirm('Esta seguro que desea eliminar la pregunta y sus imagenes?')){
            data = scope.t;
            inx = scope.$parent.$parent.$parent.$parent.promocion_edit.dins.indexOf(scope.t);
            scope.$parent.$parent.$parent.$parent.promocion_edit.dins.splice(inx,1);

            params = {'url':'/promomanage/rmswiper/','method':'GET','params':data};          
            $http(params).then(function(response){
              dones = true; 
            });            
          }

        });

    }
  };

});




angular.module("mainApp").directive('upSwipImg', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.change(function(e){
          scope.t.cargando = 'Cargando ...';

          var csrf = jQuery("[name=csrfmiddlewaretoken]").val();

            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            var ars = {};
            reader.onload = function (e) {
              resultado = e.target.result;              
              data = {'pk':scope.t.pk,'csrf':csrf,'imagen':resultado};
              data = $.param(data);
              params = {'url':'/promomanage/saveimgswiper/','method':'POST','data':data};          
              $http(params).then(function(response){
                scope.t.cargando = '';
                ars.img = response.data.img;
                ars.imgpk = response.data.imgpk; 
                scope.t.imgs.unshift(ars);
              });
            
              
            };
            reader.readAsDataURL(file);
            
        
        });



    }
  };

});



angular.module("mainApp").directive('rmSwimg', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          
          if(confirm('Desea eliminar esta imagen?')){
            data = {'imgpk':scope.i.imgpk};
            params = {'url':'/promomanage/rmimgswiper/','method':'GET','params':data};          
            $http(params).then(function(response){
              inx = scope.$parent.t.imgs.indexOf(scope.i);
              scope.$parent.t.imgs.splice(inx,1);
            });


          }

        
        });



    }
  };

});


angular.module("mainApp").directive('checkSwip', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          

              data = {'imgpk':scope.i.imgpk,'sideimg':attrs.data};
              scope.i.sideimg = attrs.data;
              scope.$apply();
              params = {'url':'/promomanage/saveimgswiper/','method':'GET','params':data};          
              $http(params).then(function(response){
                  dones = true;

              });


        });



    }
  };

});





angular.module("mainApp").directive('saveDinamicaTerm', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){          


          terms = safeText(scope.d.terms.terms);
          descp = safeText(scope.d.terms.descp);

          data = {
            'dpk':scope.d.dpk,
            'name':scope.d.name,
            'slug':scope.d.slug,
            'terms':terms,
            'descp':descp
          };


          params = {'url':'/promomanage/savedinter/','method':'GET','params':data};
          $http(params).then(function(response){
           doneit = '';
          });



        });



    }
  };

});



