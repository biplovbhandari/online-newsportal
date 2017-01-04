'use strict';

angular.module('mainApp')
// This can store template that can be loaded from the custom directive
// See https://docs.angularjs.org/api/ng/service/$templateCache
.run(function ($templateCache) {
	$templateCache.put('menu-link.template.html',
		'<md-button layout="row" id="nav-button" href="{{item.link}}"> \n ' +
		'   <i ng-if="page.icon || item.icon" class="{{page.icon || item.icon}}" aria-hidden="true"></i> \n ' +
		'	<div class="menu-title" style="padding: inherit;">{{page.title || item.title}}</div>  \n ' +
		'</md-button> \n ' + 
		'<md-divider ng-if="page.title == null"></md-divider> \n '
	);
})
// There is some naming convention for the custom directive
// See https://docs.angularjs.org/guide/directive
.directive('menuLink', function () {
	// Runs during compile
	// Runs after config before directive's compile function like the below or the controllers
	// See http://stackoverflow.com/questions/20663076/angularjs-app-run-documentation
	return {
		templateUrl: 'menu-link.template.html',
		//link: function ($scope) {

		//}
	};
});