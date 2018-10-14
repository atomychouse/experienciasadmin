


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




myapp.controller('pageCtr',function($scope,$http,$filter){

    $scope.loadcss = 1;
    $scope.itmedited = [];

    $scope.font_usages = [
        {
        'usage':'titulos',
        'label':'Títulos',
        'puntaje':'72',
        'texto':'ABCDEFGHIJKLMNOPQRS'
        },
        {
        'usage':'subtitulos',
        'label':'Subtítulos',
        'puntaje':'32',
        'texto':'ABCDEFGHIJKLMNOPQRS'
        },
        {
        'usage':'textos',
        'label':'Textos',
        'puntaje':'18',
        'texto':'ABCDEFGHIJKLMNOPQRS'
        },
    ];



    $scope.colors = [
        {'typo':'primario','colorset':{'hex':'4c4c4c','rgb':{'r':'120','g':'120','b':'120'}},'gama':true},
        {'typo':'secundario','colorset':{'hex':'4FA5EC','rgb':{'r':'120','g':'120','b':'120'}},'gama':true},
        {'typo':'default','colorset':{'hex':'000000','rgb':''},'gama':false},
        {'typo':'default','colorset':{'hex':'ffffff','rgb':''},'gama':false}
    ];

    console.log(colors);


    angular.forEach(fonts,function(v,k){
        visibles = $scope.font_usages.filter(function (elm) {
            if(elm.usage==v.usage){
                elm.texto = v.namefont;
                elm.puntaje = v.puntaje;
            }
            return (elm.visible ==='1');
        });
    });

    angular.forEach(colors,function(v,k){
        visibles = $scope.colors.filter(function (elm) {
            if(elm.typo==v.typo){
                elm.colorset.hex = v.hex;
                rgbpices = v.rgb.split(',');
                elm.colorset.rgb.r = rgbpices[0];
                elm.colorset.rgb.g = rgbpices[1];
                elm.colorset.rgb.b = rgbpices[2];
                
            }
            return (elm.visible ==='1');
        });
    });




});

