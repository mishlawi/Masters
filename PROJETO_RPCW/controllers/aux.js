var Aux = module.exports;

Aux.timeLogs = function(logs){
  dtlogs = []
  for (var i in logs){

    // 2022-06-16T15:36:41.731Z
    d = logs[i].date.split('T')[0]
    temp = d.split('-').reverse().join('-') + " "
    h = logs[i].date.split('T')[1]
    h = h.toString().substring(0,8)
    temp += h
    dtlogs.push(temp)
  }
  return dtlogs
}

Aux.datePretty = function(files){
    // por data de submissão para submissão 
        // do género há 8min
        // submissão - data hoje 
        var now = new Date()
        year_now = now.getFullYear()
        month_now = now.getMonth()+1
        day_now = now.getDate()
        hour_now = now.getHours()
        min_now = now.getMinutes()
        //hour_now = 
        dtscriacao = []
        dtsubm = []
        for (var i in files.data){
          // Data criação
          //console.log(files.data[i])
          if (files.data[i].creation_date){
            dc = files.data[i].creation_date.split('T')[0]
            dtscriacao.push(dc.split('-').reverse().join('-'))
          }else{
            dtscriacao.push('Não especificado')
          }
          // Data submissão
          subDate = new Date(files.data[i].submission_date.toString())
          year = subDate.getFullYear()
          month= subDate.getMonth()+1
          day= subDate.getDate()
          hour = subDate.getHours()-1
          min= subDate.getMinutes() 
          //console.log("TODAY---> ",year_now,month_now,day_now,' hora: ',hour_now,min_now)
          //console.log("SUB  ---> ",year,month,day,' hora: ',hour,min)
          //console.log("day: ",day," hour: ",hour," min: ",min )
          if (year==year_now){
             if(month==month_now){
                if (day==day_now){
                  if(hour==hour_now){
                    if(min==min_now){
                      dtsubm.push('agora mesmo')
                    }else{
                      mdiff= min_now-min
                      dtsubm.push('há '+mdiff+' min')
                    }
                  }else{
                    hdiff= hour_now-hour
                    if (hdiff==1) dtsubm.push('há '+hdiff+' hora')
                    else dtsubm.push('há '+hdiff+' horas')
                  }
                }else{
                  ddiff= day_now-day
                  if (ddiff==1) dtsubm.push('há '+ddiff+' dia')
                  else dtsubm.push('há '+ddiff+' dias')
                }
             }else{
              // mesmo ano, mês diferente --> há x meses
              mdiff= month_now-month
              if (mdiff==1) dtsubm.push('há '+mdiff+' mês')
              else dtsubm.push('há '+mdiff+' meses')
             }
          }else{
            dtsubm.push(day+'-'+month+'-'+year+' Hora: '+hour+':'+min)
          }
        }
    return dtscriacao, dtsubm
}

Aux.datePrettyComments = function(list_comments){
  // por data de submissão para submissão 
      // do género há 8min
      // submissão - data hoje 
      var now = new Date()
      year_now = now.getFullYear()
      month_now = now.getMonth()+1
      day_now = now.getDate()
      hour_now = now.getHours()
      min_now = now.getMinutes()
      //hour_now = 
      dts = []
      for (var i in list_comments){
        
        //Data comentario
        comDate = new Date(list_comments[i].date.toString())
        year = comDate.getFullYear()
        month= comDate.getMonth()+1
        day= comDate.getDate()
        hour = comDate.getHours()
        min= comDate.getMinutes() 
        //console.log("TODAY---> ",year_now,month_now,day_now,' hora: ',hour_now,min_now)
        //console.log("SUB  ---> ",year,month,day,' hora: ',hour,min)
        //console.log("day: ",day," hour: ",hour," min: ",min )
        if (year==year_now){
           if(month==month_now){
              if (day==day_now){
                if(hour==hour_now){
                  if(min==min_now){
                    dts.push('agora mesmo')
                  }else{
                    mdiff= min_now-min
                    dts.push('há '+mdiff+' min')
                  }
                }else{
                  hdiff= hour_now-hour
                  if (hdiff==1) dts.push('há '+hdiff+' hora')
                  else dts.push('há '+hdiff+' horas')
                }
              }else{
                ddiff= day_now-day
                if (ddiff==1) dts.push('há '+ddiff+' dia')
                else dts.push('há '+ddiff+' dias')
              }
           }else{
            // mesmo ano, mês diferente --> há x meses
            mdiff= month_now-month
            if (mdiff==1) dts.push('há '+mdiff+' mês')
            else dts.push('há '+mdiff+' meses')
           }
        }else{
          dts.push(day+'-'+month+'-'+year+' Hora: '+hour+':'+min)
        }
      }

  return dts
}


Aux.datePrettyNews = function(list_news){
  // por data de submissão para submissão 
      // do género há 8min
      // submissão - data hoje 
      var now = new Date()
      year_now = now.getFullYear()
      month_now = now.getMonth()+1
      day_now = now.getDate()
      hour_now = now.getHours()
      min_now = now.getMinutes()
      //hour_now = 
      dts = []
      for (var i in list_news){
        
        //Data comentario
        comDate = new Date(list_news[i].date.toString())
        year = comDate.getFullYear()
        month= comDate.getMonth()+1
        day= comDate.getDate()
        hour = comDate.getHours()
        min= comDate.getMinutes() 
        //console.log("TODAY---> ",year_now,month_now,day_now,' hora: ',hour_now,min_now)
        //console.log("SUB  ---> ",year,month,day,' hora: ',hour,min)
        //console.log("day: ",day," hour: ",hour," min: ",min )
        if (year==year_now){
           if(month==month_now){
              if (day==day_now){
                if(hour==hour_now){
                  if(min==min_now){
                    dts.push('agora mesmo')
                  }else{
                    mdiff= min_now-min
                    dts.push('há '+mdiff+' min')
                  }
                }else{
                  hdiff= hour_now-hour
                  if (hdiff==1) dts.push('há '+hdiff+' hora')
                  else dts.push('há '+hdiff+' horas')
                }
              }else{
                ddiff= day_now-day
                if (ddiff==1) dts.push('há '+ddiff+' dia')
                else dts.push('há '+ddiff+' dias')
              }
           }else{
            // mesmo ano, mês diferente --> há x meses
            mdiff= month_now-month
            if (mdiff==1) dts.push('há '+mdiff+' mês')
            else dts.push('há '+mdiff+' meses')
           }
        }else{
          dts.push(day+'-'+month+'-'+year+' Hora: '+hour+':'+min)
        }
      }

  return dts
}