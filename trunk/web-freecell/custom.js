var g_count=1;
$(function() {
	$("#btn1").click(function() {
		if(g_count <= 54) {
		    card_fn = "cards/card_" + g_count + ".gif";
		    //console.log("card_fn is %s", card_fn);
		    img_html="<img src=\"" + card_fn + "\">";
		    console.log("img is %s", img_html);
		    $("#card_field").html(img_html);
		    g_count++;
		}
	    });
    });
