var express = require('express');
var router = express.Router();
var User = require('../controllers/user')
var Log = require('../controllers/log')
var Auth = require('../controllers/auth')
var File =  require('../controllers/ficheiros');
var New =  require('../controllers/new');

const fs = require('fs')
// multer- tratar submissão de ficheiros
var multer = require('multer')
var upload = multer({dest: 'public/uploads/'})

var jwt = require('jsonwebtoken');
const { async } = require('node-stream-zip');
var ObjectId = require('mongodb').ObjectId;


router.post('/registo',(req,res) => {
  var u = {
    username: req.body.username,
    password: req.body.password,
    level: req.body.level
  }

  // user.consultar -> se sim -> erro username usado
  User.inserir(u)
    .then(res.redirect('/'))
    .catch(e => res.status(508).render('error',{error: e}))
})


router.post('/login', async function(req, res, next) {
  //console.log("vindo do login : ",req.body)
  let username = req.body.username
  let password = req.body.password
  if (typeof username === "undefined" && !username) 
            throw new Error ("Username não definido")
  if (typeof password === "undefined" && !password)
            throw new Error ("Password não definida")
    
  user = await User.validatePassword(username, password)
  //console.log(user)

  if(user){
    var token = jwt.sign({ user_id: user._id, username: user.username, 
      level:user.level, expiresIn: '1h'}, 'RPCW2022')

    Log.insert({user_id:user._id,username:user.username, action:'login',recurso:'---'})

    res.cookie('token', token, {
    expires: new Date(Date.now() + '1h'), 
    secure: false, // set to true if your using https
    httpOnly: true
    }).status(200).redirect('/home')
    //json({token: token, msg: "Token gerado com sucesso! Pode aceder as rotas protegidas pois o token já está guardado nos cookies."});
  }
  else{
    res.redirect('/')
  }
});

// Logs Routes
router.get('/logs',Auth.authorization,Auth.checkLevel(2),(req, res, next) => {
    Log.list()
        .then( logs => {
            res.jsonp(logs) 
        })
        .catch(error => res.status(509).status(500).send('Erro na listagem de logs'))
})

/*------------------ Users Routes -------------------------*/
router.get('/users',Auth.authorization,Auth.checkLevel(2),(req, res, next) => {
  User.listar()
  .then(users => {
      res.jsonp(users)
  })
  .catch(error => res.status(510).send('Erro a listar utilizador'))
})

router.post('/users/add',Auth.authorization,Auth.checkLevel(2),  (req, res) => {
  User.inserir(req.body)
  .then(() => res.status(200).send('Utilizador Adicionado')) //.then(res.redirect('/admin/users'))
  .catch(error => res.status(511).send('Erro a adicionar utilizador'))
})

router.get('/users/delete/:id',Auth.authorization,Auth.checkLevel(2),  (req, res) => {
  User.remover(req.params.id)
  .then((result) => {
    console.log(result)
    res.status(200).send('Utilizador removido')
  })
  .catch(error => res.status(512).send('Erro a apagar utilizador'))
})

router.post('/users/update/:id',Auth.authorization,  (req, res,next) => {
  var id = req.params.id
  var pass = req.body.password
  var usern = req.body.username
  var nivel = req.body.level
  User.update(id,usern,pass,nivel)
  .then(() => res.status(200).send('Utilizador autualizado'))
  .catch(error => res.status(513).send('Erro ao atualizar utilizador'))
})

router.get('/users/:id',Auth.authorization,  (req, res) => {
  User.consultar(req.params.id)
  .then(user => res.jsonp(user))
  .catch(error => res.status(514).send('Erro a consultar utilizador'))
})



/*------------------ Files Routes -------------------------*/
// Devolve os recursos ordenados por ordem de submissao
router.get('/recursos',Auth.authorization, (req, res) => {
  // GET /api/recursos?tipo=X --> informação dos recursos que contêm pal no título;
  
  console.log("API query: ",req.query)
  if (req.query['tipo']!=undefined){
    console.log(req.query.tipo)
    File.getByType(req.query.tipo)
      .then(dados => {res.status(200).jsonp(dados)})
      .catch(e => {res.status(515).jsonp({ erro: e })})
  //GET /api/recursos?q=pal ->  informação dos recursos que contêm pal no título;
  }else if (req.query['q']!=undefined){
    console.log(req.query.q)
    File.getByName(req.query.q)
      .then(dados => {res.status(200).jsonp(dados)})
      .catch(e => {res.status(516).jsonp({ erro: e })})
  }else{
    File.listar()
    .then(data => {
      res.jsonp(data)})
    .catch(e => res.status(515).render('error',{error: e}))
  }
})

