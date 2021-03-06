ngApp.controller('trainingByKeywordController', ['$scope', '$filter', 'seedFactory', 'fetchService', 'seedUrlFactory', 'trainingService',
function ($scope, $filter, seedFactory, fetchService, seedUrlFactory, trainingService, $mdDialog) {


    /* catalog */
    $scope.catalog = {};
    $scope.catalog.udcs = [];

    /* Filters */
    $scope.filters = {};
	$scope.filters.relevances = [];
	$scope.filters.categories = [];
	$scope.filters.udcs = [];


	/** BEGIN GENERATE SE**/

	$scope.generateSeedUrls = function(){
		$scope.errorMessage = "";
		$scope.loading = true;

    $scope.sources = {};
    $scope.sources.searchengine = {}
    $scope.sources.searchengine.checked = true;


		var nResults = 30;
		var crawlProvider = "HH_JOOGLE";

		var crawlSources = [];


		if($scope.sources.searchengine.checked){
			crawlSources.push('SE');
		}
//		if($scope.sources.twitter.checked){
//			crawlSources.push('TWITTER');
//		}
//		else if($scope.source == 'tor'){
//			crawlSources.push('TOR');
//		}
//		else if($scope.source == 'deepdeep'){
//			crawlSources.push('DD');
//		}

		fetchService.generate($scope.master.workspaceId, nResults, crawlProvider, crawlSources)
		.then(function (response) {
			$scope.submittedOk = true;
			$scope.submittedError = false;
//			checkFetch();
			$scope.loading = false;
		},
		function (response) {
			$scope.errorMessage = response.error.message;
			$scope.submittedOk = false;
			$scope.submittedError = true;
			$scope.loading = false;
		});
	}


	/** Fetch pages */
	$scope.seedUrls = [];
    $scope.source = "searchengine";
	$scope.lastId = $scope.seedUrls.length > 0 ? $scope.seedUrls[$scope.seedUrls.length-1]._id : null;

    $scope.getSeedUrls = function(){
        $scope.seedUrls = [];
        $scope.lastId = null;
        $scope.getMoreSeedUrls();
    }


    function refreshUdcOnSuccess(response){
        $scope.catalog.udcs = response.data;
    }

    trainingService.refreshUdc($scope.master.workspaceId, $scope.source, refreshUdcOnSuccess);


	$scope.getMoreSeedUrls = function(){
		seedUrlFactory.get($scope.master.workspaceId, $scope.source, $scope.filters, $scope.lastId)
		.then(function (response) {
			console.log("finish fetching seed Urls");
			var tempResults = response.data;
			angular.forEach(tempResults, function(tempResult){
			    if(tempResult.udc == null || tempResult.udc== undefined){
			        tempResult.udc = [];
			    }
			})

            var currentLength = $scope.seedUrls.length;

			Array.prototype.push.apply($scope.seedUrls, tempResults);

            for (var i = currentLength; i < $scope.seedUrls.length; i++) {
               $scope.$watch('seedUrls[' + i + ']', function (newValue, oldValue) {

                    if(!newValue || !oldValue){
                        console.log("empty objects change");
                        return;
                    }

                    if(
                        newValue.relevant != oldValue.relevant ||
                        newValue.categories != oldValue.categories ||
                        newValue.udc != oldValue.udc
                    ){
                        $scope.updateSeedUrl(newValue);
                        if(newValue.udc != oldValue.udc){
                            trainingService.udcsDirty = true;
                        }
                    }
                    else{
                        console.log("unsupported change");
                    }

               }, true);
            }

			$scope.lastId = tempResults.length > 0 ? tempResults[tempResults.length-1]._id :
				($scope.seedUrls.length > 0 ? $scope.seedUrls[$scope.seedUrls.length-1]._id : null) ;
		},
		function (response) {
		});
	}


    $scope.updateSeedUrl = function(seedUrl){
        trainingService.updateSeedUrl($scope.master.workspaceId, seedUrl, $scope.source, refreshUdcOnSuccess);
    }



}]);
