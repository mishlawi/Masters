var fs = require('fs');
var http = require('http')
var url = require('url')

function getMovie(movies) {

    let rawdata = fs.readFileSync('./source.json');
    let cinemas = JSON.parse(rawdata);
    cinemas.forEach((filme) => {
        movies.push(filme)
    });
}

// Sorts each of the movies by name
function sortMovies(movies) {
    movies.sort(function (a, b) {
        if (a.title < b.title) {
            return -1;
        }
        if (a.title > b.title) {
            return 1;
        }
        return 0;
    })
    return movies

}

function writeIndex(movies) {
    var x = 1
    index = "<!doctype html>\n<html lang=\"en\">\n<head>\n\t<meta charset=\"utf-8\"></meta>\n";
    index += "\t<title>Movies</title>\n</head>\n<body>\n\t<h1><b>Movie List</b></h1>\n\t<ol>\n"
    movies.forEach((movie) => {
        index += "\t\t<li><a href=\"" + "src/f" + x + ".html\">" + movie.title + "</a></li>\n"
        x += 1
    });
    index += "\t</ol>\n</body>\n</html>"
    fs.writeFileSync('index.html', index);

}

function writeMovies(movies) {
    const dir = './src';
    try {
        fs.mkdirSync(dir);
    } catch (error) {}
    let a = 1


    movies.forEach((filme) => {
        let skeleton = "<!doctype html>\n <html lang =\"en\">\n<head>\n\t<meta charset=\"utf-8\"></meta>\n\t<title>"
        skeleton += filme.title + "</title>\n</head>\n<body>\n\t<h1><b>Filme: </b>" +
            filme.title + " (" + filme.year + ")</h1>\n" + "\n\t<ul>\n\t\t<b> Cast: </b>\n"
        filme.cast.forEach(actor => {
            skeleton += "\t\t<li>" + actor + "</li>\n"
        })
        skeleton += "\t</ul><br><br>\n\t<ul>\n\t\t<b> Genres: </b>\n"
        filme.genres.forEach(genre => {
            skeleton += "\t\t<li>" + genre + "</li>\n"
        })
        skeleton += "\t</ul>\n</body>\n</html>"

        fs.writeFileSync('src/f' + a + '.html', skeleton);

        a += 1

    })

}

var movies = []
getMovie(movies)
movies = sortMovies(movies)
writeIndex(movies)
writeMovies(movies)
console.log("Parsing e criação de página html efetuado.")
http.createServer(function(req, res) {
    
    
    var myUrl = url.parse(req.url, true).pathname
    if(myUrl == '/filmes'){
        
        res.writeHead(200, { 'Content-Type': 'text/html' });
        var index = fs.readFileSync("./index.html")
        res.write(index)
    
        console.log(req.method + " " + req.url + " " + d)

    }else{
        var d = new Date().toISOString().substring(0,16)
        console.log(req.method + " " + req.url + " " + d)

        var page = fs.readFileSync("./" + req.url)

        res.writeHead(200, { 'Content-Type': 'text/html' })
        res.write(page)
    }
    

}).listen(32121);
console.log("Servidor iniciado porta 32121")    