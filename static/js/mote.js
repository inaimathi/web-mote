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

function FileListCtrl ($scope) {
    $scope.filesList = util.postJSON("/show-directory");

    $scope.play = function (path) { 
	console.log(["PLAYING FILE", path]) 
    }

    $scope.shuffle = function (path) { 
	console.log(["SHUFFLING DIRECTORY", path])
    }
};

function CommandCtrl ($scope) {
    $scope.controlTree = [
	[ //{cmd: "step-backward"},
    	    {cmd: "backward", held: true},
    	    {cmd: "stop"},
    	    {cmd: "pause"},
    	    {cmd: "forward", held: true}
    	    //{cmd: "step-forward"}
	],
    	[{cmd: "volume-down", held: true}, 
    	 {cmd: "volume-off"}, 
    	 {cmd: "volume-up", held: true}]
    ]

    $scope.command = function (cmd) { 
	console.log(["Sent command", cmd]) 
    }

    $scope.hold = function (cmd) {
	console.log(["Holding command", cmd]) 
    }

    $scope.release = function (cmd) { 
	console.log(["Released command"]) 
    }
}

// older versions of safari don't like `position: fixed`.
// they also don't like when you set `position: fixed` in a stylesheet,
//   then override that with inline styles.
// what I'm saying is that older versions of safari are assholes
if ($.browser.safari) {
    $("#controls").css({ "position": 'absolute' });
    window.onscroll = function() {
	$("#controls").css({ 
	    "top" : window.pageYOffset + 'px'
	});
    };
} else {
    $("#controls").css({ "position": 'fixed' });    
}