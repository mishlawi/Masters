var http = require('http')
var url = require('url')
const axios = require('axios')



    /*if (Object.keys(elem[index]).length>1){
                for(const k in elem[index]){
                    console.log(`${k}: ${elem[index][k]}`);
                }
            }*/


function TableGen(db, column){
    src = ""
    db.forEach(elem =>{
        src+="<tr>"
        column.forEach(index =>{
        if (elem[index].hasOwnProperty('#text')){
            console.log(elem[index])
            src += "<td>"+ elem[index]["#text"] +"</td>"
        }
        else{
            //console.log(elem[index])
            src += "<td>"+ elem[index] +"</td>"
        }
        })
        src+="</tr>"
    })

    return src
}



function HeadGen(listHead){
    body =  '<meta charset="UTF-8"/>\n'
    body += "<body><table><tr>"

    listHead.forEach(element => {
        
        body+= "<th>" + element + "</th>"
    });
    body += "</tr>"

    return body
}

async function getRequest(flag){
    return await axios.get("http://localhost:3000" + flag)
        .then(function(resp){
            db = resp.data
            src = HeadGen(Object.keys(db[0]))
            src += TableGen(db, Object.keys(db[0]))
            src += "</table></body>"

            return src          
        })
        .catch(function(error){
            console.log("Erro aqui")
            console.log(error)
        })
}

function indexGen(){
    return `<body>
    <h1> TPC3</h1>
    <ul>
        <li> <a href=\"http://localhost:4000/alunos\"> Alunos</a></li>
        <li> <a href=\"http://localhost:4000/instrumentos\"> Instrumentos </a></li>
        <li> <a href=\"http://localhost:4000/cursos\"> Cursos </a></li>
    </ul>
</body>`
}

    

http.createServer(async (req, res) => {
    //console.log(req.method + " " + req.url + " " + d)
    var myUrl = url.parse(req.url, true).pathname
    if(myUrl == '/'){
        res.writeHead(200, {'Content-Type':'text/html;charset=utf-8'})
        content = indexGen()
        res.write(content)
        res.end()
    }else if(myUrl == "/alunos"){
        res.writeHead(200, {'Content-Type': 'text/html'})
        content = await getRequest(myUrl)
        res.write(content)
        res.end()

    } else if(myUrl == "/instrumentos"){
        res.writeHead(200, {'Content-Type': 'text/html'})
        content = await getRequest(myUrl)
        res.write(content)
        res.end()

    }
    else if(myUrl == "/cursos"){
        res.writeHead(200, {'Content-Type': 'text/html'})
        content = await getRequest(myUrl)
        res.write(content)
        console.log(content)
        console.log("yooooo bruv")
        res.end()
    }
    
    /*
    else if(myUrl == "/cursos?_sort=instrumento&_order=desc"){
        res.writeHead(200, {'Content-Type': 'text/html'})
        content = await getRequest(myUrl)
        console.log(content)
        console.log("yooooo")
        res.write(content)
        res.end()
    }
    */
    /*
    
    else if(myUrl == "/cursos?_sort=duracao"){
        res.writeHead(200, {'Content-Type': 'text/html'})
        content = await getRequest(myUrl)
        res.write(content)
        res.end()
    }
    else if(myUrl == "/cursos?_sort=id"){
        res.writeHead(200, {'Content-Type': 'text/html'})
        content = await getRequest(myUrl)
        res.write(content)
        res.end()
    }
    */
    else{
        res.writeHead(404, {'Content-Type': 'text/html'})
        res.write('<p>File not found ' + req.url + '</p>')
        res.end()
    }
   
    
    
}).listen(4000);