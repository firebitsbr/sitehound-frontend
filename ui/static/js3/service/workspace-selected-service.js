var workspaceSelectedService =  ngApp.factory('workspaceSelectedService', [ '$cookies', 'workspaceFactory', function($cookies, workspaceFactory){

    var dataFactory = {}
    var selectedWorkspaceId = null;

    dataFactory.setSelectedWorkspaceId = function(id){
        selectedWorkspaceId = id;
        $cookies.put("workspaceId", id);
    }
//    dataFactory.setSelectedWorkspace = function(workspace){
//        selectedWorkspace = workspace;
//        $cookies.put("workspace", workspace);
//    }
//    dataFactory.setSelectedWorkspaceId = function(workspace){
//        selectedWorkspace = workspace;
//        $cookies.put("workspaceId", workspace._id);
//    }

//    dataFactory.getSelectedWorkspace = function(){
//        return selectedWorkspace;
//    }

    dataFactory.getCookieSelectedWorkspaceId = function(){
        var workspaceId;
        if(selectedWorkspaceId==null){
            workspaceId = $cookies.get("workspaceId");
        }
        else{
            workspaceId = selectedWorkspaceId;
        }
        return workspaceId;
    }

    dataFactory.getSelectedWorkspaceId = function(){
        var workspaceId;
        if(selectedWorkspaceId==null){
            workspaceId = $cookies.get("workspaceId");
        }
        else{
            workspaceId = selectedWorkspaceId;
        }
        return workspaceId;
    }

    dataFactory.getSelectedWorkspaceAsync = function(){
        var workspaceId;
        if(selectedWorkspaceId==null){
            workspaceId = $cookies.get("workspaceId");
        }
        else{
            workspaceId = selectedWorkspaceId;
        }

		if(workspaceId!=null){
	        return workspaceFactory.getWorkspace(workspaceId)
		}
		else{
			var res ={};
			res.then = function(a, b){
				console.log("No workspace defined!");
			}
			return res;
		}
    }

    return dataFactory;
}]);