
var app = angular.module("SudsDBApp", ['ui.bootstrap', 'ngSanitize']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});