// Regista um recurso no repositório;
router.post('/recursos',Auth.authorization,Auth.checkLevel([1,2]), upload.array('ficheiro'),  (req, res) => {
  console.log(req.files)
  //for( let i = 0;i<req.files.length; i++){
    // console.log("FORM: \n",req.files)
    let path = __dirname + '/../' + req.files[0].path
    let newPath = __dirname + '/../public/uploads/'+req.user.username
    
    if (!fs.existsSync(newPath)){
        fs.mkdirSync(newPath);
    }

    original_name = req.files[0].originalname
    File.getByName(req.files[0].originalname)
    // Ver se há outo ficheiro com mesmo nome
    // se sim, acrescenta ao nome o numero do fich 
    .then(dados => {
      // Se encontrou -> data = [{objeto}]
      if (dados.length!=0){
        original_name = dados.length +  req.files[0].originalname
      }
    
    namemod= original_name.replace(new RegExp(" ", 'g'),"_").replace(new RegExp("#", 'g'),"")
    
    newPath +=  '/'+ namemod

    console.log("path: "+newPath)
    fs.rename(path,newPath, function(error) {
      if (error) throw error
    })
    
    let data = new Date()
    data.setTime( data.getTime() - new Date().getTimezoneOffset()*60*1000 );
    let novoFicheiro = {
        _id: new ObjectId(),
        submission_date: data.toISOString(),
        creation_date: req.body.creation_date,
        producer: req.body.producer,
        user: req.user.username,
        desc: req.body.desc, 
        type: req.body.type,
        name: req.body.name,
        path: newPath,
        mimetype: req.files[0].mimetype,
        size: req.files[0].size

    }

    // New insert
    New.insert({user:req.user.username,date:data.toISOString(),action:0,rec_name:novoFicheiro.name,rec_id:novoFicheiro._id,active:1})
    //console.log("PARA a BD: ",novoFicheiro)
     File.inserir(novoFicheiro)
    .then(()=>res.status(200))
    .catch(error => {res.status(516).jsonp(error)})
  })
  .catch(error => {res.status(517).jsonp(error)})
 // }
  res.redirect('/recursos')
}) 

// delete recurso
router.post('/recursos/:rid',Auth.authorization,Auth.checkLevel([1,2]), (req, res) => {
  File.consultar(req.params.rid)
  .then(data => {
    console.log(data.path)
    fs.unlinkSync(data.path)
    File.delete(req.params.rid)
    .then(
      ()=>res.redirect('/recursos'))
    .catch(error => {res.status(518).jsonp(error)})
  })
  .catch(error => {res.status(519).jsonp(error)})
})

// Devolve a informação em JSON relativa ao recurso com id rid;
router.get('/recursos/:rid',Auth.authorization, (req, res) => {
  File.consultar(req.params.rid)
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(520).jsonp(error)})
})

// put /api/recursos/:rid Altera a informação do recurso com id igual a rid;
router.put('/recursos/:rid',Auth.authorization, (req, res) => {
  obj={}
  obj.type=req.body.type
  if(req.body.name!='') obj.name=req.body.name
  if(req.body.producer!='') obj.producer=req.body.producer
  if(req.body.creation_date!='') obj.creation_date=req.body.creation_date
  if(req.body.desc!=' ') obj.desc=req.body.desc
  //console.log(obj)
  File.update(req.params.rid,obj)
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(521).jsonp(error)})
})

// Get de um user por id /submissions/'+req.user.id
router.get('/submissions/:username',Auth.authorization, (req, res) => {
  File.getByUser(req.params.username)
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(522).jsonp(error)})
})

// /addComment/
router.put('/addComment/:rid',Auth.authorization, (req, res) => {
  id_recurso = req.params.rid
  //console.log("Body : ",req.body)
  if (req.body.rating)
    rat = req.body.rating 
  else
    rat = -1
  File.consultar(id_recurso)
  .then(rec => {
      New.insert({user:req.user.username,date:req.body.date,action:1,rec_id:req.params.rid,rec_name:rec.name,comment:req.body.content,rating:rat,active:1})
  })
  
  File.addComentario(req.params.rid,req.body)
  .then(data => {
    res.jsonp(data)
  })
  .catch(error => {res.status(523).jsonp(error)})
})

//  /deleteComment/'+com_id+'/'+rec_id
router.delete('/deleteComment/:cid/recurso/:rid',Auth.authorization, (req, res) => {
  
  console.log("NA APIIIIIII ",req.params.rid,req.params.cid)
  id_recurso = req.params.rid
  id_comentario = req.params.cid
  File.deleteComentario(req.params.rid,req.params.cid)
  .then(data => {
    res.jsonp(data)
  })
  .catch(error => {res.status(524).jsonp(error)})
})

// GET NEWS
router.get('/news',Auth.authorization, (req, res) => {
  New.list()
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(525).jsonp(error)})
})

// GET NEWS ACTIVE 
router.get('/news/active',Auth.authorization, (req, res) => {
  New.listActive()
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(525).jsonp(error)})
})

// GET NEWS INActive 
router.get('/news/inactive',Auth.authorization, (req, res) => {
  New.listInactive()
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(525).jsonp(error)})
})

// delete new /deleteNew/:nid
router.post('/deleteNew/:nid',Auth.authorization, (req, res) => {
  New.delete(req.params.nid)
  .then(()=>res.redirect('/home'))
  .catch(error => {res.status(526).jsonp(error)})
})

// delete new /hide/:nid
router.post('/newHide/:nid',Auth.authorization, (req, res) => {
  New.hide(req.params.nid)
  .then(()=>res.redirect('/home'))
  .catch(error => {res.status(526).jsonp(error)})
})

router.post('/newShow/:nid',Auth.authorization, (req, res) => {
  New.show(req.params.nid)
  .then(()=>res.redirect('/home'))
  .catch(error => {res.status(526).jsonp(error)})
})

router.post('/addNew',Auth.authorization, (req, res) => {
  New.insert(req.body)
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(525).jsonp(error)})
})

router.put('/editNew/:nid',Auth.authorization, (req, res) => {
  console.log("req body   ---- ", req.body.free)
  New.update(req.params.nid,req.body.free)
  .then(data => {res.jsonp(data)})
  .catch(error => {res.status(525).jsonp(error)})
})

module.exports = router;
