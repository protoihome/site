$(document).ready(function() {

    
     var get = getRouteParameter();
     var id = get.id;
     
     $.ajax({
        url: "http://10.1.14.22:5000/devices",
        type: 'POST',
        data: {id:id},
        dataType: "json",
        success: function(result){
        
            var content = '<div class="col-xs-12"><h3> Lista de Aparelhos</h3></div>';
            var nome = "";
            var dispositivo = "";
            var button = "";
            var acao = "";
    
            for(var i = 0; i < result.aparelhos.length; i++) {

                nome = '<h5>' + result.aparelhos[i].nome + '</h5>';

                dispositivo = '<h1><i class="glyphicon glyphicon-lamp"></i></h1>';

                if(result.aparelhos[i].status == 1) {

                    button = '<button class="btn btn-default btn-block btn-lg btn-equipamento btn-on" data-estado="0" data-id="' + result.aparelhos[i].id + '">';

                    status = '<p class="status">status: <span class="text-success">Ligado</span></p>';

                    acao = '<p class="acao">Desligar</p>';

                } else {

                    button = '<button class="btn btn-default btn-block btn-lg btn-equipamento btn-off" data-estado="1" data-id="' + result.aparelhos[i].id + '">';

                    status = '<p class="status">status: <span class="text-danger">Desligado</span></p>';

                    acao = '<p class="acao">Ligar</p>';

                }


                content = content + '<div class="col-xs-12 col-sm-6 col-md-4">' + button + nome + status + dispositivo + acao + ' </button> </div>';

            }

            $('#content').html(content);
            
            
            
            $('.btn-equipamento').click(function(){

                var estado = $(this).data('estado');
                var aparelho_id = $(this).data('id');

                var status = $(this).children('.status');
                var acao = $(this).children('.acao');
                var span = status.children('span');
                
                var equipamento = $(this);
                
                $.ajax({
                
                    url: "http://10.1.14.22:5000/swap",
                    type:'POST',
                    data: {id:aparelho_id, estado:estado},
                    dataType: "json",
                    success: function(response){
                        
                        console.log(response);
                        if(response.status == '0') {
                            equipamento.data('estado','1');
                            equipamento.addClass('btn-off').removeClass('btn-on');
                            span.addClass('text-danger').removeClass('text-success');
                            span.html('Desligado');
                            acao.html('Ligar');

                        } else {
                            equipamento.data('estado','0');
                            equipamento.addClass('btn-on').removeClass('btn-off');
                            span.addClass('text-success').removeClass('text-danger');
                            span.html('Ligado');
                            acao.html('Desligar');

                        }
                        
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
                       alert(msg);
                    },
                    complete: function(){
//                        navigator.notification.alert("Completo!",  null, 'Resposta da Conexão', 'ok');
                    }

                });

                

            });
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
                        alert(msg);
        },
        complete: function(){
//            navigator.notification.alert("Completo!",  null, 'Resposta da Conexão', 'ok');
        }
    });
    // body...
});