 $(function(){

    $(".dropdown-menu li a").click(function(){

      $("#countrydropdown").text($(this).text() + '&nbsp;<span class="caret"></span>');
      $("#countrydropdown").val($(this).text());

   });

});