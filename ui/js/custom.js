    function disableButton(){
        document.getElementById("approve").classList.add("disabled");
        document.getElementById("reject").classList.add("disabled");  
        
        document.getElementById("resolve").classList.remove("disabled");
    }

    function enableButton(){
        document.getElementById("approve").classList.remove("disabled");
        document.getElementById("reject").classList.remove("disabled");  
        
        document.getElementById("resolve").classList.add("disabled");
    }

    function rejectButton(){
        document.getElementById("approve").classList.add("disabled");
        document.getElementById("resolve").classList.add("disabled");

        document.getElementById("reject").classList.remove("disabled");  
    }
