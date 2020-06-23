(function ($, window, geralUI, container) {
    "use strict";

    var $container = $(container),
        $ui = null;

    var ui = {
        urlClassificador: 'http://localhost:5000/predict',

        eventos: {},

        inicializar: function ()
        {
            $ui = $(this);
            ui.addEvents();

        },

        addEvents: function () {
            $(document).ready(function (e) {
                $('#myform').on('submit',(function(e) {
                    e.preventDefault();
                    var formData = new FormData(this);
            
                    $.ajax({
                        type:'POST',
                        url: $(this).attr('action'),
                        data:formData,
                        cache:false,
                        contentType: false,
                        processData: false,
                        success:function(data){
                            console.log("success");
                            console.log(data);
                            if (data.predictions.includes("Normal") == true){
                                $("#resultado").text(data.predictions)
                                $('#resultado').css("display", "block")
                                $('#resultado').removeClass("alert-danger")
                                $('#resultado').addClass("alert-success")
                            }else{
                                $("#resultado").text(data.predictions)
                                $('#resultado').css("display", "block")
                                $('#resultado').removeClass("alert-sucess")
                                $('#resultado').addClass("alert-danger")
                            }
                        },
                        error: function(data){
                            console.log("error");
                            console.log(data);
                            $("#resultado").text("Ocorreu um erro na conecção com o servidor de classificação")
                            $('#resultado').css("display", "block")
                            $('#resultado').addClass("alert-danger")
                        }
                    });
                }));
                $("#ImageBrowse").on("change", function() {
                    readURL(this);
                    $("#imageUploadForm").submit();
                });
                function readURL(input) {
                    if (input.files && input.files[0]) {
                      var reader = new FileReader();
                      
                      reader.onload = function(e) {
                        $('#blah').attr('src', e.target.result);
                        $('#pImage').css("display", "block");
                      }
                      
                      reader.readAsDataURL(input.files[0]); // convert to base64 string
                    }
                  }
                  
                  $("#imgInp").change(function() {
                    readURL(this);
                  });
            });
        }
    };

    window.index = {};
    window.index.ui = ui;

})(jQuery, window, window.document);
