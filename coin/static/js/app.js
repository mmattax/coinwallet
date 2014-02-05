/***************************
  Controllers
****************************/
var MainController = ['$scope', '$rootScope', '$location', 'User', function($scope, $rootScope, $location, User) {
  $scope.signupOrLogin = function() {

    var user = new User($scope.user);
    if ($scope.doesntHaveAccount) {
      user = user.$save();
    } else {
      user = user.$authenticate();
    }

    user.then(function(user) {
      $rootScope.user = user;
      $location.url('/wallet')
    });
    
  };

}];

WalletController = ['$scope', 'Transaction', 'transactions', function($scope, Transaction, transactions) {
  $scope.transactions = transactions;

  $scope.sendMoney = function() {
    var transaction = new Transaction($scope.transaction);
    transaction.$save(function(transaction) {
       $scope.transactions.splice(0, 1, transaction);
       $scope.transaction = null;
    })
  };

}];
WalletController.resolve = {
  transactions: ['$q', 'Transaction', function($q, Transaction) {
    var deferred = $q.defer();
    Transaction.query(function(response) {
      deferred.resolve(response.transactions);
    }, function() {
      deferred.reject('An error occured while loading your transactions.'); 
    });
    return deferred.promise;
  }]
};

/***************************
  Services
****************************/
(function() {
  'use strict';
  var module = angular.module('coin.services', ['ngResource']);
  module.factory('User', ['$resource', function($resource) {
    return $resource('/api/user/:action', {}, {
      authenticate: {
        method: 'POST',
        params: {
          action: 'authenticate'
        }
      }
    });
  }]);

  module.factory('Transaction', ['$resource', function($resource) {
    return $resource('/api/transactions', {}, {
      query: { 
        method: 'GET',
        isArray: false 
      } 
    });
  }]);

})();

$(document).ready(function() {
  'use strict';

  var app = angular.module('coin', ['ngRoute', 'coin.services']);
  
  app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    var partialPath = 'static/partials';
    $locationProvider.html5Mode(true);    
    $routeProvider
      .when('/', {
        controller: MainController,
        templateUrl: partialPath + '/index.html'
      })
      .when('/wallet', {
        controller: WalletController,
        templateUrl: partialPath + '/wallet.html',
        resolve: WalletController.resolve
      });
  }]);

  app.run(['$rootScope', function($rootScope) {
    if (window.currentUser) {
      $rootScope.user = window.currentUser;
      currentUser = null;
    }
  }]);

  angular.bootstrap(document, ['coin']);
  
});
