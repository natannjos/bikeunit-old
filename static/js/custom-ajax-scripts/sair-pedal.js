$(function() {
    var loadModal = function(){
        var anchor = $(this);

        $.ajax({
            url: anchor.attr('data-url'),
            type: 'get',
            dataType: 'json',
            success: function(data) {
                $('#modal4').html(data.html_form)
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.tem_pedais){
                //     $('#meus-pedais-agendados').html(data.html_pedais_agendados_list)
                // } else {
                //     $('#pedais-agendados-li').remove()
                // }
            }
        });
        return false
    }

    $('#meus-pedais-agendados').on('click', '.js-perfil-sair-pedal', loadModal)
    $('#modal4').on('submit', '.js-perfil-sair-pedal-form', saveForm)
})
