'use strict';

angular.module('mainApp')
.controller('LoginCtrl', function($http, $sanitize, $location) {

	var ctrl = this;

    var authData = {};

    ctrl.showLoginForm = true;
    ctrl.showLoginProgressIndicator = false;

    var hideLoginProgressIndicator = function() {
        ctrl.showLoginProgressIndicator = false;
    }

    var showLoginProgressIndicator = function() {
        ctrl.showLoginProgressIndicator = true;
    }

    var hideLoginForm = function() {
        ctrl.showLoginForm = false;
    }

    var showLoginForm = function() {
        ctrl.showLoginForm = true;
    }

	ctrl.tryLogin = function (loginData) {

        // Hide Login Form
        hideLoginForm();

        // Show login progress Indicator
		showLoginProgressIndicator();

		// Sanitize input
		var email = sanitizeString(loginData.email);
		var password = sanitizeString(loginData.password);
    };

	var sanitizeString = function(string) {
		return $sanitize(string);
	};
});