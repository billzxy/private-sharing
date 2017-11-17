$(document).ready(function(){
    var lfield = $("#loginField");
    var rfield = $("#regField");

    $("#login").click(function(){
        checkRField();
        rfield.attr("hidden","hidden");
        lfield.removeAttr("hidden");
    });
    $("#reg").click(function(){
        rfield.removeAttr("hidden");
        lfield.attr("hidden","hidden");
    });


});
