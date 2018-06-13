﻿/*================================================================================
	Item Name: Materialize - Material Design Admin Template
	Version: 3.1
	Author: GeeksLabs
	Author URL: http://www.themeforest.net/user/geekslabs
================================================================================

NOTE:
------
PLACE HERE YOUR OWN JS CODES AND IF NEEDED.
WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR CUSTOM SCRIPT IT'S BETTER LIKE THIS. */

// Datepicker translation
$.extend($.fn.pickadate.defaults, {
    monthsFull: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    monthsShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    weekdaysFull: ['Domingo', 'Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado'],
    weekdaysShort: ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'],
    today: 'Hoje',
    clear: 'Limpar',
    close: 'Fechar',
    format: 'dd/mm/yyyy',
    formatSubmit: 'dd/mm/yyyy',

    labelMonthNext: 'Próximo Mês',
    labelMonthPrev: 'Mês Anterior',
    labelMonthSelect: 'Selecione um Mês',
    labelYearSelect: 'Selecione um Ano',
});

$('.datepicker').pickadate({
    selectYears: 100,
    selectMonths: true,
    max: true,
})

/*Show entries on click hide*/
$(document).ready(function(){
    $(".dropdown-content.select-dropdown li").on( "click", function() {
        var that = this;
        setTimeout(function(){
        if($(that).parent().hasClass('active')){
                $(that).parent().removeClass('active');
                $(that).parent().hide();
        }
        },100);
    });
});


$(document).ready(function(){ 
  
  $('label').find("input[type=search]").each(function(ev)  {
    	if(!$(this).val())
    		$(this).attr("placeholder", "Digite o que deseja ");  		
  });
});

