var express = require('express');
var router = express.Router();
var Log = require('../controllers/log')
var Auth = require('../controllers/auth');
var Aux = require('../controllers/aux');
var ObjectId = require('mongodb').ObjectId;

const { default: axios } = require('axios');
const { now } = require('mongoose');
const { runInNewContext } = require('vm');


/* GET home page. */
router.get('/', function(req, res) {
  //console.log(req.cookies.token)
  if(req.cookies.token){ // se já está logado
    Auth.authorization(req, res, function(){
      res.redirect('/home')
    })
  }
  else{
    res.render('login')
  }
});

router.get('/registo', function(req, res) {
  res.render('registo') 
})

// Logout
router.get('/logout',Auth.authorization, function(req, res){
  //console.log("Cookies: ",req.cookies, req.session)
  //console.log("Logout ADMIN",req.user)
  Log.insert({user_id:req.user.id,username:req.user.username, action:'logout'})
  res.status(200).clearCookie('token')
  req.session.destroy(function (err) {
    res.redirect('/');
  });
});

router.get('/home',Auth.authorization, function(req, res){
  axios.get('http://localhost:8000/api/news/active',{
    withCredentials: true,
    headers: {
        'Authorization': req.cookies.token
    }
    })
    .then( dados => {
      Aux.datePrettyNews(dados.data)
      console.log("Level   ----- ",req.user)
      res.render('home',{news:dados.data,user:req.user,data:dts,level:req.user.level}) 
    })
    .catch( erro => {
        console.log('Erro na consulta de Noticias: ' + erro)
        res.status(527).render('error', {error: erro, message: 'My bad...'})
    })

})

router.get('/newsTodas',Auth.authorization,Auth.checkLevel(2), function(req, res){
  axios.get('http://localhost:8000/api/news',{
    withCredentials: true,
    headers: {
        'Authorization': req.cookies.token
    }
    })
    .then( dados => {
      Aux.datePrettyNews(dados.data)
      console.log("Level   ----- ",req.user)
      res.render('home',{news:dados.data,user:req.user,data:dts,level:req.user.level}) 
    })
    .catch( erro => {
        console.log('Erro na consulta de Noticias: ' + erro)
        res.status(527).render('error', {error: erro, message: 'My bad...'})
    })
})

router.get('/newsInativas',Auth.authorization,Auth.checkLevel(2), function(req, res){
  axios.get('http://localhost:8000/api/news/inactive',{
    withCredentials: true,
    headers: {
        'Authorization': req.cookies.token
    }
    })
    .then( dados => {
      Aux.datePrettyNews(dados.data)
      console.log("Level   ----- ",req.user)
      res.render('home',{news:dados.data,user:req.user,data:dts,level:req.user.level}) 
    })
    .catch( erro => {
        console.log('Erro na consulta de Noticias: ' + erro)
        res.status(527).render('error', {error: erro, message: 'My bad...'})
    })
})



