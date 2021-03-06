'use strict';

angular.module('mainApp')
.factory('menu', function () {

    var self = {};
    self = {
    	toggleSection: function (section) {
        	self.openedSection = (self.openedSection === section ? null : section);
      	},
      	isSectionSelected: function (section) {
        	return self.openedSection === section;
      	}
    };
    return self;
});