'use strict';

angular.module('mainApp')
// This can store template that can be loaded from the custom directive
// See https://docs.angularjs.org/api/ng/service/$templateCache
.run(function ($templateCache) {
	$templateCache.put('menu-toggle.template.html',
		'<md-button layout="row" ng-click="toggleIt()"> \n ' +
		'   <i ng-if="item.icon" class="{{item.icon}}" aria-hidden="true"></i> \n ' +
		'	<div class="menu-title" style="padding: inherit;">{{item.title}}</div>  \n ' +
		'	<i ng-show="!ifToggleOn()" \n ' +
		'      class="fa fa-chevron-circle-down pull-right" \n ' +
		'      aria-hidden="true"></i> \n ' +
		'	<i ng-show="ifToggleOn()" \n ' +
		'      class="fa fa-chevron-circle-up pull-right" \n ' +
		'      aria-hidden="true"></i> \n ' +
		'</md-button> \n ' +
		'<md-divider></md-divider> \n ' +
		'<md-list ng-show="ifToggleOn()"> \n ' +
		'   <md-list-item ng-repeat="page in item.pages"> \n ' +
		'	    <menu-link></menu-link> \n ' +
		'   </md-list-item> \n ' +
		'</md-list>'
	);
})
// There is some naming convention for the custom directive
// See https://docs.angularjs.org/guide/directive
.directive('menuToggle', function () {
	// Runs during compile
	// Runs after config before directive's compile function like the below or the controllers
	// See http://stackoverflow.com/questions/20663076/angularjs-app-run-documentation
	return {
		templateUrl: 'menu-toggle.template.html',
		link: function ($scope) {

			$scope.ifToggleOn = function () {
				return $scope.isToggleOn($scope.item);
			}

			$scope.toggleIt = function () {
				$scope.toggle($scope.item);
			}

		}
	};
});