angular.module("mainApp").directive('editPage', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){

            scope.editando = true;
            document.cookie="modo=edition";
            scope.$apply();

        });



    }
  };

});






angular.module("mainApp").directive('viewPage', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){

            scope.editando = false;
            document.cookie="modo=viewer";


            angular.forEach(scope.modules,function(v,k){

                v.confiuring = false;
            });


            scope.$apply();

        });



    }
  };

});



angular.module("mainApp").directive('justDraggable', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      elm.draggable({
        stop: function(e) {
            justdragged = true;
        }
      });

    }
  };

});



angular.module("mainApp").directive('slideMas', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

      elm.flickity({
        // options
        cellAlign: 'left',
        contain: true
      });

    }
  };

});




angular.module("mainApp").directive('popOvers', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

      elm.tooltip({
            content: "&nbps,!!!",
            title:scope.m.tooltip
        });



    }
  };

});




angular.module("mainApp").directive('slideSpace', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      elm.slider({
        'min':10,
        'max':200,
        'value':scope.$parent.r.cfg.alto,
        'slide':function(event,ui){
            scope.$parent.r.cfg.alto=ui.value;
            scope.$apply();
        }

      });

    }
  };

});


angular.module("mainApp").directive('slideImgside', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
    valores = [15,30,50,75];

      elm.slider({
        'min':0,
        'max':3,
        'value':scope.$parent.r.cfg.img_box_size,
        'slide':function(event,ui){
            
            scope.$parent.r.cfg.img_box_size=valores[ui.value];
            txtsize = 100 - valores[ui.value];
            scope.$parent.r.cfg.text_box_size=txtsize;
            scope.$apply();
        }

      });

    }
  };

});


angular.module("mainApp").directive('changeImgSide', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
    valores = [15,30,50,75];

      elm.change(function(e){

                    valor = elm.val();
            lados = {'left':'right','right':'left'};
            scope.$parent.r.cfg.txt_pos = lados[valor];
            scope.$parent.r.cfg.img_pos = valor;
            scope.$apply();

      });

    }
  };

});






angular.module("mainApp").directive('slideTabla', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
      console.log('slide',scope);
      elm.slider({
        'min':1,
        'max':20,
        'value':scope.$parent.r.cfg.borde,
        'slide':function(event,ui){
            scope.$parent.r.cfg.borde=ui.value;
            scope.$apply();
        }

      });

    }
  };

});





angular.module("mainApp").directive('addRow', ['$http',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            scope.$parent.boxmods=false;
            modules = scope.modules;

            var pagepk = scope.$parent.wpage.pagepk;
            var typerow = scope.am.typ;
            var derow =  new MODULOS();
            var newrow = derow.getModule(typerow);

            newrow.orden = modules.length + 1;
            newrow.pagepk = pagepk;
            data = {
                'mtitle':newrow.title,
                'typ':newrow.typ,
                'slug':newrow.slug,
                'orden':newrow.orden,
                'pagepk':pagepk
            };

           data = $.param(data);

            params = {'url':'/motor/addmodulo/','method':'POST','data':data};
            $http(params).then(function(response){
                newrow.rowpk = response.data.rowpk;

                var newitm = derow.getItm(typerow);
                newitm.rowpk = response.data.rowpk;
                newrow.items.push(newitm);
                scope.modules.push(newrow);
            });

        });
    }
  };

}]);


angular.module("mainApp").directive('saveRow', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            newrow = scope.r;
            console.log(scope);
            return false;
            data = {

                'mtitle':newrow.title,
                'typ':newrow.typ,
                'slug':newrow.slug,
                'orden':newrow.orden,
                'pagepk':pagepk
            };

           data = $.param(data);



            scope.$apply();
        });
    }
  };

});



angular.module("mainApp").directive('rmRow', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var modules = scope.$parent.modules;
            var row = scope.r;
            var inx = modules.indexOf(row);
            if(confirm('Desea eliminar este módulo?')){
                modules.splice(inx,1);
            }
            scope.$apply();


                data = {
                    'rowpk':row.rowpk
                };

               data = $.param(data);

                params = {'url':'/motor/rmmod/','method':'POST','data':data};
                $http(params).then(function(response){
                    console.log(response.data);
                });


        });
    }
  };

});



/*  CATEGORIA MODULOS */

angular.module("mainApp").directive('addRowCat', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            row = scope.$parent.r;
            var catsnum = row.cats.length+1;

            var newcat = {
                            'catname':'Nueva Categoría',
                            'orden':catsnum,
                            'pk':catsnum,
                            'mycats':[]
                         };
            data = {
            'rowpk':row.rowpk,
            'catname':newcat.name,
            'orden':newcat.catsnum
            };
            data = $.param(data);
            params = {'url':'/motor/addcategoria/','method':'POST','data':data};
            $http(params).then(function(response){
                newcat.catpk = response.data.catpk;
                row.cats.push(newcat);
            });            

            
            //scope.$apply();
        });
    }
  };

});

