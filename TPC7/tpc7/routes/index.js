var express = require('express');
var axios = require('axios');
var router = express.Router();


const api = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyNGNiYTg0OWJhYmI2NjdjYmZkYzE2ZSIsImlhdCI6MTY0OTE5NTY1MiwiZXhwIjoxNjUxNzg3NjUyfQ.EuvH713Qr6IZ073-5FMF6j5p_3tb6Trv0TOOF5ZHWOPUlCBqKU1H9DTo_ueoCyWhPbEd6F8xzNvn-UkG3J8Ppq65xF8uukoElnSIsi3kldXI2E_EHMv5ETIq-2SGpiBmLyv1zu2broi-nXw18XwKM-WWpoumw5mZacg1qyj4kokGm--WzPIDD15Uibu2ObsDfeHpbDt81Npq-WgEVe56F5w0TdAvY_b-Xvm77hXI4MuaatL9bsOtYEyiepLuBelDyVWjAIoon3-7tB1lwrPnC0OJ_cxKUyCdqx8sZPkmciyTmBsV8fDTyvTP1ibiryAQsDRK5TrG83CcWmStZyDnoQ"

/*Na página inicial, para além de um título e outra informação de contexto,
 deverá aparecer a lista de classes de nível 1 (código e título);*/

router.get('/', function(req, res) {
  axios.get('http://clav-api.di.uminho.pt/v2/classes?nivel=1&apikey='+api)
  .then(resp=>{
    console.log(resp)
    res.render('index', { classes: resp.data });
  })
      .catch( error => {
        res.render('error', { error : error })
      })
});

router.get('/:identification', function(req, res) {
  classe = req.params.identification
  axios.get('http://clav-api.di.uminho.pt/v2/classes/c'+classe+'?apikey='+api)
      .then(resp => {
        res.render('classe', { classe : resp.data })
      })
      .catch( error => {
        res.render('error', { error : error })
      })
});

module.exports = router;
