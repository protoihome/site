/*jshint browser:true */
/*global $ */(function()
{
 "use strict";
 /*
   hook up event handlers 
 */
 function register_event_handlers()
 {
     /* button  #alertar */
     var rota = "http://10.1.14.22:5000/room";
    
    $.ajax({
        url: rota,
        dataType: "json",
        success: function(result){
        
            var navli = "";
          

            for(var i = 0; i < result.room.length; i++) {
               
                navli = navli + '<li><a href="/comodos?id=' + result.room[i].id + '">' +  result.room[i].nome; + '</a></li>';
                
            }

            $('#menu .navbar-nav').append(navli);
            
        },
         error:function (jqXHR, exception) {
                        var msg = '';
                        if (jqXHR.status === 0) {
                            msg = 'Not connect.\n Verify Network.';
                        } else if (jqXHR.status == 404) {
                            msg = 'Requested page not found. [404]';
                        } else if (jqXHR.status == 500) {
                            msg = 'Internal Server Error [500].';
                        } else if (exception === 'parsererror') {
                            msg = 'Requested JSON parse failed.';
                        } else if (exception === 'timeout') {
                            msg = 'Time out error.';
                        } else if (exception === 'abort') {
                            msg = 'Ajax request aborted.';
                        } else {
                            msg = 'Uncaught Error.\n' + jqXHR.responseText;
                        }
                        navigator.notification.alert(msg + 'rota: ' + rota);
        },
        complete: function(){
//            navigator.notification.alert("Completo!",  null, 'Resposta da Conexão', 'ok');
        }
    });
    
    
    }
 document.addEventListener("app.Ready", register_event_handlers, false);
})();
