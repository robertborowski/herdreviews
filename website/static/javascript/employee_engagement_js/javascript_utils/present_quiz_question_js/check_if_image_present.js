// Get an array of all the classes with this name. In this case all questions on the quiz will have this class
var img_array = document.getElementsByClassName("class-check-if-image-is-present");

// Loop through each element in the array and if there is no image present then add a class to that class, so that in CSS I can change the display to none for that combination of classes
for(var i = 0; i < img_array.length; i++) {
  if(img_array[i].src == 'http://localhost:5000/create/question/user/form/submit/no%20aws%20image%20url' || 
  img_array[i].src == 'http://localhost:5000/no%20aws%20image%20url' || 
  img_array[i].src == 'http://localhost:5000/quiz/archive/no%20aws%20image%20url' || 
    img_array[i].className += " no-image-present";
  }
}