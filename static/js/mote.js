var util = {
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
	$http.post("/show-directory", {}, {params: { dir: path || $location.path() }})
	    .success(function (data, status, headers, config){
		$scope.filesList = data;
	    });
	$location.path(path || $location.path())
    }

    $scope.play = function (path) { 
	$http.post("/play", {}, {params: {target: path}})
    }

    $scope.shuffle = function (path) { 
	$http.post("/play", {}, {params: {target: path, shuffle: true}})
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
	[ // {cmd: "step-backward"},
    	  {cmd: "backward", held: true},
    	  {cmd: "stop"},
    	  {cmd: "pause"},
    	  {cmd: "forward", held: true},
    	  // {cmd: "step-forward"}
	],
    	[{cmd: "volume-down", held: true}, 
    	 {cmd: "volume-off"}, 
    	 {cmd: "volume-up", held: true}]
    ]

    $scope.command = function (cmd) { 
	$http.post("/command", {}, {params: {command: cmd}})
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

function FeedCtrl ($scope, $parse) {
    $scope.playlist = [];

    $scope.fileToDict = function (filename) {
	var split = filename.split(".")
	return {name: split[0], extension: split[1].toLocaleLowerCase()}
    }

    $scope.source = new EventSource('/status');

    $scope.source.onopen = function () { console.log("OPENED!"); };
    $scope.source.onerror = function (e) { console.log(["ERRORED!", e]); };

    $scope.source.addEventListener('playlist', function (e) {
	var res = $parse(e.data)();
	if (res.nowPlaying) {
	    res.nowPlaying = $scope.fileToDict(res.nowPlaying);
	    res.upNext = _.map(res.upNext, $scope.fileToDict)
	} 
	$scope.$apply($scope.playlist = res);
    });

    $scope.source.onmessage = function (e) { 
    	console.log(["SSE", "UNLABELED", e.type, e.data, e])
    };
}