/* CATEGORIAS */




angular.module("mainApp").directive('rmSubcat', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var parentcat = scope.$parent.c;
            var me = scope.sb;
            inx = parentcat.mycats.indexOf(me);
            if(inx>=0){
                parentcat.mycats.splice(inx,1);
            }
            scope.$apply();

                data = {
                    'catpk':me.catpk
                };

               data = $.param(data);

                params = {'url':'/motor/rmcat/','method':'POST','data':data};
                $http(params).then(function(response){
                    console.log(response.data);
                });


        });
    }
  };

});







/* ---------------[ ITEMS ACTIONS] ---------- */



angular.module("mainApp").directive('addItm', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var typerow = scope.r.typ;
            var derow =  new MODULOS();
            var newitm = derow.getItm(typerow);
            var texto = '';
            if(newitm.descp){
                texto = newitm.descp.toString().replace(/"/g, '\\"');
                texto = texto.toString().replace(/'/g, "&prime;");
                texto = texto.toString().replace(/\\n/g, "\\n");
                texto = texto.toString().replace(/\\&/g, "\\&");
                texto = texto.toString().replace(/\\r/g, "\\r");
                texto = texto.toString().replace(/\\t/g, "\\t");
                texto = texto.toString().replace(/\\b/g, "\\b");
                texto = texto.toString().replace(/\\f/g, "\\f");

            }            



            data = {
                'rowpk':scope.r.rowpk,
                'titulo':newitm.title,
                'descp':texto,
                'orden':newitm.orden
            };

            data = $.param(data);

            params = {'url':'/motor/additm/','method':'POST','data':data};
            $http(params).then(function(response){
                newitm.itmpk = response.data.itmpk;
                scope.r.items.push(newitm);
            });

        });
    }
  };

});


angular.module("mainApp").directive('saveItm', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var newitm = scope.itm;
            scope.itm.publicado=1;
            scope.$apply();


            var texto = '';
            if(newitm.descp){
                texto = newitm.descp.toString().replace(/"/g, '\\"');
                texto = texto.toString().replace(/'/g, "&prime;");
                texto = texto.toString().replace(/\\n/g, "\\n");
                texto = texto.toString().replace(/\\&/g, "\\&");
                texto = texto.toString().replace(/\\r/g, "\\r");
                texto = texto.toString().replace(/\\t/g, "\\t");
                texto = texto.toString().replace(/\\b/g, "\\b");
                texto = texto.toString().replace(/\\f/g, "\\f");
            }            

            data = {
                'itmpk':newitm.itmpk,
                'rowpk':scope.r.rowpk,
                'titulo':newitm.titulo,
                'descp':texto,
                'orden':newitm.orden
            };

            data = $.param(data);

            params = {'url':'/motor/additm/','method':'POST','data':data};
            $http(params).then(function(response){
                scope.itm.itmpk = response.data.itmpk;
            });

        });
    }
  };

});


angular.module("mainApp").directive('saveGridItm', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var newitm = scope.itm;
            scope.itm.publicado=1;
            scope.$apply();
           

            params=[{'type':'params','value':newitm.params.link}];

            data = {
                'itmpk':newitm.itmpk,
                'rowpk':scope.r.rowpk,
                'titulo':newitm.titulo,
                'params':params,
                'clave':'link',
                'orden':newitm.orden
            };

            params = {'url':'/motor/additm/','method':'GET','params':data};
            $http(params).then(function(response){
                scope.itm.itmpk = response.data.itmpk;
            });

        });
    }
  };

});




angular.module("mainApp").directive('saveColorItm', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var newitm = scope.itm;
            scope.itm.publicado=1;
            scope.$apply();
            params=newitm.params;
            console.log(params);

            data = {
                'itmpk':newitm.itmpk,
                'rowpk':scope.r.rowpk,
                'titulo':newitm.titulo,
                'params':params,
                'clave':'link',
                'orden':newitm.orden
            };

            params = {'url':'/motor/addcolor/','method':'GET','params':data};
            $http(params).then(function(response){
                console.log('saved');
            });

        });
    }
  };

});






angular.module("mainApp").directive('saveItmTabla', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var newitm = scope.itm;
            scope.itm.publicado=1;
            scope.$apply();
           

            params=[{'type':'contenido','value':newitm.contenido}];

            data = {
                'itmpk':newitm.itmpk,
                'rowpk':scope.r.rowpk,
                'titulo':newitm.titulo,
                'params':params,
                'orden':newitm.orden,
                'clave':'contenido'
            };

            params = {'url':'/motor/additm/','method':'GET','params':data};
            $http(params).then(function(response){
                
                scope.itm.itmpk = response.data.itmpk;
            });

        });
    }
  };

});





