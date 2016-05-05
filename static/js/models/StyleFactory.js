app.factory("StyleFactory", function(){
  var styleFactory = this; 

  styleFactory.buildStyle = function(id, name, minIBU, maxIBU, minABV, maxABV){
    var style = {
      id: id,
      name: name,
      minIBU: minIBU,
      maxIBU: maxIBU,
      minABV: minABV,
      maxABV: maxABV
    };

    return style;
  }
  return styleFactory;
});
