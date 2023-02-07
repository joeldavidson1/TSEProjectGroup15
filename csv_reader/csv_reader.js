document.write("Test")

var string = "test, name\n1,zak"

var count = 0; // cache the running count
var result = Papa.parse(string, {
    header: true
});

console.log(result);