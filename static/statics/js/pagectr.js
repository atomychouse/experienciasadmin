


function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}




myapp.controller('pageCtr',function($scope,$http){


    

    $scope.cats = cats;
    $scope.reloadform = 0; 
    $scope.promocion_edit = {};
    $scope.tablero = null;
    $scope.pasos = 0;
    $scope.mensaje = '';
    $scope.reds = reds; 
    $scope.proximamentes = proximamentes; 
    $scope.activas = activas;
    $scope.feriados = feriados;

    $scope.segmentos = [
        {'segpk':1,
         'segmento':'Claro video',
         'slug':'clarovideo'
        },
        {'segpk':2,
         'segmento':'Claro música',
         'slug':'claromusica'
        },
        {'segpk':3,
         'segmento':'Claro juegos',
         'slug':'clarojuegos'
        },
        {'segpk':4,
         'segmento':'Claro drive',
         'slug':'clarodrive'
        },
        {'segpk':5,
         'segmento':'Club Claro apps',
         'slug':'clubclaroapp'
        },
        {'segpk':6,
         'segmento':'Claro entretenimiento',
         'slug':'claroentretenimiento'
        },
        {'segpk':7,
         'segmento':'Contestone',
         'slug':'contestone'
        },
        {'segpk':4,
         'segmento':'App Telcel',
         'slug':'apptelcel'
        }
    ];



    $scope.dinamicas = [
        {'dpk':1,
         'name':'Trivia',
         'slug':'trivia',
         'terms':dinter['trivia'],
         'bones':[]
        },
        {'dpk':2,
         'name':'Sopa de letras',
         'slug':'sopa',
         'terms':dinter['sopa'],
         'bones':[]
        },
        {'dpk':4,
         'name':'Marcador Futbol',
         'slug':'marcador_futbol',
         'terms':dinter['marcador_futbol'],
         'bones':[]
        }
        ,
        {'dpk':5,
         'name':'Rompecabezas',
         'slug':'puzzle',
         'terms':dinter['puzzle'],
         'bones':[]
        },
        {'dpk':6,
         'name':'Swiper',
         'slug':'swiper',
         'terms':dinter['trivia'],
         'bones':[]
        }

    ];


$scope.sopa_range = [];
for(r=0;r<10;r++){
  rows = [];
  for(c=0;c<10;c++){
    rows.push(c);
  }
  $scope.sopa_range.push(rows);
};




$scope.checktrivia = function(cor){


  if(cor=='True'){
    console.log('ctm',this);
    return true;
  }
  else{
    return false;
  }

}



$scope.promociones = [];
$scope.ventajas = [];
$scope.allpromos = [];
$scope.terminostxt = '';
$scope.texto_recogerprovincia = '';
$scope.texto_recogercdmx = '';
$scope.texto_recogerterceros = '';

$http.get('/allp/')
    .then(function(response) {
      $scope.ventajas = response.data.ventajas;
      $scope.promociones = response.data.dinamicas;
      $scope.allpromociones = response.data.dinamicas;
      $scope.terminostxt = response.data.terminos;
      $scope.texto_recogerprovincia = response.data.texto_recogerprovincia;
      $scope.texto_recogercdmx = response.data.texto_recogercdmx;
      $scope.texto_recogerterceros = response.data.texto_recogerterceros;


          $scope.promociones = $scope.promociones.filter(function (elm) {          
            return ($scope.reds.indexOf(elm.pk.toString())< 0);
          });



    });
   

    modrow = null;
    loadrow = null;




    $scope.savemodulo = function(rowg){

            data = {'rowpk':rowg.rowpk,'mtitle':rowg.title};
            data = $.param(data);
            params = {'url':'/motor/addmodulo/','method':'POST','data':data};
            $http(params).then(function(response){
                console.log('saved');
            });
    };


    $scope.savecat = function(c){

            data = {
            'catpk':c.catpk,
            'catname':c.catname,
            'orden':c.orden
            };
            data = $.param(data);
            params = {'url':'/motor/addcategoria/','method':'POST','data':data};
            $http(params).then(function(response){
                console.log('cat saved');
            });  
    }



    $scope.checkmycat = function(sb){

        if($scope.bancocats.length>0){
            itmcats = $scope.bancocats[0];
            inx = itmcats.mycats.indexOf(sb.catpk.toString());
            if(inx>=0)
                return true;
            else
                return false;
        }
        

    }



    $scope.setfullimage = function(ev,itm){
        ev.preventDefault();
        
        $scope.fullimage = itm.media.prev;
        $scope.titulo = itm.titulo;
        $scope.descp = itm.descp;
        $scope.dwfile = itm.media.full;
        $scope.dwfiles = itm.files;
    }


    $scope.viewmodbox = function(){
        $('#addmodbox').show();
        $scope.boxmods=true;
    }



    $scope.chowme = function(itm){

        if(itm.publicado==1){
            return false; 
        }
        else{
        if($scope.editando===true)
            return false;
        else
            return true;
        }
    }


    $scope.megamenus = function(page){
        if(page.secs.length>0)
        return true;
        else
        return false;
    }





    $scope.launchDrop = function(){


        var droper = $('#dropme');

        droper[0].dropzone.destroy();                    
        $('#dropme').dropzone({
            'paramName':'filex',
            'params':{'pk':1,'pok':101},
            'success':function(e,response){
                droper = $('#dropme');
                droper[0].dropzone.removeAllFiles();
                var $image = $('#image');  
                $scope.currmedia = response;
                var fechaEnMiliseg = Date.now();
                $image.attr('src',response.cropimg+'?p='+fechaEnMiliseg);                
                $image.cropper('destroy');
                $image.cropper({
                  'aspectRatio':$scope.itmedited[0].aspectRatio,
                  'viewMode':3,
                  'responsive':false,
                  'zoomable':true,
                  'restore':true,
                  'checkCrossOrigin':true,
                  'ready': function () {
                    croppable = true;                    
                  },
                  'crop':function(ax){
                    croppedCanvas = $image.cropper('getCroppedCanvas');
                    $scope.itmedited[0].media.img = croppedCanvas.toDataURL();
                    $scope.$apply();

                  },
                  'croped':function(ax){
                    console.log(ax);
                  }


              });
               
              
               
              jQuery('#cropperbox').show();


            }
        }); 
    }




    $scope.directImg = function(){

        $scope.urlupim = '/promo/';
        var droper = $('#dropme');

        /*
        try{
          droper[0].dropzone.destroy();
        }
        catch(err){
          no = '';
        }
        */
        $('#dropme').dropzone({
            'url':$scope.urlupim,
            'paramName':'filex',
            'params':{'pk':1,'pok':101},
            'success':function(e,response){
                console.log('asas');
                droper = $('#dropme');
                //droper[0].dropzone.removeAllFiles();
                //var $image = $('#image');  
                //$scope.currmedia = response;
                var fechaEnMiliseg = Date.now();
                $image.attr('src',response.cropimg+'?p='+fechaEnMiliseg);              
                //jQuery('#cropperbox').show();


            }
        }); 
    }


    $scope.launchDinamicaDrop = function(){


        var droper = $('#dropmed');

        droper[0].dropzone.destroy();                    
        $('#dropmed').dropzone({
            'paramName':'filex',
            'params':{'pk':1,'pok':101},
            'success':function(e,response){
                droper = $('#dropmed');
                droper[0].dropzone.removeAllFiles();
                var $image = $('#imagex');  
                $scope.currmedia = response;
                var fechaEnMiliseg = Date.now();
                $image.attr('src',response.cropimg+'?p='+fechaEnMiliseg);                
                $image.cropper('destroy');
                $image.cropper({
                  'aspectRatio':2.133333333,
                  'viewMode':3,
                  'responsive':false,
                  'zoomable':true,
                  'restore':true,
                  'checkCrossOrigin':true,
                  'ready': function () {
                    croppable = true;                    
                  },
                  'crop':function(ax){                    
                    croppedCanvas = $image.cropper('getCroppedCanvas');
                    $scope.dinamica.media.img = croppedCanvas.toDataURL();
                    $scope.$apply();
                  },
                  'croped':function(ax){
                    console.log(ax);
                  }


              });
               
              
               
              jQuery('#cropperboxdinamica').show();


            }
        }); 
    }




    $scope.droppreguntaimg = function(){



        console.log($scope.quiz);
        return true;

        var droper = $('#dropmed');

        droper[0].dropzone.destroy(); 

        $('#dropmed').dropzone({
            'paramName':'filex',
            'params':{'pk':1,'pok':101},
            'success':function(e,response){
                droper = $('#dropmed');
                droper[0].dropzone.removeAllFiles();
                var $image = $('#imagex');  
                $scope.currmedia = response;
                var fechaEnMiliseg = Date.now();
                $image.attr('src',response.cropimg+'?p='+fechaEnMiliseg);                
                $image.cropper('destroy');
                $image.cropper({
                  'aspectRatio':2.133333333,
                  'viewMode':3,
                  'responsive':false,
                  'zoomable':true,
                  'restore':true,
                  'checkCrossOrigin':true,
                  'ready': function () {
                    croppable = true;                    
                  },
                  'crop':function(ax){                    
                    croppedCanvas = $image.cropper('getCroppedCanvas');
                    $scope.dinamica.media.img = croppedCanvas.toDataURL();
                    $scope.$apply();
                  },
                  'croped':function(ax){
                    console.log(ax);
                  }


              });
               
              
               
              jQuery('#cropperboxdinamica').show();


            }
        }); 


    }



    $scope.checksegmento = function(seg){
      if($scope.promocion_edit.segmentos)
      {
        segpk = String(seg.slug);
        inx = $scope.promocion_edit.segmentos.indexOf(seg.slug);
        if(inx>-1)
          return true;
        else
          return false;

      }

    }


    $scope.checkcategoria = function(cat){
      if($scope.promocion_edit.categorias)
      {
        catpk = String(cat.slug);
        inx = $scope.promocion_edit.categorias.indexOf(cat.slug);
        if(inx>-1)
          return true;
        else
          return false;

      }

    }





    $scope.checpregunta = function(este,valor){

      console.log(este);

      if(valor=='True'){
        return true;
      }
      else{
        return false;
      }


    }


});