angular.module("mainApp").directive('rmItm', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var row = scope.$parent.$parent.r;
            var itm = scope.itm;
            var inx = row.items.indexOf(itm);
            if(inx>=0 & confirm('¿Desea eliminar este elemento de modo permanente?')){
                row.items.splice(inx,1);
                console.log(inx);
                scope.$apply();

                data = {
                    'itmpk':itm.itmpk
                };

               data = $.param(data);

                params = {'url':'/motor/rmitm/','method':'POST','data':data};
                $http(params).then(function(response){
                    console.log(response.data);
                });


            }
            
        });
    }
  };

});




/* ---------------[END ITEMS ACTIONS] ---------- */



/* ------------ [ IMAGEN ACTIONS ] ------------------ */

angular.module("mainApp").directive('launchFoto', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            drow = scope.$parent.$parent.r;
            aspect_rebase = {'20':5.545918367,'40':2.772959184,'60':1.848639456};
            
            aspects = {'grid':1.413043478,
                       'gridlink':1.413043478,
                       'gridimg':1.413043478,
                       'rebase':aspect_rebase[drow.cfg.alto],
                       'imgrebase':null,
                       'tresseiscero':null,
                   };
            
            scope.itm.typ = drow.typ;
            scope.itm.rowpk = drow.rowpk;
            scope.itm.slug = drow.slug;
            scope.itm.aspectRatio = aspects[drow.typ];
            scope.itmedited.unshift(scope.itm);
            scope.$apply();
            jQuery('#cropperbox').show();
            var $image = $('#image');                  
            $image.attr('src','/static/statics/imgs/defaults/grid.png');
            $image.cropper('destroy');
            scope.$parent.$parent.$parent.launchDrop();
        });

    }
  };

});



angular.module("mainApp").directive('launchFotoTressc', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            drow = scope.$parent.$parent.r;          
            scope.itm.typ = drow.typ;
            scope.itm.rowpk = drow.rowpk;
            scope.itm.slug = drow.slug;
            scope.itm.aspectRatio = null;
            scope.itmedited.unshift(scope.itm);
            scope.$apply();
            jQuery('#cropperbox').show();
            var $image = $('#image');                  
            $image.attr('src','/static/statics/imgs/defaults/imgrebase.png');
            $image.cropper('destroy');
            
            idbox = 'tres-box-'+scope.itm.itmpk;
            scope.$parent.$parent.$parent.directImg();
        });

    }
  };

});




angular.module("mainApp").directive('launchFile', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            drow = scope.$parent.$parent.r;
            scope.itm.typ = drow.typ;
            scope.itm.rowpk = drow.rowpk;
            scope.itm.slug = drow.slug;
            scope.itmedited.unshift(scope.itm);
            scope.$apply();
            jQuery('#upload-file').click();
        });

    }
  };

});



angular.module("mainApp").directive('launchFuente', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            drow = scope.$parent.$parent.r;
            scope.itm.typ = drow.typ;
            scope.itm.rowpk = drow.rowpk;
            scope.itm.slug = drow.slug;
            scope.itmedited.unshift(scope.itm);
            scope.$apply();
            jQuery('#upload-fuente').click();
        });

    }
  };

});


angular.module("mainApp").directive('uploadFile', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.change(function(e){
            $('#velo').show();
            
            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            var elemento = scope.itmedited[0];
            scope.itmedited[0].filename = filename;
            reader.onload = function (e) {
              resultado = e.target.result;
              data = {
                  'rowpk':scope.itmedited[0].rowpk,
                  'itmpk':elemento.itmpk,
                  'filename':filename,
                  'archivestr':resultado
              };
              data = $.param(data);
              params = {'url':'/motor/addfile/','method':'POST','data':data};
              $http(params).then(function(response){
                var files = {'pk':response.data.fpk,'file':response.data.file,'name':response.data.name};
                scope.itmedited[0].files.push(files);
                $('#velo').hide();
              });
            };
            reader.readAsDataURL(file);
        });

    }
  };

}]);


angular.module("mainApp").directive('uploadFuente', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.change(function(e){       
            $('#velo').show();     
            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            var elemento = scope.itmedited[0];
            scope.itmedited[0].filename = filename;
            reader.onload = function (e) {
              resultado = e.target.result;
              data = {
                  'rowpk':scope.itmedited[0].rowpk,
                  'itmpk':elemento.itmpk,
                  'filename':filename,
                  'archivestr':resultado,
                  'titulo':scope.itmedited[0].titulo
              };
              data = $.param(data);
              params = {'url':'/motor/addfile/','method':'POST','data':data};
              $http(params).then(function(response){
                var files = {'pk':response.data.fpk,'file':response.data.file,'name':response.data.name};
                scope.itmedited[0].files=[files];
                scope.itmedited[0].itmpk=response.data.itmpk;
                scope.itmedited[0].params.link=response.data.name;
                scope.loadcss = Date.now();
                $('#velo').hide();
                
              });
            };
            reader.readAsDataURL(file);
             scope.$apply();
        });

    }
  };

}]);



