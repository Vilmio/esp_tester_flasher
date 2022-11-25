var version = "0.0"

function start_testing(){
    $.ajax({
        type: "POST",
        url: "/test",
        async: !0,
        data: JSON.stringify({ cmd: "start_test"}),
        success: function (e) {
            clearTimeout(timer)
            if (e.Status === "ok"){
                $("#output").append("<br>")
                $("#output").append("4. The test process was succesfully -> <br><code>"+e.Detailes+"</code>")
                $("#test").text("Start")

            }else{
                $("#test").text("Start")
                $("#output").append("3. <code>"+e.Status+"</code>")
            }
        },
        error: function () {
            
        },
    });
}

$(function () {
    $("div.mainContainer").load("overview", function () {
        $(".loader").hide(100);
        $('<button type="button" id="test" class="btn btn-primary btn-lg">Start</button>').appendTo("#testContainer");
        $.ajax({
            type: "POST",
            url: "/test",
            async: !0,
            data: JSON.stringify({ cmd: "get_firmware_version"}),
            success: function (e) {
                version = e.Status
            },
        });
        }
    )
});
$(document).on("click", "#test", function () {
    if($("#test").text() === "Start"){
        $("#test").text("Flashing .. "),
        $("#output").text(""),
        $("#output").append("1. Erasing and flashing firmware with version: <code>"+version+"</code> "), 
        $("#test").append('<span class="spinner-border spinner-border-sm"></span>'),
        (timer = setInterval(function () {
            $("#output").append(".")
        }, 1e3));

        $.ajax({
            type: "POST",
            url: "/test",
            async: !0,
            data: JSON.stringify({ cmd: "start_flashing"}),
            success: function (e) {
                clearTimeout(timer)
                if (e.Status === "ok"){
                    $("#output").append("<br>")
                    $("#output").append("2. <strong> The erasing and flashing process was successful! </strong>")
                    $("#output").append("<br>")
                    $("#output").append("3. Testing ")
                    timer = setInterval(function () {$("#output").append(".")}, 1e3);
                    $("#test").text("Testing .. ")
                    $("#test").append('<span class="spinner-border spinner-border-sm"></span>')
                    start_testing()

                }else{
                    $("#test").text("Start")
                    $("#output").append("<br>")
                    $("#output").append("2. <code>"+e.Status+"</code>")
                }
                console.log(e.Status)
    
            },
            error: function () {
                
            },
            
        });

    }
})
