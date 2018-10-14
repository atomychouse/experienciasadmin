var IMAGEPROCESS = function(){


    this.imagecode = null;
    this.aspectRatioDefault = null;
    this.itm = null;

    this.grid = function(){
    	console.log('esto es un grid');
    	console.log(this.itm);
    	this.aspectRatioDefault = 1.3829787234042554;
    	var $image = $('#image');

          $image.cropper({
              aspectRatio:this.aspectRatioDefault,
              viewMode:2,
              responsive:true,
              zoomable:false,
              restore:true,
              checkCrossOrigin:true,
              ready: function () {
                croppable = true; 
                

              },
              crop:function(){
                croppedCanvas = $image.cropper('getCroppedCanvas');
                if(croppedCanvas){
                    scope.elemToEdit[0].img = croppedCanvas.toDataURL();
                    scope.elemToEdit[0].fullimage = resultado;
                    scope.$apply();
                  
                }
              }
          });


    }


    this.rebase = function(){
    	console.log('esto es un rebase');
    }


    this.descarga = function(){
    	console.log('esto es un descarga');
    }





};