angular.module("mainApp").directive('rmFile', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            var itm = scope.$parent.itm;
            var me = scope.d;
            var inx = itm.files.indexOf(me);
            if(inx>=0 & confirm('¿Desea eliminar este elemento de modo permanente?')){
                itm.files.splice(inx,1);
                scope.$apply();

                data = {
                    'itmfile':me.pk
                };

               data = $.param(data);

                params = {'url':'/motor/rmfile/','method':'POST','data':data};
                $http(params).then(function(response){
                    console.log(response.data);
                });


            }
            
        });
    }
  };

});




angular.module("mainApp").directive('closeCrop', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            jQuery('#cropperbox').hide();
        });

    }
  };

});


angular.module("mainApp").directive('saveCrop', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){


            jQuery('#cropperbox').hide();
            $('#image').cropper("destroy");
            $('#velo').show();

            mediaparams = scope.currmedia;

            datagrid = {
                    'itmpk':scope.itmedited[0].itmpk,
                    'typ':scope.itmedited[0].typ,
                    'slug':scope.itmedited[0].slug,
                    'cropimg':scope.itmedited[0].media.img,
                    'filename':scope.itmedited[0].filename,
                    'rowpk':scope.itmedited[0].rowpk,
                    'prev':mediaparams.cropimg,
                    'fullimg':mediaparams.fullimage
                   };
            

            datarebase = {
                    'itmpk':scope.itmedited[0].itmpk,
                    'typ':scope.itmedited[0].typ,
                    'slug':scope.itmedited[0].slug,
                    'cropimg':scope.itmedited[0].media.img,
                    'filename':scope.itmedited[0].filename,
                    'rowpk':scope.itmedited[0].rowpk,
                    'prev':mediaparams.cropimg,
                    'fullimg':mediaparams.fullimage
                   };
            

            data_bones = {
                          'grid':datagrid,
                          'gridlink':datagrid,
                          'gridimg':datagrid,
                          'rebase':datarebase,
                          'imgrebase':datarebase,
                          'tresseiscero':datarebase,
                          'ambientes':datarebase,
                          'notas':datarebase,
                          'imgside':datarebase
                      };
 

            data = $.param(data_bones[scope.itmedited[0].typ]);

            params = {'url':'/motor/imagen/','method':'POST','data':data};
            
            $http(params).then(function(response){
                var nochaestring = Date.now();
                scope.itmedited[0].itmpk = response.data.itm;
                scope.itmedited[0].media.img = '/'+response.data.img+'?p='+nochaestring;
                scope.itmedited[0].media.full = '/'+response.data.full+'?p='+nochaestring;
                scope.itmedited[0].media.prev = '/'+response.data.prev+'?p='+nochaestring; 
                $('#velo').hide();              
            });
            
            scope.$apply();

        });

    }
  };

}]);


angular.module("mainApp").directive('uploadGridImg', ['$http','$filter',function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.change(function(e){
            
            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            var elemento = scope.itmedited[0];
            scope.itmedited[0].filename = filename;
            aspectRatioDefault = elemento.aspectRatio;
            var $image = $('#image');

            reader.onload = function (e) {
              resultado = e.target.result;
              $image.cropper('replace',resultado);
              jQuery('#cropperbox').show();

            };

            reader.readAsDataURL(file);

          $image.cropper({
              aspectRatio:aspectRatioDefault,
              viewMode:3,
              responsive:true,
              zoomable:true,
              restore:true,
              checkCrossOrigin:true,
              ready: function () {
                croppable = true; 
                

              },
              crop:function(){
                croppedCanvas = $image.cropper('getCroppedCanvas');
                if(croppedCanvas){
                    scope.itmedited[0].media.img = croppedCanvas.toDataURL();
                    scope.itmedited[0].media.full = resultado;
                    scope.$apply();
                    jQuery('#uploader-'+scope.itmedited[0].typ).val('');
                }
              }
          });



        });

    }
  };

}]);



angular.module("mainApp").directive('launchCfg', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){


            largo = scope.bancocats.length;
            scope.bancocats.unshift(scope.itm);
            scope.bancocats.splice(1,largo-1);
            console.log(scope.bancocats);
            scope.$apply();
            $('#myacastitm').show();
        });

    }
  };

});


angular.module("mainApp").directive('closeCfg', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){

            $('#myacastitm').hide();
        });

    }
  };

});



angular.module("mainApp").directive('closeRowCfg', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            data = {'rowpk':scope.$parent.r.rowpk,
                    'cfg':scope.$parent.r.cfg
                };
            
            scope.$parent.r.confiuring=false;
            scope.$apply();

            params = {'url':'/motor/savecfg/','method':'GET','params':data};
            
            $http(params).then(function(response){
                console.log(response.data);
            });



        });

    }
  };

});



