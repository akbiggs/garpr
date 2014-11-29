var app = angular.module('myApp', ['ngRoute', 'ui.bootstrap', 'angulartics', 'angulartics.google.analytics', 'facebook']);

var dev = true;
if (dev) {
    var hostname = 'http://garsh0p.no-ip.biz:5101/';
}
else {
    var hostname = 'http://api.garpr.com/';
}

app.service('RegionService', function ($http, PlayerService, TournamentService, RankingsService) {
    var service = {
        regionsPromise: $http.get(hostname + 'regions'),
        regions: [],
        region: '',
        setRegion: function (newRegionId) {
            if (!this.region || newRegionId != this.region.id) {
                this.regionsPromise.then(function(response) {
                    service.region = service.getRegionFromRegionId(newRegionId);
                    PlayerService.playerList = null;
                    TournamentService.tournamentList = null;
                    RankingsService.rankingsList = null;
                    service.populateDataForCurrentRegion();
                });
            }
        },
        getRegionFromRegionId: function(regionId) {
            return this.regions.filter(function(element) {
                return element.id == regionId;
            })[0];
        },
        populateDataForCurrentRegion: function() {
            $http.get(hostname + this.region.id + '/players').
                success(function(data) {
                    PlayerService.playerList = data;
                });

            $http.get(hostname + this.region.id + '/tournaments').
                success(function(data) {
                    TournamentService.tournamentList = data.tournaments.reverse();
                });

            $http.get(hostname + this.region.id + '/rankings').
                success(function(data) {
                    RankingsService.rankingsList = data;
                });
        }
    };

    service.regionsPromise.success(function(data) {
        service.regions = data.regions;
    });

    return service;
});

app.service('PlayerService', function() {
    var service = {
        playerList: null,
        getPlayerIdFromName: function (name) {
            for (i = 0; i < this.playerList.players.length; i++) {
                p = this.playerList.players[i]
                if (p.name == name) {
                    return p.id;
                }
            }
            return null;
        }
    };
    return service;
});

app.service('TournamentService', function() {
    var service = {
        tournamentList: null
    };
    return service;
});

app.service('RankingsService', function() {
    var service = {
        rankingsList: null
    };
    return service;
});

app.config(function(FacebookProvider) {
    FacebookProvider.init('328340437351153');
});

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/:region/rankings', {
        templateUrl: 'rankings.html',
        controller: 'RankingsController',
        activeTab: 'rankings'
    }).
    when('/:region/players', {
        templateUrl: 'players.html',
        controller: 'PlayersController',
        activeTab: 'players'
    }).
    when('/:region/players/:playerId', {
        templateUrl: 'player_detail.html',
        controller: 'PlayerDetailController',
        activeTab: 'players'
    }).
    when('/:region/tournaments', {
        templateUrl: 'tournaments.html',
        controller: 'TournamentsController',
        activeTab: 'tournaments'
    }).
    when('/:region/headtohead', {
        templateUrl: 'headtohead.html',
        controller: 'HeadToHeadController',
        activeTab: 'headtohead'
    }).
    when('/about', {
        templateUrl: 'about.html',
        activeTab: 'about'
    }).
    otherwise({
        redirectTo: '/norcal/rankings'
    });
}]);

app.controller("AuthenticationController", function($scope, $http, Facebook) {
    $scope.loggedIn = false;
    $scope.userInfo = null;

    $scope.handleLogin = function(response) {
        if (response.status == 'connected') {
            console.log(response);

            $http.defaults.headers.common.Authorization = response.authResponse.accessToken;
            console.log(response.authResponse.accessToken);

            Facebook.api('/me', function(response) {
                $scope.$apply(function() {
                    $scope.userInfo = response;
                    console.log($scope.userInfo);
                    $scope.loggedIn = true;
                });
            });
        }
    };

    $scope.login = function() {
        Facebook.login($scope.handleLogin);
    };

    $scope.logout = function() {
        Facebook.logout(function() {
            $scope.$apply(function() {
                $scope.loggedIn = false;
                $scope.userInfo = null;
                $http.defaults.headers.common.Authorization = undefined;
            });
        });
    };

    Facebook.getLoginStatus(function(response) {
        $scope.handleLogin(response);
    });
});

app.controller("RegionDropdownController", function($scope, $route, RegionService) {
    $scope.regionService = RegionService;
    $scope.$route = $route;
});

app.controller("RankingsController", function($scope, $routeParams, RegionService, RankingsService) {
    RegionService.setRegion($routeParams.region);
    $scope.regionService = RegionService;
    $scope.rankingsService = RankingsService
});

app.controller("TournamentsController", function($scope, $routeParams, RegionService, TournamentService) {
    RegionService.setRegion($routeParams.region);
    $scope.regionService = RegionService;
    $scope.tournamentService = TournamentService;
});

app.controller("PlayersController", function($scope, $routeParams, RegionService, PlayerService) {
    RegionService.setRegion($routeParams.region);
    $scope.regionService = RegionService;
    $scope.playerService = PlayerService;
});

app.controller("PlayerDetailController", function($scope, $http, $routeParams, RegionService) {
    RegionService.setRegion($routeParams.region);
    $scope.regionService = RegionService;
    $scope.playerId = $routeParams.playerId;

    $http.get(hostname + $routeParams.region + '/players/' + $routeParams.playerId).
        success(function(data) {
            $scope.playerData = data;
        });

    $http.get(hostname + $routeParams.region + '/matches/' + $routeParams.playerId).
        success(function(data) {
            $scope.matches = data.matches.reverse();
        });

});

app.controller("HeadToHeadController", function($scope, $http, $routeParams, RegionService, PlayerService) {
    RegionService.setRegion($routeParams.region);
    $scope.regionService = RegionService;
    $scope.playerService = PlayerService;
    $scope.player1 = null;
    $scope.player2 = null;
    $scope.wins = 0;
    $scope.losses = 0;

    $scope.onChange = function() {
        if ($scope.player1 != null && $scope.player2 != null) {
            $http.get(hostname + $routeParams.region + 
                '/matches/' + $scope.player1.id + '?opponent=' + $scope.player2.id).
                success(function(data) {
                    $scope.playerName = $scope.player1.name;
                    $scope.opponentName = $scope.player2.name;
                    $scope.matches = data.matches.reverse();
                    $scope.wins = data.wins;
                    $scope.losses = data.losses;
                });
        }
    };

    $scope.typeaheadFilter = function(playerName, viewValue) {
        var lowerPlayerName = playerName.toLowerCase();
        var lowerViewValue = viewValue.toLowerCase();

        // try matching the full name first
        if (lowerPlayerName.indexOf(lowerViewValue) == 0) {
            return true;
        }

        // if viewValue is >= 3 chars, allow substring matching
        // this is to allow players with very short names to appear for small search terms
        if (lowerViewValue.length >= 3 && lowerPlayerName.indexOf(lowerViewValue) != -1) {
            return true;
        }

        var tokens = playerName.split(new RegExp('[-_|. ]', 'g')).filter(function (str) { return str; });
        for (i = 0; i < tokens.length; i++) {
            if (tokens[i].toLowerCase().indexOf(viewValue.toLowerCase()) == 0) {
                return true;
            }
        }

        return false;
    };
});
