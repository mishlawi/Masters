var express = require('express');
var router = express.Router();
var Ficheiro = require('../controllers/ficheiro')

var fs = require('fs')

var multer = require('multer')
var upload = multer({ dest: 'uploads' })


router.get('/', function(req, res) {
    Ficheiro.list()
        .then(data => res.render('index', { list: data }))
        .catch(error => res.render('error', { error: error }))
});

router.post('/submitFile', upload.single('myFile'), (req, res) => {
    var d = new Date().toISOString().substring(0, 16)
    let oldPath = __dirname.substring(0, __dirname.length - 6) + '/' + req.file.path
    let newPath = __dirname.substring(0, __dirname.length - 6) + 'uploads/' + req.file.originalname

    fs.rename(oldPath, newPath, erro => {
        if (erro) throw erro
    })

    var ficheiro = {
        data: d,
        _id: req.file.originalname,
        mimetype: req.file.mimetype,
        descricao: req.body.descricao
    }


    Ficheiro.insert(ficheiro)
        .then(() => res.redirect('/'))
        .catch(e => res.render('error', { error: e }))

})

router.post('/deleteFile/:id', (req, res) => {
    Ficheiro.remove(req.params.id)
    fs.unlinkSync(__dirname.substring(0, __dirname.length - 6) + 'uploads/' + req.params.id)
    res.redirect('/')
})

module.exports = router;