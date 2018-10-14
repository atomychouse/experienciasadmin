var MODULOS = function(){

    var QUIZ = {};
    QUIZ['trivia'] = {
                'pk':0,
                'indice':'','pregunta':'¿Pregunta?',
                'img':'/static/statics/imgs/defaults/rebase.png',
                'options':[
                {'indice':'A','texto':'opción 1','orden':1,'cor':false},
                {'indice':'B','texto':'opción 2','orden':2,'cor':false},
                {'indice':'C','texto':'opción 3','orden':3,'cor':false}
                ],
                'orden':2
            };


    QUIZ['palabras'] = {
                'pk':0,
                'indice':'','palabra':'',
                'img':['/static/statics/imgs/defaults/rebase.png',''],
                'palabra':'',
                'orden':1
            };



    QUIZ['sopa'] = {'palabra':''};



    QUIZ['marcador_futbol'] = {
                'pk':0,
                'imgs':[
                    {'img':'','marcador':''},
                    {'img':'','marcador':''},
                ],
                'description':'',
                'respuesta':'True'

            };


    QUIZ['swiper'] = {
            };


            this.quiz = QUIZ;


    this.getQuiz = function(cual){
        return this.quiz[cual];

    }


    this.getModule = function(slugrow){
      this.slugrow = slugrow;



        try {
            this.response = this.modulos[slugrow];
        }
        catch(err) {
            console.log(err);
            this.response = null;
        }
        return this.response;
    };

  this.getItm = function(slugrow){
        this.slugrow = slugrow;        
  
       try {
            this.response = this.itms[slugrow];
        }
        catch(err) {
            
            alert(err);
            this.response = null;
        }
        return this.response;

    };
      
};





function safeText(texto){
    try{
        texto = texto.toString().replace(/"/g, '\\"');
        texto = texto.toString().replace(/'/g, "&prime;");
        texto = texto.toString().replace(/\\n/g, "\\n");
        texto = texto.toString().replace(/\\&/g, "\\&");
        texto = texto.toString().replace(/\\r/g, "\\r");
        texto = texto.toString().replace(/\\t/g, "\\t");
        texto = texto.toString().replace(/\\b/g, "\\b");
        texto = texto.toString().replace(/\\f/g, "\\f");
    }
    catch(err){
        texto = '';
    }

    return texto;
}