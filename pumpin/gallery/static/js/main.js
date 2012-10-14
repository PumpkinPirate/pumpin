function chooseOverlay()
{
    var i = $("#id_overlay").val()
    $("#overlay_box img").hide()
    $("#overlay_" + i).show()
}

var offsetX = 0
var offsetY = 0

function positionMousedown(event)
{
    $(document).mousemove(positionMousemove)
    $(document).mouseup(positionMouseup)
    
    position = $("#overlay_box").offset()
    offsetX = event.pageX - position.left
    offsetY = event.pageY - position.top
    
    return false
}

function positionMousemove(event)
{
    $("#overlay_box").offset({left: event.pageX - offsetX, top: event.pageY - offsetY})
    
    var position = $("#overlay_box").position()
    $("#id_x").val(position.left)
    $("#id_y").val(position.top)
    
    return false
}

function positionMouseup(event)
{
    $(document).unbind("mousemove")
    $(document).unbind("mouseup")
    
    return false
}

function setupTrayScroll(tab)
{
    var tray = $("#"+tab+"_tray")
    tray.data("next_page", 1)
    
    function trayScroll(event)
    {
        if (tray[0].scrollHeight - tray.scrollTop() - tray.height() < 200)
        {
            loadPage(tab)
        }
    }
    
    tray.scroll(trayScroll)
}


function loadPage(tab)
{
    var tray = $("#"+tab+"_tray")
    n = tray.data("next_page")
    tray.unbind("scroll")
    
    $.get("/"+tab+"/"+n+"/", function (content) {
        tray.append(content)
        
        if (content.length)
        {
            setupTrayScroll(tab)
            tray.data("next_page", n+1)
        }
    })
}

$(function () {
    chooseOverlay()
    $("#id_overlay").change(chooseOverlay)
    
    $("#edit_box").mousedown(positionMousedown)
    
    $("#tabs a").click(function () {
        var self = $(this)
        $("#tabs a").removeClass("active")
        self.addClass("active")
        
        $(".tray").hide()
        $("#" + self.attr("id") + "_tray").show()
        
        return false
    })
    
    $("#overlay_choices img").click(function () {
        var self = $(this)
        $("#id_overlay").val(self.attr("data-overlay-id"))
        chooseOverlay()
    })
    
    $("#report").click(function () {
        var self = $(this)
        $.get(self.attr("href"), function() {
            document.location.reload()
        })
        
        return false
    })
    
    setupTrayScroll("popular")
    setupTrayScroll("latest")
    
    $(".tray img").click(function () {
        var self = $(this)
        console.log(this)
        $("#feature_img").attr("src", self.attr("data-image-src"))
        $("#feature_url").val("http://pumpingironwithpaulryan.com" + self.attr("data-page-url"))
        $("#report").attr("href", self.attr("data-report-url"))
    })
})