angular.module("mainApp").directive('addCatItm', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){
            checado = $(elm).is(':checked');
            catpk = $(elm).val();
            itm = scope.bancocats[0];
            inx = itm.mycats.indexOf(catpk);
            if(checado){
                itm.mycats.push(catpk);
            }
            else{
                itm.mycats.splice(inx,1);
            }

            scope.$apply();

            data = {'itmpk':itm.itmpk,'mycats':itm.mycats};

            params = {'url':'/motor/savemycats/','method':'GET','params':data};
            
            $http(params).then(function(response){
                console.log(response.data);
            });


        });

    }
  };

});



/*  LITRADO   */

angular.module("mainApp").directive('clickFlter', ['$http','$filter',function($scope,$filter,$http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
       
       elm.click(function(e){
          checado = $(elm).is(':checked');
          var pkcat = scope.sb.catpk;
          var newcat = {'pk':scope.sb.catpk,'catname':scope.sb.catname};
          ro = scope.$parent.$parent.$parent.r;

          angular.forEach(ro.items,function(v,k){
            v.visible = '1';
          });

          if(checado){
             ro.catfilts.unshift(newcat); 
          }
          else{
            ro.catfilts.splice(newcat,1);  
          }
        
        angular.forEach(ro.catfilts,function(v,k){

          visibles = ro.items.filter(function (elm) {
            return (elm.visible ==='1');
          });
           
          var porcategoria = visibles.filter(function(itm){
              indice = itm.mycats.indexOf(v.pk.toString());
              if(indice<0)
                itm.visible = '2';
              return (itm.visible === '1');
          });      
        });
        scope.$apply();
       });


    }
  };

}]);



angular.module("mainApp").directive('rmFlter', ['$http','$filter',function($scope,$filter,$http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
       
       elm.click(function(e){
          
          
          checado = false;
          var checkbox = 'check-'+scope.cf.pk;
          jQuery('#'+checkbox).attr('checked', false);

          var newcat = {'pk':scope.cf.pk,'catname':scope.cf.catname};

          var newcat = {'pk':scope.cf.pk,'catname':scope.cf.catname};
          
          ro = scope.$parent.$parent.r;

          angular.forEach(ro.items,function(v,k){
            v.visible = '1';
          });

          if(checado){
             ro.catfilts.unshift(newcat); 
          }
          else{
            ro.catfilts.splice(newcat,1);  
          }
        
        angular.forEach(ro.catfilts,function(v,k){

          visibles = ro.items.filter(function (elm) {
            return (elm.visible ==='1');
          });
           
          var porcategoria = visibles.filter(function(itm){
              indice = itm.mycats.indexOf(v.pk.toString());
              if(indice<0)
                itm.visible = '2';
              return (itm.visible === '1');
          });      
        });
        scope.$apply();
       });


    }
  };

}]);





angular.module("mainApp").directive('addPage', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){
            console.log(scope);
            pagslen = scope.pages.length;
            var newpage = {'pagepk':0,
                           'page_name':'Section '+pagslen,
                           'slug':'new_page',
                           'secs':[],
                           'orden':pagslen
                        };
            
            data = {'pagename':newpage.pagename,'orden':pagslen};
            params = {'url':'/motor/savepage/','method':'GET','params':data};
            
            $http(params).then(function(response){
                console.log(response.data);
                newpage.pagepk = response.data.pagepk;
                newpage.page_slug = response.data.pageslug;
                scope.pages.push(newpage);

            });

        });



    }
  };

});



angular.module("mainApp").directive('addSubPage', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){  
            $('#menucatedit').show();
            scope.$parent.catedit = scope.p.secs;
            scope.$apply();
                    
            pagslen = scope.p.secs.length;
            var cols = {'colpk':0,
                        'colname':'TITULO '+pagslen,
                        'orden':pagslen,
                        'secs':[]};
            data = {
                    'pagepk':scope.p.pagepk,
                    'colname':cols.colname,
                    'colpk':cols.colpk,
                    'orden':pagslen
                };

            params = {'url':'/motor/savecolumna/','method':'GET','params':data};
            $http(params).then(function(response){
                cols.colpk = response.data.colpk;
                scope.p.secs.push(cols);
                //scope.$apply();
            });
        });
    }
  };
});



angular.module("mainApp").directive('saveCol', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.blur(function(e){                      
            col = scope.c;
            data = {'colname':col.colname,'colpk':col.colpk,'orden':col.orden};
            params = {'url':'/motor/savecolumna/','method':'GET','params':data};
            $http(params).then(function(response){
                col.colslug = response.data.slug;
            });
        });
    }
  };
});



angular.module("mainApp").directive('addSubsec', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.click(function(e){  


            lenx = scope.c.secs.length;
            var newpage = {'pagepk':0,
                           'page_name':'Section '+lenx,
                           'slug':'new_page',
                           'orden':lenx
                        };

            data = newpage;
            data.pagecol = scope.c.colpk;

            params = {'url':'/motor/savepage/','method':'GET','params':data};
            $http(params).then(function(response){
                newpage.pagepk = response.data.pagepk;
                newpage.slug = response.data.slug;
                scope.c.secs.push(newpage);

            });            

        });



    }
  };

});



