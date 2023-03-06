var express = require('express');
var router = express.Router();
var jwt = require('jsonwebtoken');
var axios = require('axios');
var fs = require('fs');
const { db } = require('../models/user');
var Aux = require('../controllers/aux');


router.get('/logs', function(req, res) {
    //console.log("Cookies: ",req.cookies)
    axios.get('http://localhost:8000/api/logs',{
        withCredentials: true,
        headers: {
            'Authorization': req.cookies.token
        }
    })
    .then( logs => {
        Aux.timeLogs(logs.data)
        res.render('admin/logs', {logs: logs.data, dt:dtlogs}) 
    })
    .catch( erro => {
        console.log('Erro na consulta de Logs: ' + erro)
        res.status(501).render('error', {error: erro, message: 'My bad...'})
    })
})

router.get('/logs/download', function(req, res) {
    axios.get('http://localhost:8000/api/logs',{
        withCredentials: true,
        headers: {
            'Authorization': req.cookies.token
        }
    })
    .then( logs => {
        fs.writeFileSync('logs.json', JSON.stringify(logs.data, null, 4))
        res.download('logs.json')
    
    })
    .catch( erro => {
        console.log('Erro no download de Logs: ' + erro)
        res.status(502).render('error', {error: erro, message: 'My bad...'})
    })
})
  
router.get('/users', function(req, res) {
    axios.get('http://localhost:8000/api/users',{
        withCredentials: true,
        headers: {
            'Authorization': req.cookies.token
        }
    })
    .then( users => {
        res.render('admin/users', {users: users.data}) 
    })
    .catch( erro => {
        console.log('Erro na consulta de users: ' + erro)
        res.status(503).render('error', {error: erro, message: 'My bad...'})
    })
})


router.post('/users/add', function(req, res) {
    axios.post('http://localhost:8000/api/users/add', req.body,{
        withCredentials: true,
        headers: {
            'Authorization': req.cookies.token
        }
    })
    .then(res.redirect('/admin/users') )
    .catch( erro => {
        //console.log('Erro na remoção de utilizador: ' + erro)
        res.status(504).render('error', {error: erro, message: 'Erro na remoção de utilizador'})
    })
})



router.post('/users/delete/:id', function(req, res) {
    //console.log(req.cookies.token)
    axios.get('http://localhost:8000/api/users/delete/'+req.params.id,{
        withCredentials: true,
        headers: {
            'Authorization': req.cookies.token
        }
    })
    .then(res.redirect('/admin/users'))
    .catch( erro => {
       // console.log('Erro na remoção de utilizador: ' + erro)
        res.status(505).render('error', {error: erro, message: 'Erro na remoção de utilizador'})
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
    .then(() =>res.redirect('/admin/users'))
    .catch( erro => {
       // console.log('Erro na remoção de utilizador: ' + erro)
        res.status(506).render('error', {error: erro, message: 'Erro na atualização de utilizador'})
    })
})

router.get('/users/create', function(req, res) {
    res.render('admin/user-form') 
})

router.get('/users/:id', function(req, res) {
    axios.get('http://localhost:8000/api/users/'+req.params.id,{
        withCredentials: true,
        headers: {
            'Authorization': req.cookies.token
        }
    })
    .then(dados => res.render('admin/user-edit',{user:dados.data}))
    .catch( erro => {
       // console.log('Erro na remoção de utilizador: ' + erro)
        res.status(507).render('error', {error: erro, message: 'Erro na consulta de utilizador'})
    })
    
})

module.exports = router;
