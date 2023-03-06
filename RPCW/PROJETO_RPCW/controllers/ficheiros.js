var Ficheiro = require('../models/ficheiros')
const StreamZip = require('node-stream-zip');
const del = require('del')
var fs = require('fs')
var zipFolder = require('zip-folder')

module.exports.createSIP = () => {
    console.log("Criando SIP")
    if(fs.existsSync('./sip.zip'))
        fs.unlinkSync('./sip.zip')
    console.log(" |-- SIP.zip apagado")

    if(!fs.existsSync('./public/uploads/RRD-SIP.json'))
        fs.writeFileSync('./public/uploads/RRD-SIP.json', JSON.stringify([]), 'utf8')
    console.log(" |-- RRD-SIP.json criado")

    zipFolder('./public/uploads/','./sip.zip',(err)=>{
      if(err) console.log(" |-- Error: "+err)
      else console.log(" |-- Zip criado com sucesso")
    })
}

module.exports.readSIP = () => {
    console.log("Lendo SIP")
    if (fs.existsSync('./sip.zip')){
        console.log(" |-- SIP encontrado")
        const zip = new StreamZip({
            file:'./sip.zip',
            storeEntries:true
        })
        
        zip.on('ready', async () => {
            console.log(" |-- Zip aberto")
            await Ficheiro.deleteMany();
            var ficheiros = zip.entryDataSync('RRD-SIP.json')
            ficheiros = JSON.parse(ficheiros)
            console.log(" |-- Ficheiros encontrados: "+ficheiros.length)
            if(ficheiros)
                for (let ficheiro of ficheiros) {
                    var novo = new Ficheiro(ficheiro)
                    novo.save()
                }
                console.log(" |-- Ficheiros carregados na BD")
                
                if(fs.existsSync('public/uploads/')) {
                    del.sync(['public/uploads'])
                    console.log(" |-- Pasta de uploads apagada")
                }

                fs.mkdirSync('public/uploads/')
                console.log(" |-- Pasta de uploads criada")
                zip.extract(null, './public/uploads', err => {
                    console.log(err ? " |-- Error: "+err : ' |-- SIP extraido com sucesso');
                    zip.close()
                })
        })
    } 
    else 
        console.log(" |-- SIP não encontrado")
}

module.exports.listar = () => {
    return Ficheiro
        .find() //devolve uma lista enquanto que findOne devolve um objeto só
        .sort({submission_date:-1})
        .exec()
}

module.exports.consultar = id => {
    return Ficheiro
        .findOne({_id: id})
        .exec()
}

// Get by type 
//0-slides 1-exame 2-manual  3-relatório 4-tese
module.exports.getByType = tipo =>{
    return Ficheiro
        .find({type: tipo})
        .sort({submission_date:-1})
        .exec()
}

module.exports.getByName = fname =>{
    return Ficheiro
        .find({"name":{$regex :fname, $options: 'i'}})
        .sort({submission_date:-1})
        .exec()
}

// Get by quem submeteu 
module.exports.getByUser = username =>{
    return Ficheiro
        .find({user: username})
        .sort({submission_date:-1})
        .exec()
}

module.exports.inserir = async f => {
    var novo = new Ficheiro(f)
    
    const data = await fs.readFileSync('./public/uploads/RRD-SIP.json','utf8') 

    let ficheiros = JSON.parse(data)
    ficheiros.push(novo)
    await fs.writeFileSync('./public/uploads/RRD-SIP.json', JSON.stringify(ficheiros), 'utf8')
    
    this.createSIP()
    return novo.save()
}

module.exports.delete = async id =>{
    const data = await fs.readFileSync('public/uploads/RRD-SIP.json','utf8')
    
    let ficheiros = JSON.parse(data)
    console.log("Antes: ",ficheiros)
    var index = -1;
    ficheiros.find(function(item, i){
      if(item._id === id){
        index = i;
      }
    })
    ficheiros.splice(ficheiros.indexOf(index),1)
    
    await fs.writeFileSync('public/uploads/RRD-SIP.json', JSON.stringify(ficheiros), 'utf8') 
    
    this.createSIP()
    return Ficheiro.deleteOne({_id: id})
}

// Mandas os id e tudo que quiseres alterar em objeto {}
module.exports.update = async (id, file) =>{
    const data = await fs.readFileSync('public/uploads/RRD-SIP.json','utf8')
    
    let ficheiros = JSON.parse(data)
    console.log("Ficheiros: ",ficheiros)
    var index = -1;
    ficheiros.find(function(item, i){
      if(item._id === id){
        index = i;
      }
    })
    //let index = ficheiros.indexOf(v => v._id == id)
    console.log("OI ",index,id)
    console.log( ficheiros[0])

    ficheiros[index] = {...ficheiros[index], ...file}

    await fs.writeFileSync('public/uploads/RRD-SIP.json', JSON.stringify(ficheiros), 'utf8') 
    
    this.createSIP()
    return Ficheiro.findByIdAndUpdate(id, file)
}

module.exports.addComentario = async  (id,com) =>{
    const data = await fs.readFileSync('public/uploads/RRD-SIP.json','utf8')
    
    let ficheiros = JSON.parse(data)
    //let index = ficheiros.indexOf(v=> v.id == id)
    var index = -1;
    ficheiros.find(function(item, i){
      if(item._id === id){
        index = i;
      }
    })
    //console.log("È NESTE ",ficheiros[index])
    ficheiros[index].comments.push(com)
    //console.log("oiiiiii",ficheiros[index])

    await fs.writeFileSync('public/uploads/RRD-SIP.json', JSON.stringify(ficheiros), 'utf8') 
    this.createSIP()
    return Ficheiro
   .findByIdAndUpdate(
        {"_id" : id},
        {$push:{"comments":com}} )
}

// File.deleteComentario(id_recurso,id_comentario)
module.exports.deleteComentario = async  (id,id_com) =>{
    console.log("oiiiiiiiiiii")
    const data = await fs.readFileSync('public/uploads/RRD-SIP.json','utf8')
    
    let ficheiros = JSON.parse(data)
    //let index = ficheiros.indexOf(v=> v.id == id)
    var index = -1;
    ficheiros.find(function(item, i){
      if(item._id === id){
        index = i;
      }
    })

    let list_coments = ficheiros[index].comments
    console.log("Lista coments: ",list_coments)
    var index2 = -1;
    list_coments.find(function(item, i){
      if(item._id === id_com){
        index2 = i;
      }
    })
    
    ficheiros[index].comments.splice(index2,1)

    await fs.writeFileSync('public/uploads/RRD-SIP.json', JSON.stringify(ficheiros), 'utf8') 
    this.createSIP()
    return Ficheiro
   .findByIdAndUpdate(
        {"_id" : id},
        { $pull: { "comments": 
            { "_id" : id_com  } 
        }},
        {returnOriginal:false})
}


module.exports.comentarios = id => {
    return Ficheiro
    .find({_id:id},{_id:0,comments:1})
}