var util = {
    post: function ($http, url, data) {
	var encoded = _.map(data, function (val, k) { return encodeURI(k) + "=" + encodeURI(val); });
	$http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
	return $http.post(url, encoded.join("&"));
    },
    browser: function () { 
	/// Adapted from jQuery.browser()
	/// Yes, I know it's frowned upon, fuck you. 
	/// I need quick&dirty version detection for a SPECIFIC type of old-ass Safari.
	/// This is sufficient if inelegant.
	var ua = navigator.userAgent.toLowerCase();
	var match = /(chrome)[ \/]([\w.]+)/.exec( ua ) ||
	    /(webkit)[ \/]([\w.]+)/.exec( ua ) ||
	    /(opera)(?:.*version|)[ \/]([\w.]+)/.exec( ua ) ||
	    /(msie) ([\w.]+)/.exec( ua ) ||
	    ua.indexOf("compatible") < 0 && /(mozilla)(?:.*? rv:([\w.]+)|)/.exec( ua ) ||
	    [];
	return {agent: match[1] || "", version: match[2] || "0"}
    }
};

function FileListCtrl ($scope, $http, $location) { 
    $scope.navigate = function (path) {
	util.post($http, "/show-directory", { dir: path || $location.path() })
	    .success(function (data, status, headers, config){
		$scope.filesList = data;
	    });
	$location.path(path || $location.path())
    }

    $scope.play = function (path) { 
	util.post($http, "/play", {target: path})
    }

    $scope.shuffle = function (path) { 
	util.post($http, "/play", {target: path, shuffle: true})
    }
};

function CommandCtrl ($scope, $http) {
// older versions of safari don't like `position: fixed`.
// they also don't like when you set `position: fixed` in a stylesheet then override with inline styles.
// what I'm saying is that older versions of safari are assholes
    if (util.browser().agent == 'safari') {
	$scope.style = { position: "absolute", top : window.pageYOffset + 'px' };
	window.onscroll = function() { 
	    $scope.style = { position: "absolute", top : window.pageYOffset + 'px' };
	};
    } else {
	$scope.style = { position: "fixed" };
    }
////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////

    $scope.held = false;

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
	util.post($http, "/command", {"command": cmd})
	    .success(function (data, status, headers, config) {
		$scope.data = data;
		if (cmd == "pause") $scope.controlTree[0][2] = {cmd: "play"}
		else if (cmd == "play") $scope.controlTree[0][2] = {cmd: "pause"}
	    })
    }

    $scope.hold = function (cmd) {
	$scope.held = setInterval(function() { $scope.command(cmd) }, 200);
    }

    $scope.release = function (cmd) { 
	clearInterval($scope.held);
	$scope.held = false;
    }
}

// var sseSource = new EventSource('/status');

// sseSource.onopen = function () { console.log("OPENED!"); };
// sseSource.onerror = function (e) { console.log(["ERRORED!", e]); };

// sseSource.addEventListener('connection_id', function (e) { console.log(["SSE", e.type, e.data, e]) }, false);
// sseSource.addEventListener('playing', function (e) { console.log(["SSE", e.type, e.data, e]) }, false);
// sseSource.addEventListener('finished', function (e) { console.log(["SSE", e.type, e.data, e])}, false);
// sseSource.addEventListener('command', function (e) { console.log(["SSE", e.type, e.data, e])}, false);

// sseSource.onmessage = function (e) { console.log(["SSE", "UNLABELED", e.type, e.data, e])};