// Recursos
router.get('/recursos',Auth.authorization, function(req, res){
  axios.get('http://localhost:8000/api/recursos',{
    withCredentials: true,
    headers: {
        'Authorization': req.cookies.token
    }
    })
    .then( files => {
      Aux.datePretty(files)
      if (req.user.level==2) {
        res.render('admin/index', {files: files.data,dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
      //}else if (req.user.level== 0){
      //  res.render('alunos/index', {files: files.data,dCriacao:dtscriacao,dSub:dtsubm})
      }else{
        //console.log(dtscriacao)
        res.render('recursos', {files: files.data, dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
      }
    })
    .catch( erro => {
        console.log('Erro na consulta de Files: ' + erro)
        res.status(528).render('error', {error: erro, message: 'My bad...'})
    })
    
})

/* GET Recusos por tipo Page /tipo/tipo */
router.get('/tipo/:tipo',Auth.authorization, function(req, res, next) {
  axios.get('http://localhost:8000/api/recursos?tipo='+req.params.tipo,{
    withCredentials: true,
    headers: {
        'Authorization': req.cookies.token
    }
    })
  .then(files=>{
      Aux.datePretty(files)
      if (req.user.level==2) {
        res.render('admin/index', {files: files.data,dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
      }else{
        res.render('recursos', {files: files.data,dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
      }
  })
  .catch(e => res.status(529).render('error',{error:e}))
});


/* GET Recusos por pal in titulo Page /recursos/search */
router.get('/recursos/search',Auth.authorization, function(req, res, next) {
  console.log("SEARCH POR:",req.query['search'],req.query['search']!='')
  if (req.query['search']!=undefined & req.query['search']!=''){
    axios.get('http://localhost:8000/api/recursos?q='+req.query['search'],{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
      })
    .then(files=>{
        Aux.datePretty(files)
        if (req.user.level==2) {
          res.render('admin/index', {files: files.data,dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
        }else{
          res.render('recursos', {files: files.data,dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
        }
    })
    .catch(e => res.status(530).render('error',{error:e}))
}else{
  res.redirect('/recursos')
}
});

//Get um recurso
router.get('/recursos/:rid',Auth.authorization, function(req, res) {
  axios.get('http://localhost:8000/api/recursos/'+req.params.rid,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(dados => {
      Log.insert({user_id:req.user.id,username:req.user.username, action:'Visualização',recurso:req.params.rid})
      
      if (dados.data.creation_date!=null) dc = dados.data.creation_date.split('T')[0]
      else dc = "Não especificado"
      a = dados.data.submission_date.split('T')
      sd = a[0]
      hd = a[1].toString().substring(0,5)

      //console.log(dados.data.comments)
      Aux.datePrettyComments(dados.data.comments)
      //console.log(sd,"Horas:",hd)
      res.render('recurso',{rec:dados.data,dCriacao:dc,dSubm:sd,hSubm:hd,user:req.user,dCom:dts,level:req.user.level})
  })
  .catch( erro => {
     //console.log('Erro na remoção de utilizador: ' + erro)
      res.status(531).render('error', {error: erro, message: 'Erro na consulta de recurso'})
  })
  
})

// ADD file - Admin(2) e Professor(1)
router.get('/recurso/add',Auth.authorization,Auth.checkLevel([1,2]), function(req, res){
  res.render('addRecurso',{level:req.user.level})
})

// download recurso
router.get('/download/:rid',Auth.authorization, (req, res) => {
  axios.get('http://localhost:8000/api/recursos/'+req.params.rid,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(dados => {
      Log.insert({user_id:req.user.id,username:req.user.username, action:'Download',recurso:req.params.rid})
      res.download(dados.data.path)
  })
  .catch( erro => {
     // console.log('Erro na remoção de utilizador: ' + erro)
      res.status(532).render('error', {error: erro, message: 'Erro no download de recurso'})
  })

  
});

// Get view recurso edit
router.get('/recursos/edit/:rid',Auth.authorization,Auth.checkLevel([1,2]), function(req, res){
  axios.get('http://localhost:8000/api/recursos/'+req.params.rid,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(dados => {
      if (dados.data.creation_date) dc = dados.data.creation_date.split('T')[0]
      else dc = "Não especificado"
      a = dados.data.submission_date.split('T')
      sd = a[0]
      hd = a[1].toString().substring(0,5)
      console.log(dados.data)
      res.render('recurso-edit',{rec:dados.data,dCriacao:dc,dSubm:sd,hSubm:hd,user:req.user, level:req.user.level})
  })
  .catch( erro => {
     //console.log('Erro na remoção de utilizador: ' + erro)
      res.status(533).render('error', {error: erro, message: 'Erro na edição de recurso'})
  })
})

// edit recurso
router.post('/recursos/edit/:rid', function(req, res) {
  console.log(req.body,req.params.rid)
  var id = req.params.rid
  axios.put('http://localhost:8000/api/recursos/'+id, req.body,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(() =>res.redirect('/recursos/'+id))
  .catch( erro => {
     //console.log('Erro na remoção de utilizador: ' + erro)
      res.status(534).render('error', {error: erro, message: 'Erro na atualização de recurso'})
  })
})

// Get submissoes de um user
router.get('/submissions',Auth.authorization,Auth.checkLevel([1,2]), function(req, res){
  axios.get('http://localhost:8000/api/submissions/'+req.user.username,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(files => {
      Aux.datePretty(files)
      res.render('mysub',{files: files.data,dCriacao:dtscriacao,dSub:dtsubm,level:req.user.level})
  })
  .catch( erro => {
     // console.log('Erro na remoção de utilizador: ' + erro)
      res.status(535).render('error', {error: erro, message: 'Erro na consulta de recurso'})
  })
  
})

// Adicionar comentario ao recurso
router.post('/addComentario/:rid',Auth.authorization, (req, res) => {
  console.log("Body : ",req.body)
  comment={}
  comment.from=req.user.username
  date = new Date()
  comment.date= date.toISOString()
  comment.content = req.body.comentario
  comment._id = new ObjectId();
  if(req.body.rating) comment.rating=req.body.rating
  rec_id = req.params.rid
  
  axios.put('http://localhost:8000/api/addComment/'+req.params.rid,comment,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(res.redirect('/recursos/'+rec_id ))
  .catch( erro => {
      res.status(536).render('error', {error: erro, message: 'Erro na inserção de comentário'})
  })
})

// /deleteComentario/
router.post('/deleteComentario/:cid/recurso/:rid',Auth.authorization, (req, res) => {
  console.log("com_id: ",req.params.cid," Rec id ",req.params.rid)
  let com_id = req.params.cid
  let rec_id = req.params.rid

  axios.delete('http://localhost:8000/api/deleteComment/'+com_id+'/recurso/'+rec_id,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(res.redirect('/recursos/'+rec_id ))
  .catch( erro => {
      res.status(537).render('error', {error: erro, message: 'Erro na remoção de comentário'})
  })
})

router.get('/profile',Auth.authorization, function(req, res) {
  axios.get('http://localhost:8000/api/users/' + req.user.id,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(dados =>{res.render('profile',{user:dados.data,level:req.user.level})})
  .catch( erro => {
     // console.log('Erro na remoção de utilizador: ' + erro)
      res.status(538).render('error', {error: erro, message: 'Erro na consulta de utilizador'})
  })
  
})

router.post('/addNews',Auth.authorization, function(req, res) {
  console.log(req.body)
  data = new Date()
  n = {user:req.user.username,date:data.toISOString(),action:2,free:req.body.free,active:1}
  axios.post('http://localhost:8000/api/addNew',n,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(() => res.redirect('/home'))
  .catch( erro => {
     // console.log('Erro na remoção de utilizador: ' + erro)
      res.status(538).render('error', {error: erro, message: 'Erro na consulta de utilizador'})
  })
})

router.post('/users/update/:id', function(req, res) {
  console.log(req.body)
  var id = req.params.id
  axios.post('http://localhost:8000/api/users/update/'+id, req.body,{
      withCredentials: true,
      headers: {
          'Authorization': req.cookies.token
      }
  })
  .then(() =>res.redirect('/profile'))
  .catch( erro => {
     // console.log('Erro na remoção de utilizador: ' + erro)
      res.status(506).render('error', {error: erro, message: 'Erro na atualização de utilizador'})
  })
})

module.exports = router;
