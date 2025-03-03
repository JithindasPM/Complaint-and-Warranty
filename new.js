// var request = require("request");
// clientID = 'ec41569ae51041eab575322a7f1ed4d7'
// clientSecret = '00b013e862b0441e9e32cd894e2a04ce'

// var options = {
//    method: 'POST',
//    url: 'https://oauth.fatsecret.com/connect/token',
//    method : 'POST',
//    auth : {
//       user : clientID,
//       password : clientSecret
//    },
//    headers: { 'content-type': 'application/x-www-form-urlencoded'},
//    form: {
//       'grant_type': 'client_credentials',
//       'scope' : 'basic'
//    },
//    json: true
// };

// request(options, function (error, response, body) {
//    if (error) throw new Error(error);

//    console.log(body);
// });


const url = 'https://platform.fatsecret.com/rest/server.api';
const accessToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjEwOEFEREZGRjZBNDkxOUFBNDE4QkREQTYwMDcwQzE5NzNDRjMzMUUiLCJ0eXAiOiJhdCtqd3QiLCJ4NXQiOiJFSXJkX19ha2tacWtHTDNhWUFjTUdYUFBNeDQifQ';  // Replace with your actual access token

const payload = {
    method: 'foods.search',
    search_expression: 'toast',
    format: 'json'
};

fetch(url, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