angular.module("mainApp").directive('saveSec', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

        elm.blur(function(e){                      


            data = {};

            if(scope.sb){
                targ = scope.sb;
            }

            if(scope.p){
                targ = scope.p;
            }

            data['pagepk']=targ.pagepk;
            data['pagename'] = targ.page_name;
            if(targ.page_name.trim().length<1){
                alert('El campo no puede ser un valor nulo o vacio');
                return false;
            }

            params = {'url':'/motor/savepage/','method':'GET','params':data};
            $http(params).then(function(response){
                targ.page_slug = response.data.pageslug;
            });
        });
    }
  };
});





angular.module("mainApp").directive('editCat', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){
            $('#menucatedit').show();
            scope.$parent.$parent.catedit = scope.$parent.p.secs;
            scope.$apply();
            

        });



    }
  };

});



angular.module("mainApp").directive('closeCats', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){
            $('#menucatedit').hide();
            scope.$parent.$parent.catedit = [];
            scope.$apply();
        });



    }
  };

});




angular.module("mainApp").directive('rmPage', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){   
            if(confirm('La sección y todo su contenido se eliminara\ ¿Desea continuar?')){
                pages = scope.$parent.pages;
                inx = pages.indexOf(scope.p);
                pages.splice(inx,1);

                data = {'pagepk':scope.p.pagepk};
                params = {'url':'/motor/rmpage/','method':'GET','params':data};
                $http(params).then(function(response){
                    return true;
                });
            }
        });
    }
  };
});



angular.module("mainApp").directive('rmSbPage', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){   


            if(confirm('La sección y todo su contenido se eliminara\ ¿Desea continuar?')){
                pages = scope.$parent.c.secs;
                inx = pages.indexOf(scope.sb);
                pages.splice(inx,1);

                data = {'pagepk':scope.sb.pagepk};
                params = {'url':'/motor/rmpage/','method':'GET','params':data};
                $http(params).then(function(response){
                    return true;
                });
            }
        });
    }
  };
});




angular.module("mainApp").directive('rmColumn', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.click(function(e){   



            if(confirm('La Columna y todo su contenido se eliminara\ ¿Desea continuar?')){

                pages = scope.$parent.catedit;
                inx = pages.indexOf(scope.c);
                pages.splice(inx,1);

                data = {'catpk':scope.c.colpk};
                params = {'url':'/motor/rmcol/','method':'GET','params':data};
                $http(params).then(function(response){
                    return true;
                });
            }
        });
    }
  };
});




/* FOR UPLOAD IMAGES  */


/* FIRST DA DROPZONE ELEMENT */

    


angular.module("mainApp").directive('dropMe', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {

             
      elm.dropzone({
            'url':'/motor/dropimage/',
            'paramName':'filex'
        });
    
    }
  };
});




angular.module("mainApp").directive('tresSeisSeis', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
            div = elm[0];
            var psv = new PhotoSphereViewer({
                          panorama: scope.itm.media.img,
                          container: div,
                          time_anim: 3000,
                          mousewheel:false,
                          markers:[],
                          caption:'',
                          navbar:['autorotate','zoom'],
                          navbar_style: {
                            backgroundColor: 'rgba(58, 67, 77, 0.7)',
                         }
                    });
        scope.$watch('itm.media.img',function(x,y){
            jQuery(div).html('');
            psv = null;
            psv = new PhotoSphereViewer({
                      panorama: scope.itm.media.img,
                      container: div,
                      time_anim: 3000,
                      mousewheel:false,
                      markers:[],
                      caption:'',
                      navbar:['autorotate','zoom'],
                      navbar_style: {
                        backgroundColor: 'rgba(58, 67, 77, 0.7)',
                      }
                });
        });
    }
  };
});



angular.module("mainApp").directive('ambienteLaunch', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        div = elm[0];

        scope.$watch('itm.media.img',function(x,y){
            medias = scope.itm.media.img.indexOf('rebase.png');
            if(medias<0){
                scope.$parent.$parent.$parent.addSfera(div,scope.itm);    
            }

            
        });

        
    }
  };
});






angular.module("mainApp").directive('updateNotaMark', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
        elm.blur(function(e){


            data = {'prmpk':scope.m.id,'tooltip':scope.m.tooltip,'orden':scope.m.orden};
           params = {'url':'/motor/upparam/','method':'GET','params':data};
            $http(params).then(function(response){
                
                updated = true;

            });

            
            scope.$apply();
            

        });

    }
  };
});


angular.module("mainApp").directive('rmNotaMark', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
        elm.click(function(e){
            
            inx = scope.$parent.itm.markas.indexOf(scope.m);

            data = {'prmpk':scope.m.id};
           params = {'url':'/motor/rmparam/','method':'GET','params':data};
            $http(params).then(function(response){
                if(inx>-1)
                    scope.$parent.itm.markas.splice(inx,1);            
            });            
            scope.$apply();
        });

    }
  };
});



