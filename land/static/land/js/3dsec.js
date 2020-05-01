function _3dsec(url) {
    document.addEventListener("DOMContentLoaded", function(event){
      var iframe = document.createElement('iframe');
        
      iframe.src = url;
      iframe.width = 600;
      iframe.height = 400;
      yourContainer.appendChild(iframe);
    }); // DOMContentLoaded
}