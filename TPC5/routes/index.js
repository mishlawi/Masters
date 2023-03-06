var express = require('express');
var router = express.Router();
var axios = require('axios')

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'DataSet Arq-Son' });
});

router.get('/musicas', function(req, res, next) {
  axios.get("http://localhost:3000/musicas")
  .then(response => {
      var lista = response.data
      res.render('musicas', {musicas:lista})
  })
  .catch(function(erro){
      res.render('error', {error : erro})
  })
});

router.get('/musicas/:id', function(req, res, next) {
  axios.get("http://localhost:3000/musicas?tit=" + req.params.id)
  .then(response => {
      var dados = response.data[0]
      res.render('musica', {musica:dados})
  })
  .catch(function(erro){
      res.render('error', {error : erro})
  })
});

router.get('/musicas/prov/:idProv', function(req, res, next) {
  axios.get("http://localhost:3000/musicas?prov=" + req.params.idProv)
  .then(response => {
      var dados = response.data
      res.render('provincia', {musicas:dados})
  })
  .catch(function(erro){
      res.render('error', {error : erro})
  })
});

module.exports = router;
