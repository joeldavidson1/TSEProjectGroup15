document.write("Test")

var string = "test, name\n1,zak"

function readSingleFile(e) {
    var file = e.target.files[0];
    if (!file) {
      return;
    }
    var reader = new FileReader();
    reader.onload = function(e) {
      var contents = e.target.result;
      displayContents(contents);
    };
    reader.readAsText(file);
  }
  
  function displayContents(contents) {
        var count = 0; // cache the running count
        var result = Papa.parse(contents, {
        header: true
});

console.log(result);
  }
  
  document.getElementById('file-input')
    .addEventListener('change', readSingleFile, false);

