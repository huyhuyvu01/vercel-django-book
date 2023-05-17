
window.onload=function(){
    console.log("detail.js");

// get all the star

    const one = document.getElementById("first");
    const two  = document.getElementById("second");
    const three = document.getElementById("third");
    const four = document.getElementById("fourth");
    const five = document.getElementById("fifth");
    const six = document.getElementById("sixth");
    const seven = document.getElementById("seventh");
    const eight = document.getElementById("eighth");
    const nine = document.getElementById("ninth");
    const ten = document.getElementById("tenth");

    const form = document.querySelector(".rate-form");
    const confirmBox = document.getElementById("confirm-box");

    const csrf = document.getElementsByName("csrfmiddlewaretoken");

    const handleStarSelect =(size)=>{
        const children = form.children
        for (let i=0; i<children.length; i++){
            if (i<=size){
                children[i].classList.add("checked")
            }else{
                children[i].classList.remove("checked")
            }
        }
    }

    const handleSelect = (selection) => {
        switch (selection) {
            case "first":{
                handleStarSelect(1)
                return
            }
            case "second":{
                handleStarSelect(2)
                return
            }
            case "third":{
                handleStarSelect(3)
                return
            }
            case "fourth":{
                handleStarSelect(4)
                return
            }
            case "fifth":{
                handleStarSelect(5)
                return
            }
            case "sixth":{
                handleStarSelect(6)
                return
            }
            case "seventh":{
                handleStarSelect(7)
                return
            }
            case "eighth":{
                handleStarSelect(8)
                return
            }
            case "ninth":{
                handleStarSelect(9)
                return
            }
            case "tenth":{
                handleStarSelect(10)
                return
            }
        }
    }

    const getNumericValue = (stringValue) => {
        let NumericValue;
        if (stringValue === "first"){
            NumericValue = 1;
        }else if (stringValue === "second"){
            NumericValue = 2;
        }else if (stringValue === "third"){
            NumericValue = 3;
        }else if (stringValue === "fourth"){
            NumericValue = 4;
        }else if (stringValue === "fifth"){
            NumericValue = 5;
        }else if (stringValue === "sixth"){
            NumericValue = 6;
        }else if (stringValue === "seventh"){
            NumericValue = 7;
        }else if (stringValue === "eighth"){
            NumericValue = 8;
        }else if (stringValue === "ninth"){
            NumericValue = 9;
        }else if (stringValue === "tenth"){
            NumericValue = 10;
        }
        else{
            NumericValue = 0;
        }
        return NumericValue;
    }


    if (one){
        const arr = [one, two, three, four, five, six, seven, eight, nine, ten];

        arr.forEach(item => item.addEventListener("mouseover", (event) => {
            handleSelect(event.target.id)
        }));

        arr.forEach(item => item.addEventListener("click", (event) => {
            const val = event.target.id;
            console.log(val);

            form.addEventListener("submit", e => {
                e.preventDefault();
                const ISBN = e.target.id;
                const valnum = getNumericValue(val);
                
                $.ajax({
                    type: "POST",
                    url: "./rate-book/",
                    data: {
                        'csrfmiddlewaretoken': csrf[0].value,
                        'el_id': ISBN,
                        'val': valnum,
                    },
                    success: function (response) {
                        console.log(response);
                        confirmBox.innerHTML =`<h1>Successfully rated with ${response.score}</h1>`
                    },
                    error: function(error){
                        console.log(error);
                        confirmBox.innerHTML =`<h1>Something went wrong</h1>`
                    }
                })

            });
        }));
  }
}