angular.module("mainApp").directive('updateMark', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
        elm.blur(function(e){


            data = {'prmpk':scope.m.id,'tooltip':scope.m.tooltip,'orden':scope.m.orden};
           params = {'url':'/motor/upparam/','method':'GET','params':data};
            $http(params).then(function(response){
                
            mypsv = scope.$parent.$parent.$parent.mypsv[scope.$parent.itm.itmpk];
            udatermk = {
                    'id':scope.m.id,
                    'tooltip':scope.m.tooltip,
                    'html':'<span class="redondeo">'+scope.m.orden+'</span>'
                };
            mypsv.updateMarker(udatermk);


            });

            

            

        });

    }
  };
});




angular.module("mainApp").directive('rmMark', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
        elm.click(function(e){
            
            inx = scope.$parent.itm.markas.indexOf(scope.m);

            data = {'prmpk':scope.m.id};
           params = {'url':'/motor/rmparam/','method':'GET','params':data};
            $http(params).then(function(response){
                
                if(inx>-1)
                    scope.$parent.itm.markas.splice(inx,1);
            
                mypsv = scope.$parent.$parent.$parent.mypsv[scope.$parent.itm.itmpk];
                mypsv.removeMarker(scope.m.id);
            });            
            scope.$apply();
        });

    }
  };
});


angular.module("mainApp").directive('launchNotas', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        div = elm[0];

        elm.dblclick(function(e,x){
            H = e.target.height;
            W = e.target.width;
            xplane = e.offsetX;
            yplane = e.offsetY;

            leftpice = ( xplane * 100 ) / W ;
            toppice = ( yplane * 100 ) / H ;


                ordenes = [];
                angular.forEach(scope.itm.markas, function(mk){
                    ordenes.push(mk.orden);
                });

                if(ordenes.length>0){
                    numero = ordenes.reverse()[0];
                    lastorden = numero+1;
                }
                else
                    lastorden = 1;
 


            newarr = {
                    pk:0,
                    'tooltip':'texto aquí',
                    'lat':toppice,
                    'longt':leftpice,
                    'orden':lastorden,
                    'longitude':leftpice,
                    'latitude':toppice
                    };        


            data = {
                'itmpk':scope.itm.itmpk,
                'nota':newarr
            };

            params = {'url':'/motor/addparam/','method':'GET','params':data};
            $http(params).then(function(response){
                newarr['id']=response.data.prmpk;
                scope.itm.markas.push(newarr);
                console.log(newarr);
            });
        });

        scope.$watch('itm.media.img',function(x,y){
            medias = scope.itm.media.img.indexOf('rebase.png');
            if(medias<0){
                console.log('facking awesome');
                //elm.imgNotes();    
            }
            
        });

        
    }
  };
});


angular.module("mainApp").directive('cleaveRgb', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
             var cleave = new Cleave(elm, {
                prefix: '',
                delimiter: ',',
                blocks: [3,3,3],
                uppercase: true
            });

    }
  };
});



angular.module("mainApp").directive('cleaveCmyk', function($http) {
  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
             var cleave = new Cleave(elm, {
                prefix: '',
                delimiter: ',',
                blocks: [2,2,2,2],
                uppercase: true
            });

    }
  };
});



angular.module("mainApp").directive('sortableMe', function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        

      elm.nestedSortable({
              handle: 'div',
              items: 'li:not(.ui-state-disabled)',
              toleranceElement: '> div',
              maxLevels:'2',
              stop:function(event,ui) { 
                brodas = $(ui.item).parent('ol:first').find('.ordermy');
                reorder = [];
                $.each(brodas,function(x,y){
                    vax = angular.element(y).scope();
                    vax.$apply(function() {
                      vax.m.orden = x;
                      neworder = {'pk':vax.m.rowpk,'orden':vax.m.orden};
                      reorder.push(neworder);

                    visibles = scope.modules.filter(function (elm) {
                        if(elm.rowpk ===vax.m.rowpk){
                            elm.orden = vax.m.orden;
                        }
                        return (elm.rowpk ===vax.m.rowpk);
                    });

                    


                    });
                });
                console.log(reorder);

           data = {'listado':reorder};

            params = {'url':'/motor/reorder/','method':'GET','params':data};
            $http(params).then(function(response){
                console.log(response.data);

            });




              }
          });

    }
  };

});


/*  CONFIGURADOR -----------------------------------------------------   */


angular.module("mainApp").directive('launchCfgFuente', function() {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
        elm.click(function(e){
            scope.itmedited.unshift(scope.fu);
            scope.$apply();
            jQuery('#upload-fuente').click();
        });

    }
  };

});



