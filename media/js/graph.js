function Graphs() {
    /* data: dictionary of the format:
        {id1: [[x1, y1], [x2, y2], ...], id2: ...]

        for this function to work, there must be a container in the page 
        already with id='graph<id>' where <id> is the id of the 
        site in the data passed into the function
    */
    Graphs.prototype.display = function(data, mintick) {    
        for (var id in data) {
            for (var point in data[id])
                data[id][point][0] *= 1000;
            $.plot($("#graph"+id),
                [data[id]], {
                    xaxis: {
                        mode: "time",
                        minTickSize: mintick
                    },
                    yaxis: {
                        min: 0,
                        max: 100,
                    },
                    lines: {
                        show: true, 
                        fill: true,
                        fillColor: "rgba(0, 255, 0, 0.7)",
                        lineWidth: 3
                    },
                    points: {show: true},
                    grid: {
                        backgroundColor: "#cc0000"
                    },
                    colors: ["#000000"]
                }); 
        }
    }
}

function PageFX() {
    PageFX.prototype.bindEffects = function() {
        // this.bindMiniMax();
        this.bindDragAndDrop();
        this.bindTooltip();
    }

    PageFX.prototype.bindTooltip = function() {
        $('.graph').bind('plothover', function(event, pos, item) {
            if (item) 
            {
                if (previousPoint != item.datapoint) 
                {
                    previousPoint = item.datapoint;
                    $("div#tooltip").addClass("hidden");
                    var x = item.datapoint[0].toFixed(2);
                    var y = item.datapoint[1].toFixed(2);
                    
                    showTooltip(item.pageX, item.pageY, '');
                }
            }
        });
    }

    PageFX.prototype.hideTooltip = function() {
        $('div#tooltip').addClass("hidden");
    }

    PageFX.prototype.showTooltip = function(content, x, y) {
        $('div#tooltip').html(content);
        $('div#tooltip').removeClass("hidden");
        $('div#tooltip').css({
            'left': x,
            'top': y,
        });
    }

    PageFX.prototype.bindMiniMax = function() {
        $(".site_label").click(function () {
            if ($(this).parents(":first").hasClass("moved"))
                $(this).parents(":first").removeClass("moved");
            else
                $(this).siblings(":first").toggleClass("minimized");
        });
    }

    PageFX.prototype.bindDragAndDrop = function() {
        $("#content").sortable({
            tolerance: 'pointer',
            start: function(event, ui) {
                ui.item.addClass("moved");
            },
            stop: function() {
                $.cookie('graph_order', $('ul').sortable("toArray"), {root: '/'});
            }
        });
        $("#content").disableSelection();
    }
}
