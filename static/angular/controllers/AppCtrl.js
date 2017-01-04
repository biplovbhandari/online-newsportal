'use strict';

angular.module('mainApp')
.controller('AppCtrl', function ($scope, menu) {
	//var ctrl = this;
	$scope.menu = menu;

    // App Name
    $scope.appName = {c:'default', f:'index'}
	// Side nav Menu Options
 	$scope.menuItems = [
    	{
      		link : '#',
      		title: 'Dashboard',
      		icon: 'fa fa-tachometer fa-2x',
      		toggle: false
    	},
    	{
      		link : '#',
      		title: 'Users',
      		icon: 'fa fa-users fa-2x',
      		toggle: true,
      		pages: [
      			{
		      		link : '#',
		      		title: 'Create',
		      		icon: 'fa fa-cog fa-2x',
      			},
      			{
		      		link : '#',
		      		title: 'Manage',
		      		icon: 'fa fa-files-o fa-2x',
      			},
      		]
    	},
    	{
      		link : '#',
      		title: 'Newsportal',
      		icon: 'fa fa-newspaper-o fa-2x',
      		toggle: true,
      		pages: [
      			{
		      		link : '#',
		      		title: 'Posts',
		      		icon: 'fa fa-pencil fa-2x',
      			},
      			{
		      		link : '#',
		      		title: 'Category',
		      		icon: 'fa fa-th-list fa-2x',
      			},
      		]
    	},
  	];

    // Menu Nav Item
    // Logged In
    $scope.authNavMenuLoggedIn = [
        {
            link : {
                c: 'default',
                f: 'user/profile',
            },
            title: 'Edit Profile',
            icon: 'fa fa-user fa-2x'
        },
        {
            link : '#',
            title: 'Edit Contact',
            icon: 'fa fa-cog fa-2x'
        },
        {
            link : {
                c: 'default',
                f: 'user/logout',
            },
            title: 'Logout',
            icon: 'fa fa-sign-out fa-2x'
        }
    ];

    // Default
    $scope.authNavMenu = [
        {
            link : {
                c: 'default',
                f: 'user/register',
            },
            title: 'Sign Up',
            icon: 'fa fa-user fa-2x'
        },
        {
            link : {
                c: 'default',
                f: 'user/retrieve_password',
            },
            title: 'Lost Password?',
            icon: 'fa fa-lock fa-2x'
        },
        {
            link : {
                c: 'default',
                f: 'user/login',
            },
            title: 'Log In',
            icon: 'fa fa-power-off fa-2x'
        }
    ];

  	// Toggle side-nav
  	$scope.isShowingFullSideMenu = true;
  	$scope.isShowingIconSideMenu = false;

  	$scope.showFullSideMenu = function () {
  		$scope.isShowingFullSideMenu = true;
  		$scope.isShowingIconSideMenu = false;
  	}

  	$scope.showIconSideMenu = function () {
  		$scope.isShowingFullSideMenu = false;
  		$scope.isShowingIconSideMenu = true;
  	}

	// Menu-link and menu-toggle options
	$scope.isToggleOn = function (section) {
		return menu.isSectionSelected(section)
	}

	$scope.toggle = function (section) {
		menu.toggleSection(section);
	}
});