angular.module("mainApp").directive('uploadcfgFuente', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        
        elm.change(function(e){       
            usage = scope.itmedited[0].usage;
            puntaje = scope.itmedited[0].puntaje;
            
            $('#velo').show();     
            var file=e.currentTarget.files[0];
            var reader = new FileReader();
            var filename = file.name;
            reader.onload = function (e) {
              resultado = e.target.result;
              data = {
                  'filename':filename,
                  'archivestr':resultado,
                  'usage':usage,
                  'puntaje':puntaje
              };

              data = $.param(data);
              params = {'url':'/cfg/addfont/','method':'POST','data':data};
              $http(params).then(function(response){
                $('#velo').hide();
                scope.loadcss = Date.now();

              });

            };
            reader.readAsDataURL(file);
            scope.itmedited.splice(0,1);
            scope.$apply();
        });        

    }
  };

}]);



angular.module("mainApp").directive('saveFont', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){
            $('#velo').show();

              data = {
                  'usage':scope.fu.usage,
                  'puntaje':scope.fu.puntaje
              };
              
              data = $.param(data);
              params = {'url':'/cfg/addfont/','method':'POST','data':data};
              $http(params).then(function(response){
                $('#velo').hide();
                scope.loadcss = Date.now();
              });

              scope.$apply();
        });        

    }
  };

}]);



angular.module("mainApp").directive('changeColor', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
    elm.keypress(function(e){
        r = parseInt(scope.$parent.c.colorset.rgb.r);
        g = parseInt(scope.$parent.c.colorset.rgb.g);
        b = parseInt(scope.$parent.c.colorset.rgb.b);
        solidColor = r+','+ g +','+b;
        rgbColor = 'rgb('+solidColor+')';
        hexcolor = w3color(rgbColor).toHexString();
        scope.$parent.c.colorset.hex = hexcolor.replace('#','');
        scope.$apply();

        


    });

        

    }
  };

}]);


angular.module("mainApp").directive('saveColor', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){
            visibles = scope.colors.filter(function (elm) {
                return (elm.gama === true);
            });
            
            data = {'cual':visibles};

            //$('#velo').show();
              params = {'url':'/cfg/addcolor/','method':'GET','params':data};
              $http(params).then(function(response){
                $('#velo').hide();
                
              });

              scope.$apply();
        });        

    }
  };

}]);



angular.module("mainApp").directive('changeColorSettings', ['$http','$filter',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        

        elm.click(function(e){
            backcolor = scope.$parent.$parent.bc.colorset.hex;
            fontcolor = scope.$parent.fc.colorset.hex;
            data = {
                'backcolor':backcolor,
                'fontcolor':fontcolor
            };

              params = {'url':'/cfg/addsett/','method':'GET','params':data};
              $http(params).then(function(response){
                $('#velo').hide();
                scope.$parent.$parent.$parent.loadcss = Date.now();
                
              });             

              scope.$apply();
        });        

    }
  };

}]);






angular.module("mainApp").directive('sendData', ['$http',function($http) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {
        elm.submit(function(e){

          jQuery('.errform').remove();
            elemento = e.target;
            uri = jQuery(elemento).attr('action');
            data = jQuery(elemento).serializeArray();
            data.push({'name':'imagen','value':scope.imgbrand.replace(/^data:image\/(png|jpeg);base64,/, "")});
            data = data = $.param(data);
            $http({'url':uri,method:'POST',data:data}).then(function(response){
                
                if(response.data.errors){
                     angular.forEach(response.data.errors,function(vaue,key){
                        jQuery('#id_'+key).after('<div class="errform">'+vaue+'</div>');
                    });
                }
                else{
                  jQuery('#id_pk').val(response.data.saved);
                  scope.userprofile['ok'] = response.data.saved;
                  scope.userprofile['domain'] = response.data.domain;
                  scope.userprofile['path'] = response.data.path;
                  scope.paso++;
                  scope.pasosvalidos.unshift(1);
                  scope.$apply();
                }
            });

            return false;
        });

    }
  };

}]);



/* CALENDARIO  DIRECTIVES */


angular.module("mainApp").directive('filtPromo', ['$filter',function($filter) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){

          scope.promociones = scope.promociones.filter(function (elm) {
            console.log(scope.reds.indexOf(elm.pk.toString()));            
            return (scope.reds.indexOf(elm.pk.toString())>-1);
          });

        scope.$apply();

        });



    }
  };

}]);




angular.module("mainApp").directive('activePromo', ['$filter',function($filter) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){

          scope.promociones = scope.allpromociones;  
          scope.promociones = scope.promociones.filter(function (elm) {
                    console.log(scope.activas.indexOf(elm.pk.toString()));   
            return (scope.activas.indexOf(elm.pk.toString())>-1);
          });

        scope.$apply();

        });



    }
  };

}]);



angular.module("mainApp").directive('todosPromo', ['$filter',function($filter) {

  return {
    restrict: 'A',
    link: function(scope, elm, attrs) {


        elm.click(function(e){
            scope.promociones = scope.allpromociones;
            scope.$apply();
        });



    }
  };

}]);