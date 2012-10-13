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

$(function () {
    chooseOverlay()
    $("#id_overlay").change(chooseOverlay)
    
    $("#edit_box").mousedown(positionMousedown)
})