var Auth = module.exports;
var jwt = require('jsonwebtoken');

Auth.authorization = (req, res, next) => {
    const token = req.cookies.token || req.headers.authorization;
    //console.log("Auth Token",token)

    if (!token) {
      return res.sendStatus(403);
    }
    try {
      jwt.verify(token,"RPCW2022", function(e, payload){
        if(e) res.status(401).jsonp({error: 'Erro na verificação do token: ' + e})
        else{
          //console.log("Payload: ",payload)
          req.user = {id:payload.user_id, level: payload.level, username: payload.username }
          //console.log(req.user)
          next()
        } 
      })
    } catch {
      return res.sendStatus(403);
    }
  };

Auth.checkLevel = function(permitidos) {
    
    return function(req, res, next) {
        console.log(req.user.level)

        var hasPremissions = false
        // Array of permitidoss
        if (permitidos instanceof Array) {
                if (permitidos.includes(req.user.level))
                    hasPremissions = true
        }
        
        // Number
         else {
            if (req.user.level == permitidos) 
                hasPremissions = true
    
            
        }
        console.log("Tem permissão: ",hasPremissions)
        if (hasPremissions) return next();
        else return res.status(403).send('Não tem premissões suficientes para aceder');
    }
  }