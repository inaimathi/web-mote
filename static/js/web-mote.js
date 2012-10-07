var util = {
    requestJSON : function (url, dat, type) {
	var res = null;
	$.ajax({
	    url: url,
	    data: dat,
	    type: type,
	    success: function (data, ret, jq) { 
		// some browsers error if you try to use the data value here, 
		// so we use jq.responseText. It provides the same contents, 
		// but doesn't error
		res = $.parseJSON(jq.responseText); 
	    },
	    async: false
	});
	return res;
    },
    getJSON : function (url, dat) { 
	return util.requestJSON(url, dat, "GET"); 
    },
    postJSON : function (url, dat) { return util.requestJSON(url, dat, "POST"); }
};

var mote = {
    targetId: "#file-list",
    render: function (fileList) {
	if (fileList) {
	    $(mote.targetId).empty();
	    $.each(fileList,
		   function (index, e){
		       if (e.type == "directory") 
			   $(mote.targetId).append(templates.folder(e))
		       else 
			   $(mote.targetId).append(templates.file(e))
		   })
		}
    },
    renderButton: function (control) {
	
    },
    renderControls: function (controlLists) {
	$.each(controlLists,
	       function (index, e) {
		   $("#controls").append(templates.controlBlock(e));
	       })
	    },
    play: function (file) {
	console.log(["cmd", "play", file]);
	$.post("/play",
	       {"file" : file},
	       function (data, textStatus) { 
		   console.log(["now playing", file, textStatus]);
	       });
    },
    shuffleDir: function (dir) {
	console.log(["SHUFFLE", dir]);
	$.post("/shuffle-directory", {"dir": dir});
    },
    command: function (cmd) {
	console.log(cmd);
	$.post("/command", {"command": cmd},
	       function () {
		   if (cmd == "pause") {
		       var btn = templates.control({cmd: "play", "css-class": "big"});
		       $("#controls button.pause").replaceWith(btn);
		   } else if (cmd == "play") {
		       var btn = templates.control({cmd: "pause", "css-class": "big"});
		       $("#controls button.play").replaceWith(btn);
		   }
	       })
    },
    navigate: function (dir) {
	console.log(["cmd", "display", dir]);
	mote.render(util.postJSON("/show-directory", {"dir": dir}));
    }
}

Handlebars.registerHelper("control-button", function (ctrl) {
    return new Handlebars.SafeString(templates.control(ctrl));
});

var templates = {
    folder : Handlebars.compile($("#tmp-folder").html()),
    file : Handlebars.compile($("#tmp-file").html()),
    control: Handlebars.compile($("#tmp-control").html()),
    controlBlock : Handlebars.compile($("#tmp-control-block").html())
}

var Routes = Backbone.Router.extend({ 
    routes: {
	"navigate*path": "nav"
    },
    nav: mote.navigate
});

// older versions of safari don't like `position: fixed`.
// they also don't like when you set `position: fixed` in a stylesheet,
//   then override that with inline styles.
// what I'm saying is that older versions of safari are assholes
if ($.browser.safari) {
    $("#controls").css({ "position": 'absolute' });
    window.onscroll = function() {
	$("#controls").css({ 
	    "position": 'absolute',
	    "top" : window.pageYOffset + 'px'
	});
    };
} else {
    $("#controls").css({ "position": 'fixed' });    
}

$(document).ready(function() {
    mote.renderControls(
	[[{cmd: "rewind-big"}, {cmd: "rewind"}, {cmd: "ff"}, {cmd: "ff-big"}],
	 [{cmd: "volume-down"}, {cmd: "mute"}, {cmd: "volume-up"}],
	 [{cmd: "stop", "css-class": "big"}, {cmd: "pause", "css-class": "big"}]]);
    mote.render(util.postJSON("/show-directory"));

    new Routes();
    Backbone.history.start();
});