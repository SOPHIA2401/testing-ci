const https = require('https');
const fetch = require('node-fetch')
const hooks = require('hooks');
const fs = require('fs')

var host = "";
var protocol = "https";
var auth = "";

// Reading .txt file to set URL  
const data = fs.readFileSync('url.txt', {encoding:'utf8', flag:'r'});
// const data = "https://127.0.0.1:9200 admin:admin"
function address()
{
    text = data.toString();
    text = text.split(" ");
    host = text[0].substring(8,text[0].length);
    auth = text[1];
    return (protocol + "://" + auth + "@" + host); 
    // https://admin:admin@https://127.0.0.1:9200
}
  
hooks.before("/_aliases > POST > 200 > application/json",function(transactions,done) {
    transactions.expected.headers['Content-Type'] =  "application/json; charset=UTF-8";
  
    const request = async () => {

        var url = address();
        // var url = "https://admin:admin@https://127.0.0.1:9200";

        // Create an index with non-default settings.
        const cluster = await fetch(url+'/books',{
            method: 'PUT',
            body:JSON.stringify({
            settings : {
                index: {
                    number_of_shards:1,
                    number_of_replicas:0
                   }
                }    
            }),
            headers:{
                "content-type": "application/json; charset=UTF-8"
            }
        });
 
        var actions = {
            actions : [
            {
              add: {
                index: "books",
                alias: "sample-aliases"
              }
            }
          ]  
        }

        transactions.request.body = JSON.stringify(actions);
        done();
    }
    request();  

});
  
hooks.after("/_aliases > POST > 200 > application/json",function(transactions, done){
  
    const request = async () => {

        var url = address();
        // var url = "https://admin:admin@https://127.0.0.1:9200";
        
        // Deleting cluster
        const del = await fetch(url+'/books',{
            method: 'DELETE'
        });

        done();
    }   
    request();
});